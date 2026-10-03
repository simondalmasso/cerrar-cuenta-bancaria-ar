#!/usr/bin/env python3
"""Deterministic repository-structure checks.

No third-party packages and no network access required.
This does NOT execute an AI model and does NOT certify behavioral compliance.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []

def fail(msg: str) -> None:
    ERRORS.append(msg)

def read(path: str) -> str:
    p = ROOT / path
    if not p.is_file():
        fail(f"missing required file: {path}")
        return ""
    return p.read_text(encoding="utf-8")

skill = read("SKILL.md")
families = []
manifest_version = ""

if skill:
    parts = skill.split("---", 2)
    if len(parts) < 3:
        fail("SKILL.md missing YAML frontmatter delimiters")
        front = ""
    else:
        front = parts[1]

    def top_value(key: str) -> str:
        m = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", front)
        return m.group(1).strip().strip('"').strip("'") if m else ""

    name = top_value("name")
    desc = top_value("description")
    compat = top_value("compatibility")
    version_match = re.search(r"(?m)^  version:\s*['\"]?([^'\"\n]+)['\"]?\s*$", front)
    manifest_version = version_match.group(1).strip() if version_match else ""

    if not name:
        fail("frontmatter missing name")
    elif len(name) > 64 or name != name.lower() or name.startswith("-") or name.endswith("-") or "--" in name or not re.fullmatch(r"[a-z0-9-]+", name):
        fail(f"invalid skill name: {name!r}")
    if not desc or len(desc) > 1024:
        fail(f"description invalid length: {len(desc)}")
    if compat and len(compat) > 500:
        fail(f"compatibility too long: {len(compat)}")
    if not manifest_version:
        fail("metadata.version missing")
    if len(skill.splitlines()) >= 500:
        fail("SKILL.md must stay under 500 lines")
    if ROOT.name == "cerrar-cuenta-bancaria-ar" and name != ROOT.name:
        fail("skill name must match directory name")

    body = parts[2] if len(parts) >= 3 else ""
    if "\\n" in body:
        fail(r"SKILL.md body contains a literal \n escape; use a real newline")

required = [
    "README.md","LICENSE","DISCLAIMER.md","SECURITY.md","CONTRIBUTING.md","agents/openai.yaml",
    "docs/EXECUTIVE-AUDIT.md","docs/TOOLING-AUDIT.md","docs/PRESENTATION.md","docs/RESEARCH-STACK.md","docs/RELEASE-GATE.md","docs/SECURITY-HARDENING.md",
    "references/sources-ar.md","references/bank-discovery.md","references/money-and-blockers.md",
    "references/decision-tree.md","references/evidence-protocol.md","references/escalation-playbook.md","references/special-cases.md","references/post-close.md","references/review-playbook.md",
    "references/jurisprudencia.md","references/integrations.md","references/client-setup.md",
    "references/public-web-research.md","references/source-integrity.md","registry/sources.json","registry/tooling.json","registry/case-law.json","registry/legal-watch.json","registry/case-state.schema.json","registry/review-playbook.json","registry/release-gate.json",
    "evals/scenarios.json","evals/README.md","evals/behavioral-run.schema.json","evals/runs/README.md","banks/README.md","banks/profile.schema.json","examples/case-synthetic/README.md","examples/case-synthetic/handoff.json","examples/case-synthetic/timeline.md",".github/dependabot.yml",".github/workflows/security-codeql.yml",
]
for path in required:
    read(path)

link_re = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
for md in ROOT.rglob("*.md"):
    text = md.read_text(encoding="utf-8")
    for raw in link_re.findall(text):
        target = raw.split("#", 1)[0].strip()
        if not target or re.match(r"^(?:https?://|mailto:)", target):
            continue
        candidate = (md.parent / target).resolve()
        try:
            candidate.relative_to(ROOT.resolve())
        except ValueError:
            fail(f"link escapes repo: {md.relative_to(ROOT)} -> {raw}")
            continue
        if not candidate.exists():
            fail(f"broken local link: {md.relative_to(ROOT)} -> {raw}")

for js in ROOT.rglob("*.json"):
    try:
        json.loads(js.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON {js.relative_to(ROOT)}: {exc}")

try:
    reg = json.loads((ROOT / "registry/sources.json").read_text(encoding="utf-8"))
    ids = []
    for bucket in ("core","optional_mcp","conditional","excluded_as_core"):
        for item in reg.get(bucket, []):
            sid=item.get("id")
            if not sid:
                fail(f"registry item without id in {bucket}")
            ids.append(sid)
    dupes=sorted({x for x in ids if ids.count(x)>1})
    if dupes:
        fail(f"duplicate registry ids: {dupes}")

    for item in reg.get("core", []):
        if item.get("type")=="official" and not str(item.get("url","")).startswith("https://"):
            fail(f"official core source must use https: {item.get('id')}")
        for key in ("allowed_final_hosts","content_type_prefixes","body_markers_any"):
            if not isinstance(item.get(key),list) or not item.get(key):
                fail(f"core source {item.get('id')} missing non-empty {key}")
        if not item.get("expected_path_contains"):
            fail(f"core source {item.get('id')} missing expected_path_contains")

    sha_re=re.compile(r"^[0-9a-f]{64}$")
    for item in reg.get("optional_mcp", []):
        for key in ("pinned_version","license_expression","requires_python","source_repo_url","source_repo_status","source_repo_verified_at"):
            if not item.get(key):
                fail(f"optional MCP {item.get('id')} missing {key}")
        requires_dist=item.get("requires_dist")
        if not isinstance(requires_dist,list) or not all(isinstance(x,str) and x.strip() for x in requires_dist):
            fail(f"optional MCP {item.get('id')} requires_dist must be a string list")
        artifacts=item.get("artifacts")
        if not isinstance(artifacts,list) or len(artifacts)<2:
            fail(f"optional MCP {item.get('id')} must record wheel + sdist artifacts")
            continue
        kinds={a.get("packagetype") for a in artifacts}
        if not {"bdist_wheel","sdist"}.issubset(kinds):
            fail(f"optional MCP {item.get('id')} missing wheel or sdist provenance")
        for artifact in artifacts:
            if not artifact.get("filename") or not sha_re.fullmatch(str(artifact.get("sha256",""))):
                fail(f"optional MCP {item.get('id')} has invalid artifact provenance")
except Exception as exc:
    fail(f"registry validation failed: {exc}")

try:
    tooling=json.loads((ROOT/"registry/tooling.json").read_text(encoding="utf-8"))
    if tooling.get("required_dependencies") != []:
        fail("registry/tooling.json must keep required_dependencies empty")
    tool_ids=[]
    for bucket in ("accepted_optional","accepted_conditional_services"):
        for item in tooling.get(bucket,[]):
            tid=item.get("id")
            if not tid:
                fail(f"tooling item without id in {bucket}")
            tool_ids.append(tid)
            if not str(item.get("url","")).startswith("https://"):
                fail(f"tooling URL must use https: {tid}")
            if item.get("hard_dependency") is True:
                fail(f"optional tooling cannot be a hard dependency: {tid}")
    for item in tooling.get("architectural_references",[]):
        tid=item.get("id")
        if not tid:
            fail("architectural reference without id")
            continue
        if tid in tool_ids:
            fail(f"duplicate tooling/reference id: {tid}")
        tool_ids.append(tid)
        if not str(item.get("url","")).startswith("https://"):
            fail(f"architectural reference URL must use https: {tid}")
        if item.get("hard_dependency") is not False:
            fail(f"architectural reference cannot be a hard dependency: {tid}")
        if item.get("code_imported") is not False:
            fail(f"architectural reference must explicitly record code_imported=false: {tid}")
        if item.get("decision") != "concept_only_no_runtime_dependency":
            fail(f"architectural reference decision invalid: {tid}")
    if len(tool_ids) != len(set(tool_ids)):
        fail("duplicate tooling ids")
    policy=tooling.get("policy",{})
    for key in ("install_automatically","authenticated_browser","bank_credentials","transactional_actions"):
        if policy.get(key) is not False:
            fail(f"tooling policy {key} must be false")
except Exception as exc:
    fail(f"tooling registry validation failed: {exc}")

try:
    case_law=json.loads((ROOT/"registry/case-law.json").read_text(encoding="utf-8"))
    cases=case_law.get("cases",[])
    if len(cases)<5:
        fail(f"expected >=5 verified case-law records, got {len(cases)}")
    ids=set()
    for i,item in enumerate(cases,start=1):
        for key in ("id","status","court","jurisdiction","date","case_name","identifier","verified_summary","relevance","limits","official_url"):
            if not isinstance(item.get(key),str) or not item.get(key).strip():
                fail(f"case-law #{i} missing non-empty {key}")
        cid=item.get("id")
        if cid in ids:
            fail(f"duplicate case-law id: {cid}")
        ids.add(cid)
        if item.get("status")=="VERIFIED_OFFICIAL" and not str(item.get("official_url","")).startswith("https://"):
            fail(f"verified case-law source must use https: {cid}")
        for key in ("topics","use_when"):
            value=item.get(key)
            if not isinstance(value,list) or not value or not all(isinstance(x,str) and x.strip() for x in value):
                fail(f"case-law {cid} requires non-empty string list {key}")
except Exception as exc:
    fail(f"case-law registry validation failed: {exc}")

try:
    playbook=json.loads((ROOT/"registry/review-playbook.json").read_text(encoding="utf-8"))
    if playbook.get("result_states") != ["SATISFIED","OPEN","NOT_APPLICABLE"]:
        fail("review playbook result_states must be SATISFIED/OPEN/NOT_APPLICABLE")
    phases=playbook.get("phases")
    if not isinstance(phases,list) or not phases:
        fail("review playbook requires phases")
    else:
        phase_ids=[]
        check_ids=[]
        allowed_severity={"blocking","important","informational"}
        for phase in phases:
            pid=phase.get("id")
            if not isinstance(pid,str) or not pid:
                fail("review playbook phase missing id")
                continue
            phase_ids.append(pid)
            checks=phase.get("checks")
            if not isinstance(checks,list) or not checks:
                fail(f"review playbook phase {pid} requires checks")
                continue
            for check in checks:
                cid=check.get("id")
                if not isinstance(cid,str) or not cid:
                    fail(f"review playbook {pid} check missing id")
                    continue
                check_ids.append(cid)
                for key in ("category","question","rationale","pass_when"):
                    if not isinstance(check.get(key),str) or not check.get(key).strip():
                        fail(f"review playbook {cid} missing non-empty {key}")
                if check.get("severity") not in allowed_severity:
                    fail(f"review playbook {cid} invalid severity")
                if not isinstance(check.get("evidence_required"),bool):
                    fail(f"review playbook {cid} evidence_required must be boolean")
        if len(phase_ids) != len(set(phase_ids)):
            fail("review playbook duplicate phase ids")
        if len(check_ids) != len(set(check_ids)):
            fail("review playbook duplicate check ids")
        required_phases={"pre-request","pre-escalation","pre-close","post-close"}
        if set(phase_ids) != required_phases:
            fail(f"review playbook phases must be exactly {sorted(required_phases)}")
except Exception as exc:
    fail(f"review playbook validation failed: {exc}")

try:
    state_schema=json.loads((ROOT/"registry/case-state.schema.json").read_text(encoding="utf-8"))
    props=state_schema.get("properties",{})
    if props.get("case_state",{}).get("enum") != list("ABCDEFG"):
        fail("case-state schema must preserve A-G exactly")
    if props.get("response_mode",{}).get("enum") != ["FAST","LIVE","FORENSIC"]:
        fail("case-state schema response_mode must be FAST/LIVE/FORENSIC")
    evidence_enum=props.get("evidence_classes_present",{}).get("items",{}).get("enum")
    if evidence_enum != ["FACT","BANK_CLAIM","USER_CLAIM","INFERENCE","OPEN_GAP"]:
        fail("case-state schema evidence classes drifted")
except Exception as exc:
    fail(f"case-state schema validation failed: {exc}")

try:
    watch=json.loads((ROOT/"registry/legal-watch.json").read_text(encoding="utf-8"))
    core_ids={item.get("id") for item in reg.get("core",[])}
    watched={item.get("source_id") for item in watch.get("sources",[])}
    if watched != core_ids:
        fail(f"legal-watch ids must exactly match core source ids: watched={sorted(watched)} core={sorted(core_ids)}")
    sha_re_local=re.compile(r"^[0-9a-f]{64}$")
    for item in watch.get("sources",[]):
        for key in ("relevant_section","local_claim"):
            if not isinstance(item.get(key),str) or not item.get(key).strip():
                fail(f"legal-watch {item.get('source_id')} missing {key}")
        local_hash=str(item.get("local_claim_sha256",""))
        if not sha_re_local.fullmatch(local_hash):
            fail(f"legal-watch {item.get('source_id')} invalid local_claim_sha256")
        elif hashlib.sha256(item["local_claim"].encode("utf-8")).hexdigest() != local_hash:
            fail(f"legal-watch {item.get('source_id')} local_claim fingerprint mismatch")
        strategy=item.get("strategy")
        if strategy not in {"full_content","semantic_text_windows","availability_only"}:
            fail(f"legal-watch {item.get('source_id')} invalid strategy {strategy!r}")
        if strategy=="full_content":
            remote=item.get("expected_remote_sha256")
            if not sha_re_local.fullmatch(str(remote or "")):
                fail(f"legal-watch {item.get('source_id')} full_content baseline missing/invalid")
        elif strategy=="semantic_text_windows":
            needles=item.get("semantic_needles")
            if not isinstance(needles,list) or not needles or not all(isinstance(x,str) and x.strip() for x in needles):
                fail(f"legal-watch {item.get('source_id')} semantic_needles missing")
            if not sha_re_local.fullmatch(str(item.get("expected_semantic_sha256") or "")):
                fail(f"legal-watch {item.get('source_id')} semantic baseline missing/invalid")
except Exception as exc:
    fail(f"legal-watch registry validation failed: {exc}")

try:
    gate=json.loads((ROOT/"registry/release-gate.json").read_text(encoding="utf-8"))
    gates={item.get("id"):item.get("status") for item in gate.get("gates",[])}
    if gates.get("repository-ci") not in {"PASS","PENDING"}:
        fail("release gate repository-ci status invalid")
    if gates.get("source-integrity") not in {"PASS","PENDING","PASS_WITH_LEGAL_WATCH_BASELINE_PENDING"}:
        fail("release gate source-integrity status invalid")
    if gates.get("behavioral-evals") not in {"NOT_RUN","PASS"}:
        fail("release gate behavioral-evals status invalid")
    if gates.get("immutable-release") not in {"PENDING","PASS"}:
        fail("release gate immutable-release status invalid")
    if gates.get("behavioral-evals")!="PASS" and gate.get("status")!="BLOCKED":
        fail("release gate must remain BLOCKED until behavioral evals PASS")
    if gate.get("status")=="READY" and any(gates.get(k)!="PASS" for k in ("repository-ci","source-integrity","behavioral-evals","immutable-release")):
        fail("release gate cannot be READY before all release-critical gates PASS")
except Exception as exc:
    fail(f"release-gate validation failed: {exc}")

try:
    synthetic=(ROOT/"examples/case-synthetic")
    joined="\n".join(p.read_text(encoding="utf-8",errors="ignore") for p in synthetic.rglob("*") if p.is_file())
    if re.search(r"(?<!\d)\d{8,}(?!\d)", joined):
        fail("synthetic example contains an 8+ digit numeric sequence; keep examples obviously synthetic")
    if "Banco Ejemplo" not in joined or "ficticio" not in joined.lower():
        fail("synthetic example must be explicitly marked fictitious")
except Exception as exc:
    fail(f"synthetic-example validation failed: {exc}")

try:
    ev=json.loads((ROOT/"evals/scenarios.json").read_text(encoding="utf-8"))
    families=ev.get("families",[])
    if len(families)<45:
        fail(f"expected >=45 adversarial eval specifications, got {len(families)}")
    if ev.get("version") != manifest_version:
        fail(f"eval version {ev.get('version')!r} != manifest version {manifest_version!r}")
    legal_baseline=ev.get("legal_baseline") or {}
    if legal_baseline.get("source") != "references/sources-ar.md" or legal_baseline.get("reverify_on_source_change") is not True:
        fail("eval legal_baseline must require re-verification from references/sources-ar.md")
    ids_seen=set()
    names_seen=set()
    for i,case in enumerate(families,start=1):
        if not isinstance(case,dict):
            fail(f"eval #{i} is not an object")
            continue
        for key in ("id","name","prompt"):
            value=case.get(key)
            if not isinstance(value,str) or not value.strip():
                fail(f"eval #{i} missing non-empty {key}")
        for key in ("must","must_not"):
            value=case.get(key)
            if not isinstance(value,list) or not value or not all(isinstance(x,str) and x.strip() for x in value):
                fail(f"eval {case.get('id',i)} requires non-empty string list {key}")
        cid=case.get("id")
        cname=case.get("name")
        if isinstance(cid,str):
            if cid in ids_seen:
                fail(f"duplicate eval id: {cid}")
            ids_seen.add(cid)
        if isinstance(cname,str):
            if cname in names_seen:
                fail(f"duplicate eval name: {cname}")
            names_seen.add(cname)
except Exception as exc:
    fail(f"eval validation failed: {exc}")

readme_text=read("README.md")
changelog_text=read("CHANGELOG.md")
if manifest_version:
    if manifest_version not in readme_text:
        fail(f"README does not mention manifest version {manifest_version}")
    if manifest_version not in changelog_text:
        fail(f"CHANGELOG does not mention manifest version {manifest_version}")


# GitHub Actions supply-chain hardening.
action_ref_re = re.compile(r"(?m)^\s*uses:\s*([^\s#]+)\s*$")
sha40_re = re.compile(r"^[0-9a-f]{40}$")
for wf in (ROOT/".github/workflows").glob("*.yml"):
    txt=wf.read_text(encoding="utf-8")
    if re.search(r"(?m)^\s*permissions:\s*write-all\s*$", txt):
        fail(f"workflow must not use write-all permissions: {wf.relative_to(ROOT)}")
    for ref in action_ref_re.findall(txt):
        if ref.startswith("./"):
            continue
        if "@" not in ref:
            fail(f"workflow action missing immutable ref: {wf.relative_to(ROOT)} -> {ref}")
            continue
        _, version=ref.rsplit("@",1)
        if not sha40_re.fullmatch(version):
            fail(f"workflow action must be pinned to 40-char commit SHA: {wf.relative_to(ROOT)} -> {ref}")

dependabot_text=read(".github/dependabot.yml")
if 'package-ecosystem: "github-actions"' not in dependabot_text:
    fail("Dependabot must monitor github-actions")
if 'interval: "weekly"' not in dependabot_text:
    fail("Dependabot github-actions schedule must be weekly")

codeql_text=read(".github/workflows/security-codeql.yml")
for marker in (
    "security-events: write",
    "languages: python",
    "github/codeql-action/init@",
    "github/codeql-action/analyze@",
    "persist-credentials: false",
):
    if marker not in codeql_text:
        fail(f"CodeQL workflow missing required marker: {marker}")
if re.search(r"(?m)^\s*contents:\s*write\s*$", codeql_text):
    fail("CodeQL workflow must not have contents: write")

privacy_protocol=read("references/evidence-protocol.md")
case_intake=read("assets/templates/case-intake.md")
if "Redactar:" in privacy_protocol or "Redactar datos sensibles" in case_intake:
    fail("ambiguous Spanish 'Redactar' privacy wording is forbidden; use Ocultar/tapar/Nunca incluir")

for obsolete in (
    ROOT/"scripts/check_source_health.py",
    ROOT/"references/source-health.md",
    ROOT/".github/workflows/source-health.yml",
):
    if obsolete.exists():
        fail(f"obsolete source-health path still present: {obsolete.relative_to(ROOT)}")

openai_yaml=read("agents/openai.yaml")
try:
    lines=[line for line in openai_yaml.splitlines() if line.strip() and not line.lstrip().startswith("#")]
    if not lines or lines[0] != "interface:":
        raise ValueError("top-level must be exactly 'interface:'")
    parsed={}
    allowed={"display_name","short_description","default_prompt"}
    for line in lines[1:]:
        if "\t" in line:
            raise ValueError("tabs are not allowed")
        if not line.startswith("  ") or line.startswith("   "):
            raise ValueError(f"expected exactly two-space indentation: {line!r}")
        body=line[2:]
        if ":" not in body:
            raise ValueError(f"missing ':' in {line!r}")
        key,raw=body.split(":",1)
        key=key.strip()
        raw=raw.strip()
        if key not in allowed:
            raise ValueError(f"unexpected key: {key!r}")
        if key in parsed:
            raise ValueError(f"duplicate key: {key!r}")
        if not raw:
            raise ValueError(f"empty scalar: {key}")
        if raw.startswith('"'):
            value=json.loads(raw)
        elif raw.startswith("'") and raw.endswith("'") and len(raw)>=2:
            value=raw[1:-1].replace("''","'")
        else:
            value=raw
        if not isinstance(value,str) or not value.strip():
            raise ValueError(f"{key} must be a non-empty string")
        parsed[key]=value
    missing=allowed-set(parsed)
    if missing:
        raise ValueError(f"missing keys: {sorted(missing)}")
except Exception as exc:
    fail(f"agents/openai.yaml strict subset validation failed: {exc}")

secret_patterns=[
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"jur_[A-Za-z0-9]{20,}"),
    re.compile(r"oarg_sk_[A-Za-z0-9_-]{12,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._~-]{24,}"),
]
for p in ROOT.rglob("*"):
    if not p.is_file() or ".git" in p.parts:
        continue
    if p.suffix.lower() not in {".md",".json",".py",".yml",".yaml",".sh",".ps1"}:
        continue
    txt=p.read_text(encoding="utf-8",errors="ignore")
    for pattern in secret_patterns:
        if pattern.search(txt):
            fail(f"possible secret in {p.relative_to(ROOT)} matching {pattern.pattern}")

if ERRORS:
    print("REPOSITORY STRUCTURE VALIDATION FAILED")
    for err in ERRORS:
        print(f"- {err}")
    sys.exit(1)

print("REPOSITORY STRUCTURE VALIDATION PASS")
print(f"- skill lines: {len(skill.splitlines())}")
print("- local links: pass")
print("- JSON: pass")
print(f"- adversarial eval specifications: {len(families)} (structure pass)")
gate_now=json.loads((ROOT/"registry/release-gate.json").read_text(encoding="utf-8"))
behavioral_status={x.get("id"):x.get("status") for x in gate_now.get("gates",[])}.get("behavioral-evals","UNKNOWN")
print(f"- behavioral agent eval execution: {behavioral_status}")
print("- registry/provenance invariants: pass")
print("- verified case-law registry: pass")
print("- case-state schema + special/post-close scaffolding: pass")
print("- deterministic case-review playbook: pass")
print("- legal-watch registry: structure pass")
print("- synthetic-example privacy lint: pass")
print("- zero-cost tooling policy: pass")
print("- GitHub Actions immutable-pin + Dependabot + CodeQL security baseline: pass")
print("- OpenAI metadata strict-subset parse: pass")
print("- secret scan: pass")