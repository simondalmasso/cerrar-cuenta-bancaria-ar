#!/usr/bin/env python3
"""Deterministic local checks for cerrar-cuenta-bancaria-ar.

No third-party packages and no network access required.
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

required = [
    "README.md",
    "LICENSE",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "references/sources-ar.md",
    "references/bank-discovery.md",
    "references/money-and-blockers.md",
    "references/decision-tree.md",
    "references/evidence-protocol.md",
    "references/escalation-playbook.md",
    "references/jurisprudencia.md",
    "references/integrations.md",
    "references/client-setup.md",
    "registry/sources.json",
    "evals/scenarios.json",
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
    for bucket in ("core", "optional_mcp", "conditional", "excluded_as_core"):
        for item in reg.get(bucket, []):
            sid = item.get("id")
            if not sid:
                fail(f"registry item without id in {bucket}")
            ids.append(sid)
    dupes = sorted({x for x in ids if ids.count(x) > 1})
    if dupes:
        fail(f"duplicate registry ids: {dupes}")
    for item in reg.get("core", []):
        if item.get("type") == "official" and not str(item.get("url", "")).startswith("https://"):
            fail(f"official core source must use https: {item.get('id')}")
except Exception as exc:
    fail(f"registry validation failed: {exc}")

try:
    ev = json.loads((ROOT / "evals/scenarios.json").read_text(encoding="utf-8"))
    families = ev.get("families", [])
    if len(families) < 20:
        fail(f"expected >=20 eval families, got {len(families)}")
    eval_ids = [x.get("id") for x in families]
    if len(eval_ids) != len(set(eval_ids)):
        fail("duplicate eval ids")
except Exception as exc:
    fail(f"eval validation failed: {exc}")

secret_patterns = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"jur_[A-Za-z0-9]{20,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._~-]{24,}"),
]
for p in ROOT.rglob("*"):
    if not p.is_file() or ".git" in p.parts:
        continue
    if p.suffix.lower() not in {".md", ".json", ".py", ".yml", ".yaml", ".sh", ".ps1"}:
        continue
    txt = p.read_text(encoding="utf-8", errors="ignore")
    for pattern in secret_patterns:
        if pattern.search(txt):
            fail(f"possible secret in {p.relative_to(ROOT)} matching {pattern.pattern}")

if ERRORS:
    print("VALIDATION FAILED")
    for err in ERRORS:
        print(f"- {err}")
    sys.exit(1)

print("VALIDATION PASS")
print(f"- skill lines: {len(skill.splitlines())}")
print("- local links: pass")
print("- JSON: pass")
print(f"- eval families: {len(families)}")
print("- registry invariants: pass")
print("- secret scan: pass")
