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

    if not name:
        fail("frontmatter missing name")
    elif len(name) > 64 or name != name.lower() or name.startswith("-") or name.endswith("-") or "--" in name or not re.fullmatch(r"[a-z0-9-]+", name):
        fail(f"invalid skill name: {name!r}")
    if not desc or len(desc) > 1024:
        fail(f"description invalid length: {len(desc)}")
    if compat and len(compat) > 500:
        fail(f"compatibility too long: {len(compat)}")
    if len(skill.splitlines()) >= 500:
        fail("SKILL.md must stay under 500 lines")
    if ROOT.name == "cerrar-cuenta-bancaria-ar" and name != ROOT.name:
        fail("skill name must match directory name")

    body = parts[2] if len(parts) >= 3 else ""
    if "\\n" in body:
        fail(r"SKILL.md body contains a literal \n escape; use a real newline")

required = [
    "README.md","LICENSE","SECURITY.md","CONTRIBUTING.md","agents/openai.yaml",
    "references/sources-ar.md","references/bank-discovery.md","references/money-and-blockers.md",
    "references/decision-tree.md","references/evidence-protocol.md","references/escalation-playbook.md",
    "references/jurisprudencia.md","references/integrations.md","references/client-setup.md",
    "registry/sources.json","evals/scenarios.json","evals/README.md",
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
    ev=json.loads((ROOT/"evals/scenarios.json").read_text(encoding="utf-8"))
    families=ev.get("families",[])
    if len(families)<22:
        fail(f"expected >=22 adversarial eval specifications, got {len(families)}")
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

openai_yaml=read("agents/openai.yaml")
for required_text in ("interface:","display_name:","short_description:","default_prompt:"):
    if required_text not in openai_yaml:
        fail(f"agents/openai.yaml missing {required_text}")

secret_patterns=[
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"jur_[A-Za-z0-9]{20,}"),
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
print("- secret scan: pass")