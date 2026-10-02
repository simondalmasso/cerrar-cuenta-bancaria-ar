# Changelog

## 1.1.1 — 2026-10-02

- pinned optional PyPI MCP integrations and recorded wheel/sdist SHA-256 provenance;
- downgraded unavailable-source MCPs to OPTIONAL_PYPI / provenance_limited;
- hardened source checks: CORE 2xx, final host/path, Content-Type and content marker;
- added PyPI metadata/hash verification and explicit legal-freshness disclaimer;
- guarded installers against updating unrelated Git repositories by verifying origin;
- added explicit prompt-injection boundary for web/PDF/MCP content;
- added two prompt-injection adversarial specifications (22 total);
- upgraded eval validation from count-only to structural checks and clarified they are specifications, not executed model tests;
- pinned GitHub Actions by immutable commit SHA and disabled checkout credential persistence;
- added optional `agents/openai.yaml` presentation metadata;
- clarified that public bank pages may be researched read-only while authenticated surfaces remain prohibited;
- forced installer pulls from the verified `origin main`, ignoring a malicious branch upstream;
- fixed the literal `\\n9.` regression in `SKILL.md` and added validator/CI coverage.


## 1.1.0 — 2026-10-02

- narrowed core scope to personal accounts/personas humanas;
- added bank-specific research protocol without hardcoded menus;
- added economic/blocker classification;
- audited legal research integrations and free/free-tier boundaries;
- added cross-agent install scripts;
- added repository validator and CI;
- expanded eval suite from 10 to 20 scenarios;
- added security and contribution policy.

## 1.0.0 — 2026-10-02

- initial vendor-neutral Agent Skill;
- BCRA/Argentina official-source hierarchy;
- evidence model and escalation ladder;
- optional Argentine legal MCP integrations.