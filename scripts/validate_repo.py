#!/usr/bin/env python3
"""Deterministic repository-structure checks.

No third-party packages and no network access required.
This does NOT execute an AI model and does NOT certify behavioral compliance.
"""
from __future__ import annotations

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
    "docs/EXECUTIVE-AUDIT.md","docs/TOOLING-AUDIT.md",
    "references/sources-ar.md","references/bank-discovery.md","references/money-and-blockers.md",
    "references/decision-tree.md","references/evidence-protocol.md","references/escalation-playbook.md",
    "references/jurisprudencia.md","references/integrations.md","references/client-setup.md",
    "references/public-web-research.md","references/source-integrity.md","registry/sources.json","registry/tooling.json",
    "evals/scenarios.json","evals/README.md",
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
    if len(tool_ids) != len(set(tool_ids)):
        fail("duplicate tooling ids")
    policy=tooling.get("policy",{})
    for key in ("install_automatically","authenticated_browser","bank_credentials","transactional_actions"):
        if policy.get(key) is not False:
            fail(f"tooling policy {key} must be false")
except Exception as exc:
    fail(f"tooling registry validation failed: {exc}")

try:
    ev=json.loads((ROOT/"evals/scenarios.json").read_text(encoding="utf-8"))
    families=ev.get("families",[])
    if len(families)<31:
        fail(f"expected >=31 adversarial eval specifications, got {len(families)}")
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
print("- behavioral agent eval execution: NOT RUN")
print("- registry/provenance invariants: pass")
print("- zero-cost tooling policy: pass")
print("- OpenAI metadata strict-subset parse: pass")
print("- secret scan: pass")