#!/usr/bin/env python3
"""Pure helpers for source-integrity checks.

Stdlib-only so repository CI can regression-test payload identity without
network access.
"""
from __future__ import annotations

import hashlib


def sha256_hex(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def verify_case_law_payload(
    body: bytes,
    content_type: str,
    *,
    expected_sha256: str | None = None,
    markers_any: list[str] | tuple[str, ...] = (),
) -> tuple[bool, str]:
    """Verify a fetched official case-law payload.

    PDFs require an explicitly pinned SHA-256. HTML/text payloads require at
    least one configured identity marker. Merely being a PDF is never enough.
    """
    ctype = (content_type or "").split(";", 1)[0].strip().lower()
    is_pdf = body.startswith(b"%PDF") or ctype == "application/pdf"

    if is_pdf:
        if not expected_sha256:
            return False, "pdf_sha256_missing"
        observed = sha256_hex(body)
        if observed != expected_sha256:
            return False, f"pdf_sha256_mismatch:{observed}"
        return True, f"pdf_sha256_match:{observed}"

    markers = [str(m).strip().lower() for m in markers_any if str(m).strip()]
    if not markers:
        return False, "text_identity_markers_missing"
    text = body.decode("utf-8", errors="ignore").lower()
    if any(marker in text for marker in markers):
        return True, "text_identity_marker_match"
    return False, "text_identity_marker_missing"
