#!/usr/bin/env python3
"""Public-source integrity/provenance checks.

This is NOT a legal-freshness or legal-validity certifier.
It checks transport/content identity for CORE sources, emits explicit
LEGAL_REAUDIT_REQUIRED findings on watched legal-source drift, verifies
official case-law endpoints, and validates immutable package metadata/artifact
hashes for pinned optional PyPI integrations. Any legal re-audit trigger exits
non-zero so CI cannot report a green integrity gate until it is reviewed.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

from integrity_utils import verify_case_law_payload

ROOT = Path(__file__).resolve().parents[1]
REG = json.loads((ROOT / "registry/sources.json").read_text(encoding="utf-8"))
WATCH = json.loads((ROOT / "registry/legal-watch.json").read_text(encoding="utf-8"))
WATCH_BY_ID = {item["source_id"]: item for item in WATCH.get("sources", [])}
CASE_LAW = json.loads((ROOT / "registry/case-law.json").read_text(encoding="utf-8"))
UA = "cerrar-cuenta-bancaria-ar-source-integrity/1.2.0-dev (+https://github.com/simondalmasso/cerrar-cuenta-bancaria-ar)"

FAILURES: list[str] = []
WARNINGS: list[str] = []
LEGAL_REAUDIT: list[str] = []

def request(url: str, *, max_bytes: int | None = 262144, accept: str = "*/*"):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            status = int(getattr(r, "status", 200))
            body = r.read() if max_bytes is None else r.read(max_bytes)
            return status, r.geturl(), dict(r.headers.items()), body
    except urllib.error.HTTPError as exc:
        body = exc.read() if (exc.fp and max_bytes is None) else (exc.read(max_bytes) if exc.fp else b"")
        return int(exc.code), exc.geturl(), dict(exc.headers.items()) if exc.headers else {}, body

def request_with_retry(
    url: str,
    *,
    max_bytes: int | None = 262144,
    accept: str = "*/*",
    attempts: int = 3,
):
    """Retry transient transport failures and retryable HTTP statuses.

    Identity/content mismatches are never retried here; only transport-like
    failures are. The final failure still blocks integrity.
    """
    retryable_statuses = {408, 425, 429, 500, 502, 503, 504}
    last_exc: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            result = request(url, max_bytes=max_bytes, accept=accept)
            status = result[0]
            if status not in retryable_statuses or attempt == attempts:
                return result
        except (TimeoutError, urllib.error.URLError, ConnectionError, OSError) as exc:
            last_exc = exc
            if attempt == attempts:
                raise
        time.sleep(0.75 * attempt)
    if last_exc is not None:
        raise last_exc
    raise RuntimeError("request retry loop exhausted unexpectedly")

def lower_header(headers: dict[str, str], key: str) -> str:
    for k, v in headers.items():
        if k.lower() == key.lower():
            return str(v)
    return ""


class VisibleTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts: list[str] = []
        self._skip = 0
    def handle_starttag(self, tag, attrs):
        if tag.lower() in {"script","style","noscript"}:
            self._skip += 1
    def handle_endtag(self, tag):
        if tag.lower() in {"script","style","noscript"} and self._skip:
            self._skip -= 1
    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)

def normalized_visible_text(body: bytes) -> str:
    parser = VisibleTextParser()
    parser.feed(body.decode("utf-8", errors="ignore"))
    return re.sub(r"\s+", " ", " ".join(parser.parts)).strip().lower()

def semantic_window_fingerprint(text: str, needles: list[str], radius: int = 220) -> tuple[str | None, list[str]]:
    windows = []
    missing = []
    for raw in needles:
        needle = re.sub(r"\s+", " ", raw).strip().lower()
        idx = text.find(needle)
        if idx < 0:
            missing.append(raw)
            continue
        start = max(0, idx-radius)
        end = min(len(text), idx+len(needle)+radius)
        windows.append(text[start:end])
    if missing:
        return None, missing
    joined = "\n---\n".join(windows)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest(), []

def normalize_repo_url(url: str) -> str:
    u = url.strip().lower().rstrip("/")
    return u[:-4] if u.endswith(".git") else u

def legal_reaudit(source_id: str, reason: str) -> None:
    msg = f"LEGAL_REAUDIT_REQUIRED {source_id}: {reason}"
    LEGAL_REAUDIT.append(msg)
    WARNINGS.append(msg)

print("CORE SOURCE INTEGRITY")
for item in REG.get("core", []):
    try:
        status, final_url, headers, body = request_with_retry(item["url"], max_bytes=None)
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
        text_body = body.decode("utf-8", errors="ignore").lower()
        if body.startswith(b"%PDF"):
            text_body = "%pdf\n" + text_body
        markers = [m.lower() for m in item.get("body_markers_any", [])]
        if markers and not any(m in text_body for m in markers):
            reasons.append("expected content marker not found")

        watch = WATCH_BY_ID.get(item["id"])
        if watch:
            local_claim = watch.get("local_claim", "")
            local_expected = watch.get("local_claim_sha256")
            local_observed = hashlib.sha256(local_claim.encode("utf-8")).hexdigest()
            if local_expected != local_observed:
                legal_reaudit(item["id"], f"local legal-claim fingerprint drift {local_expected!r} -> {local_observed}")

            strategy = watch.get("strategy", "availability_only")
            etag = lower_header(headers, "ETag") or None
            last_modified = lower_header(headers, "Last-Modified") or None

            if strategy == "full_content":
                remote_sha = hashlib.sha256(body).hexdigest()
                print(
                    f"  OBSERVED legal-watch {item['id']} strategy=full_content "
                    f"sha256={remote_sha} etag={etag!r} last_modified={last_modified!r} "
                    f"section={watch.get('relevant_section')!r}"
                )
                expected_sha = watch.get("expected_remote_sha256")
                if not expected_sha:
                    legal_reaudit(item["id"], f"remote SHA-256 baseline missing; observed {remote_sha}")
                elif expected_sha != remote_sha:
                    legal_reaudit(item["id"], f"remote content SHA-256 changed {expected_sha} -> {remote_sha}")

                expected_etag = watch.get("expected_etag")
                if expected_etag and etag and expected_etag != etag:
                    legal_reaudit(item["id"], f"ETag changed {expected_etag!r} -> {etag!r}")
                expected_lm = watch.get("expected_last_modified")
                if expected_lm and last_modified and expected_lm != last_modified:
                    legal_reaudit(item["id"], f"Last-Modified changed {expected_lm!r} -> {last_modified!r}")

            elif strategy == "semantic_text_windows":
                visible = normalized_visible_text(body)
                semantic_sha, missing = semantic_window_fingerprint(visible, watch.get("semantic_needles", []))
                print(
                    f"  OBSERVED legal-watch {item['id']} strategy=semantic_text_windows "
                    f"semantic_sha256={semantic_sha!r} missing={missing!r} "
                    f"section={watch.get('relevant_section')!r}"
                )
                if missing:
                    legal_reaudit(item["id"], "semantic anchors missing: " + ", ".join(missing))
                else:
                    expected_semantic = watch.get("expected_semantic_sha256")
                    if not expected_semantic:
                        legal_reaudit(item["id"], f"semantic fingerprint baseline missing; observed {semantic_sha}")
                    elif expected_semantic != semantic_sha:
                        legal_reaudit(item["id"], f"semantic text-window fingerprint changed {expected_semantic} -> {semantic_sha}")

            elif strategy == "availability_only":
                print(
                    f"  OBSERVED legal-watch {item['id']} strategy=availability_only "
                    f"etag={etag!r} last_modified={last_modified!r} "
                    f"section={watch.get('relevant_section')!r}"
                )
            else:
                reasons.append(f"unknown legal-watch strategy: {strategy!r}")

        if reasons:
            FAILURES.append(item["id"])
            print(f"- {item['id']}: FAIL — " + "; ".join(reasons))
        else:
            print(f"- {item['id']}: OK — HTTP {status}, {ctype}, {final_url}")
    except Exception as exc:
        FAILURES.append(item["id"])
        print(f"- {item['id']}: FAIL — {type(exc).__name__}: {exc}")

print("\nOFFICIAL CASE-LAW INTEGRITY")
for case in CASE_LAW.get("cases", []):
    cid = case.get("id", "<missing>")
    if case.get("status") != "VERIFIED_OFFICIAL":
        print(f"- {cid}: SKIP — status={case.get('status')!r}")
        continue
    try:
        urls = case.get("verification_urls") or [case.get("official_full_text") or case.get("official_url")]
        markers = case.get("verification_markers_any", [])
        pinned_pdf_hashes = case.get("verification_sha256_by_url", {})
        if not urls or not urls[0]:
            raise RuntimeError("no verification URL")
        matched = False
        observations: list[str] = []
        allowed_hosts = {h.lower() for h in case.get("verification_allowed_hosts", [])}
        for url in urls:
            if not url:
                continue
            status, final_url, headers, body = request_with_retry(url, max_bytes=None)
            ctype = lower_header(headers, "Content-Type").split(";", 1)[0].strip().lower()
            observations.append(f"{status} {final_url}")
            if not 200 <= status < 300:
                continue
            final_host = (urllib.parse.urlparse(final_url).hostname or "").lower()
            if allowed_hosts and final_host not in allowed_hosts:
                observations.append(f"unexpected host {final_host}")
                continue

            expected_sha = pinned_pdf_hashes.get(url) or pinned_pdf_hashes.get(final_url)
            ok, identity = verify_case_law_payload(
                body,
                ctype,
                expected_sha256=expected_sha,
                markers_any=markers,
            )
            observations.append(identity)

            if identity.startswith("pdf_sha256_mismatch:"):
                raise RuntimeError(
                    f"official case-law PDF drift for {url}: {identity}"
                )
            if ok:
                matched = True
                break

        if not matched:
            raise RuntimeError("official case-law verification failed; " + "; ".join(observations))
        print(f"- {cid}: OK — official source identity verified")
    except Exception as exc:
        FAILURES.append(cid)
        print(f"- {cid}: FAIL — {type(exc).__name__}: {exc}")

print("\nPINNED OPTIONAL PYPI PROVENANCE")
for item in REG.get("optional_mcp", []):
    pkg = item["id"]
    version = item["pinned_version"]
    try:
        latest_status, _, _, latest_body = request_with_retry(
            f"https://pypi.org/pypi/{pkg}/json",
            max_bytes=1024*1024,
            accept="application/json",
        )
        if latest_status == 200:
            latest = json.loads(latest_body.decode("utf-8"))["info"].get("version")
            if latest and latest != version:
                WARNINGS.append(f"{pkg}: newer PyPI version {latest} exists; pin remains {version}")

        status, _, _, body = request_with_retry(
            f"https://pypi.org/pypi/{pkg}/{version}/json",
            max_bytes=1024*1024,
            accept="application/json",
        )
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

        src_status, _, _, _ = request_with_retry(item["source_repo_url"], max_bytes=4096, accept="text/html")
        expected_src = item.get("source_repo_status")
        if expected_src == "unavailable_404" and src_status != 404:
            WARNINGS.append(f"{pkg}: source repo status changed from expected 404 to HTTP {src_status}; re-audit provenance")
        elif expected_src == "available" and not 200 <= src_status < 300:
            WARNINGS.append(f"{pkg}: source repo expected available, got HTTP {src_status}")

        if mismatches:
            FAILURES.append(pkg)
            print(f"- {pkg}=={version}: FAIL — " + "; ".join(mismatches))
        else:
            print(
                f"- {pkg}=={version}: OK — metadata + dependency set + "
                f"artifact SHA-256/yanked state match; source repo HTTP {src_status}"
            )
    except Exception as exc:
        FAILURES.append(pkg)
        print(f"- {pkg}=={version}: FAIL — {type(exc).__name__}: {exc}")

print("\nCONDITIONAL SOURCE AVAILABILITY (NON-BLOCKING)")
for item in REG.get("conditional", []):
    url = item.get("url")
    if not url:
        continue
    try:
        status, final_url, _, _ = request_with_retry(url, max_bytes=4096)
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

if LEGAL_REAUDIT:
    print("\nSOURCE INTEGRITY BLOCKED")
    print("LEGAL WATCH: re-audit required before merge/release.")
    print("NOTE: drift is not itself a legal conclusion; review and rebaseline only after verifying the official source.")
    sys.exit(2)

print("\nSOURCE INTEGRITY PASS")
print("LEGAL WATCH: baseline matched; no legal re-audit trigger.")
print("NOTE: this detects source drift but does not decide legal freshness or legal interpretation.")
