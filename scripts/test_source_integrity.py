#!/usr/bin/env python3
"""Network-free regression tests for case-law payload verification."""
from integrity_utils import sha256_hex, verify_case_law_payload

pdf = b"%PDF-1.7\nsynthetic legal fixture\n%%EOF"
good = sha256_hex(pdf)

ok, reason = verify_case_law_payload(
    pdf,
    "application/pdf",
    expected_sha256=good,
    markers_any=["irrelevant"],
)
assert ok and reason.startswith("pdf_sha256_match:"), (ok, reason)

ok, reason = verify_case_law_payload(
    pdf,
    "application/pdf",
    expected_sha256="0" * 64,
)
assert not ok and reason.startswith("pdf_sha256_mismatch:"), (ok, reason)

ok, reason = verify_case_law_payload(pdf, "application/pdf")
assert not ok and reason == "pdf_sha256_missing", (ok, reason)

html = "<html><body>Causa 123 — Banco Ejemplo</body></html>".encode()
ok, reason = verify_case_law_payload(
    html,
    "text/html; charset=utf-8",
    markers_any=["Causa 123", "Otro marcador"],
)
assert ok and reason == "text_identity_marker_match", (ok, reason)

ok, reason = verify_case_law_payload(
    html,
    "text/html",
    markers_any=["No existe"],
)
assert not ok and reason == "text_identity_marker_missing", (ok, reason)

print("SOURCE INTEGRITY UNIT TESTS PASS")
print("- PDF requires pinned SHA-256")
print("- wrong PDF hash is rejected")
print("- text identity requires a configured marker")
