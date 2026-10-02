#!/usr/bin/env python3
"""Availability/freshness smoke checks for public research sources.

No secrets. No bank access. Optional/conditional sources only warn.
Core source failures make the job fail so maintainers notice breakage.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = json.loads((ROOT / "registry/sources.json").read_text(encoding="utf-8"))
UA = "cerrar-cuenta-bancaria-ar-source-health/1.1 (+https://github.com/simondalmasso/cerrar-cuenta-bancaria-ar)"

def probe(url: str, attempts: int = 2) -> tuple[bool, str]:
    last = ""
    for n in range(attempts):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": UA, "Accept": "*/*"},
                method="GET",
            )
            with urllib.request.urlopen(req, timeout=20) as r:
                code = getattr(r, "status", 200)
                r.read(1024)
                return 200 <= code < 400, f"HTTP {code}"
        except urllib.error.HTTPError as exc:
            last = f"HTTP {exc.code}"
            if exc.code in (401, 403, 405, 429):
                # Reachable but access/rate policy may block automation.
                return True, last + " (reachable/restricted)"
        except Exception as exc:
            last = f"{type(exc).__name__}: {exc}"
        if n + 1 < attempts:
            time.sleep(2)
    return False, last or "unknown error"

failures: list[str] = []
warnings: list[str] = []

print("CORE")
for item in REG.get("core", []):
    ok, detail = probe(item["url"])
    print(f"- {item['id']}: {'OK' if ok else 'FAIL'} — {detail}")
    if not ok:
        failures.append(item["id"])

print("\nOPTIONAL MCP / PyPI")
for item in REG.get("optional_mcp", []):
    pkg = item.get("id")
    url = f"https://pypi.org/pypi/{pkg}/json"
    ok, detail = probe(url)
    print(f"- {pkg}: {'OK' if ok else 'WARN'} — {detail}")
    if not ok:
        warnings.append(pkg)

print("\nCONDITIONAL")
for item in REG.get("conditional", []):
    url = item.get("url")
    if not url:
        continue
    ok, detail = probe(url)
    print(f"- {item['id']}: {'OK' if ok else 'WARN'} — {detail}")
    if not ok:
        warnings.append(item["id"])

if warnings:
    print("\nWarnings (non-core): " + ", ".join(warnings))

if failures:
    print("\nCORE SOURCE HEALTH FAILED: " + ", ".join(failures))
    sys.exit(1)

print("\nSOURCE HEALTH PASS")
