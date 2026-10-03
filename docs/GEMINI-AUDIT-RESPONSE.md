# Gemini hostile-audit response — 2026-10-03

> **Documento histórico.** Registra el estado y los hallazgos al momento de esa auditoría; no representa el estado actual del candidato. Para el estado vigente usar [registry/release-gate.json](../registry/release-gate.json) y [RELEASE-GATE.md](RELEASE-GATE.md).

External audit target: `e2c409e3a57a3158e4b4e82d5d63cf4a8965ec72`.

The review was useful, but findings were rechecked before implementation. Severity labels were not treated as evidence.

## Disposition

| Finding | Disposition | Result |
|---|---|---|
| behavioral evals still NOT_RUN | **CONFIRMED / OPEN** | Stable release remains blocked. |
| official case-law PDF accepted on presence only | **CONFIRMED / FIXED** | Historical official PDFs now require pinned SHA-256 identity; a 200 PDF is insufficient. |
| current-account debtor-balance rule wrong | **REJECTED** | Current skill already distinguishes debtor balance and does not promise mandatory remote closure. |
| repo still uses 20 business days | **REJECTED** | Current baseline uses 10 business days for BCRA second-instance timing. |
| tracked text-only policy can be bypassed | **PARTLY CONFIRMED / HARDENED** | Validator now rejects non-regular git modes, unknown tracked formats, NUL/binary content, non-UTF-8 and forbidden control characters. |
| installer accepts attacker fork | **REJECTED** | Canonical owner/repo origin + clean/branch/ancestry/exact-origin-main checks already reject that path. |
| G state can lose target-product identity | **CONFIRMED / FIXED** | Handoffs now require opaque local `target_product_ref` plus `related_products[]`; G may not leave related products unknown. |
| punitive-damages precedent can be overread | **HARDENING ACCEPTED** | Jurisprudence guide and new adversarial scenario state that punitive damages are judicial, fact-dependent and never automatic. |
| version metadata inconsistent | **REJECTED** | Current release remains consistently `1.2.0-dev` / unreleased. |

## Additional hardening from the review

- behavioral-run evidence is bound to the candidate commit by default;
- response text must be non-empty;
- behavioral schema is stricter and now covers 54 scenarios;
- source-integrity identity logic has network-free unit regressions;
- the case-state handoff uses privacy-safe local product refs instead of banking identifiers.

## Estado de release en el momento de esa auditoría

At the time of that audit, this work did **not** turn the project into a stable release. The then-open gates were:

- repository-security administrator review: pending at that time;
- behavioral evals: NOT_RUN at that time;
- immutable `v1.2.0` tag/release: pending at that time.

Current status is intentionally not duplicated here; use the release-gate files linked above.
