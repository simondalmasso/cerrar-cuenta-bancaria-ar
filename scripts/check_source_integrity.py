#!/usr/bin/env python3
"""Public-source integrity/provenance checks.

This is NOT a legal-freshness or legal-validity certifier.
It checks transport/content identity for CORE sources and immutable
package metadata/artifact hashes for pinned optional PyPI integrations.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = json.loads((ROOT / "registry/sources.json").read_text(encoding="utf-8"))
UA = "cerrar-cuenta-bancaria-ar-source-integrity/1.1.1 (+https://github.com/simondalmasso/cerrar-cuenta-bancaria-ar)"

FAILURES: list[str] = []
WARNINGS: list[str] = []

def request(url: str, *, max_bytes: int = 262144, accept: str = "*/*"):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            status = int(getattr(r, "status", 200))
            body = r.read(max_bytes)
            return status, r.geturl(), dict(r.headers.items()), body
    except urllib.error.HTTPError as exc:
        body = exc.read(max_bytes) if exc.fp else b""
        return int(exc.code), exc.geturl(), dict(exc.headers.items()) if exc.headers else {}, body

def lower_header(headers: dict[str, str], key: str) -> str:
    for k, v in headers.items():
        if k.lower() == key.lower():
            return str(v)
    return ""

def normalize_repo_url(url: str) -> str:
    u = url.strip().lower().rstrip("/")
    return u[:-4] if u.endswith(".git") else u

print("CORE SOURCE INTEGRITY")
for item in REG.get("core", []):
    try:
        status, final_url, headers, body = request(item["url"])
        reasons: list[str] = []
        if not 200 <= status < 300:
            reasons.append(f"HTTP {status} (CORE requires 2xx)")
        parsed = urllib.parse.urlparse(final_url)
        allowed_hosts = {h.lower() for h in item.get("allowed_final_hosts", [])}
        if allowed_hosts and (parsed.hostname or "").lower() not in allowed_hosts:
            reasons.append(f"unexpected final host: {parsed.hostname}")
        path_marker = item.get("expected_path_contains")
        if path_marker and path_marker.lower() not in parsed.path.lower():
            reasons.append(f"unexpected final path: {parsed.path}")
        ctype = lower_header(headers, "Content-Type").split(";", 1)[0].strip().lower()
        prefixes = [x.lower() for x in item.get("content_type_prefixes", [])]
        if prefixes and not any(ctype.startswith(x) for x in prefixes):
            reasons.append(f"unexpected Content-Type: {ctype or '<missing>'}")
        text = body.decode("utf-8", errors="ignore").lower()
        if body.startswith(b"%PDF"):
            text = "%pdf\n" + text
        markers = [m.lower() for m in item.get("body_markers_any", [])]
        if markers and not any(m in text for m in markers):
            reasons.append("expected content marker not found")
        if reasons:
            FAILURES.append(item["id"])
            print(f"- {item['id']}: FAIL — " + "; ".join(reasons))
        else:
            print(f"- {item['id']}: OK — HTTP {status}, {ctype}, {final_url}")
    except Exception as exc:
        FAILURES.append(item["id"])
        print(f"- {item['id']}: FAIL — {type(exc).__name__}: {exc}")

print("\nPINNED OPTIONAL PYPI PROVENANCE")
for item in REG.get("optional_mcp", []):
    pkg = item["id"]
    version = item["pinned_version"]
    try:
        latest_status, _, _, latest_body = request(f"https://pypi.org/pypi/{pkg}/json", max_bytes=1024*1024, accept="application/json")
        if latest_status == 200:
            latest = json.loads(latest_body.decode("utf-8"))["info"].get("version")
            if latest and latest != version:
                WARNINGS.append(f"{pkg}: newer PyPI version {latest} exists; pin remains {version}")

        status, _, _, body = request(f"https://pypi.org/pypi/{pkg}/{version}/json", max_bytes=1024*1024, accept="application/json")
        if status != 200:
            raise RuntimeError(f"pinned PyPI metadata returned HTTP {status}")
        data = json.loads(body.decode("utf-8"))
        info = data.get("info", {})
        mismatches: list[str] = []

        if info.get("version") != version:
            mismatches.append(f"version {info.get('version')!r} != {version!r}")

        actual_license = info.get("license_expression") or info.get("license")
        if actual_license != item.get("license_expression"):
            mismatches.append(f"license {actual_license!r} != {item.get('license_expression')!r}")

        if info.get("requires_python") != item.get("requires_python"):
            mismatches.append(f"requires_python {info.get('requires_python')!r} != {item.get('requires_python')!r}")

        project_urls = info.get("project_urls") or {}
        repo_url = project_urls.get("Repository") or project_urls.get("Source") or project_urls.get("Homepage")
        if not repo_url:
            mismatches.append("source URL missing from PyPI metadata")
        elif normalize_repo_url(repo_url) != normalize_repo_url(item["source_repo_url"]):
            mismatches.append(f"source URL {repo_url!r} != {item['source_repo_url']!r}")

        actual_deps = sorted(info.get("requires_dist") or [])
        expected_deps = sorted(item.get("requires_dist") or [])
        if actual_deps != expected_deps:
            mismatches.append(f"requires_dist {actual_deps!r} != {expected_deps!r}")

        actual = {
            (u.get("filename"), u.get("packagetype")): {
                "sha256": (u.get("digests") or {}).get("sha256"),
                "yanked": bool(u.get("yanked")),
                "yanked_reason": u.get("yanked_reason"),
            }
            for u in data.get("urls", [])
        }
        for expected in item.get("artifacts", []):
            key = (expected["filename"], expected["packagetype"])
            got = actual.get(key)
            if not got:
                mismatches.append(f"missing pinned artifact: {expected['filename']}")
                continue
            if got["sha256"] != expected["sha256"]:
                mismatches.append(f"sha256 mismatch for {expected['filename']}: {got['sha256']!r}")
            if got["yanked"]:
                reason = got["yanked_reason"] or "no reason supplied"
                mismatches.append(f"artifact yanked: {expected['filename']} ({reason})")

        src_status, _, _, _ = request(item["source_repo_url"], max_bytes=4096, accept="text/html")
        expected_src = item.get("source_repo_status")
        if expected_src == "unavailable_404" and src_status != 404:
            WARNINGS.append(f"{pkg}: source repo status changed from expected 404 to HTTP {src_status}; re-audit provenance")
        elif expected_src == "available" and not 200 <= src_status < 300:
            WARNINGS.append(f"{pkg}: source repo expected available, got HTTP {src_status}")

        if mismatches:
            FAILURES.append(pkg)
            print(f"- {pkg}=={version}: FAIL — " + "; ".join(mismatches))
        else:
            print(f"- {pkg}=={version}: OK — metadata + dependency set + artifact SHA-256/yanked state match; source repo HTTP {src_status}")
    except Exception as exc:
        FAILURES.append(pkg)
        print(f"- {pkg}=={version}: FAIL — {type(exc).__name__}: {exc}")

print("\nCONDITIONAL SOURCE AVAILABILITY (NON-BLOCKING)")
for item in REG.get("conditional", []):
    url = item.get("url")
    if not url:
        continue
    try:
        status, final_url, _, _ = request(url, max_bytes=4096)
        ok = 200 <= status < 400
        print(f"- {item['id']}: {'OK' if ok else 'WARN'} — HTTP {status}, {final_url}")
        if not ok:
            WARNINGS.append(f"{item['id']}: HTTP {status}")
    except Exception as exc:
        WARNINGS.append(f"{item['id']}: {type(exc).__name__}: {exc}")
        print(f"- {item['id']}: WARN — {type(exc).__name__}: {exc}")

if WARNINGS:
    print("\nWARNINGS")
    for warning in WARNINGS:
        print(f"- {warning}")

if FAILURES:
    print("\nSOURCE INTEGRITY FAILED: " + ", ".join(FAILURES))
    sys.exit(1)

print("\nSOURCE INTEGRITY PASS")
print("NOTE: this validates availability/provenance/content markers, not legal freshness or legal interpretation.")
