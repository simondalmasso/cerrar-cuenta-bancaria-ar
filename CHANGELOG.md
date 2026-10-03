# Changelog

## 1.2.0-dev — Unreleased

- hardened both installers against dirty trees, detached/non-main checkouts and local-ahead/diverged commits before validator execution;
- added real-Git adversarial installer regression tests, including dirty-tree and trojan-commit cases plus legitimate stale fast-forward;
- renamed the source-health file family consistently to source-integrity;
- added PyPI yanked detection and requires_dist provenance checks;
- documented that uvx top-level pins do not hash-pin transitive dependencies;
- fixed privacy wording so full DNI/CBU/account/card identifiers are explicitly hidden, not ambiguously “redacted”;
- expanded adversarial specifications from 22 to 31, covering the nine PARTIAL scenarios from the hostile audit;
- added currency/multi-currency intake and compensated-balance handling;
- tightened Agent Skill activation metadata and restored the BCRA single-act wording in the always-loaded summary;
- centralized the BCRA second-instance wait period in references/sources-ar.md;
- marked the manifest as unreleased development state; no tag/release is created by this hardening branch;
- added an official-source jurisprudence dossier and machine-readable case-law registry;
- added two jurisprudence-backed dispute specs for post-closure charges/credit reporting and undocumented telephone cancellation;
- added a presentation-ready one-hour review path and a research-stack policy separating discovery from authority;
- added machine-readable A–G handoff schema and FAST/LIVE/FORENSIC response modes;
- clarified unrecorded bank-call recollections without expanding the five-class evidence ontology;
- added special-case branches for cotitulars, powers, death, minors, judicial measures and residence abroad;
- added a post-close verification/monitoring protocol;
- added semantic legal-source drift monitoring with `LEGAL_REAUDIT_REQUIRED`;
- expanded adversarial specifications to 45;
- added a real behavioral-eval evidence contract and explicit BLOCKED release gate until such runs exist;
- added synthetic-only workflow examples and an optional bank-profile schema while keeping the core bank-neutral;
- reviewed Prism Legal OS and adopted only its reusable-review-playbook concept: independently implemented stage-gate checks, no Prism code/runtime dependency, no legal compliance score;
- reviewed GitHub Security Lab `gh-secure`; added Dependabot for Actions, pinned CodeQL scanning, immutable-Action validation, and repository-security guidance;
- registered Strix as optional external security assurance only, with explicit-authorization/credit safeguards;
- Arena hostile-audit follow-up: made legal drift blocking, added live official case-law identity checks, expanded prompt-injection/precedent-misuse specs to 52, enforced text-only tracked content, and tightened workflow write-permission policy;
- Gemini hostile-audit follow-up: replaced permissive PDF-presence acceptance with pinned SHA-256 identity, bound handoffs to privacy-safe product refs, enforced strict UTF-8 regular tracked files, and expanded adversarial specs to 54;
- reviewed `cc-thinking-skills`, Agent-Reach, last30days, InsForge, Decision 2.0, Cloudflare `security-audit-skill`, and Agent Beacon; adopted only Cloudflare's independent-verification/coverage-led audit methodology conceptually, with no new runtime dependency or mandatory cost;
- added bounded retries for transient source-integrity transport failures after a real CSJN timeout on main, while keeping final failures and identity/content mismatches release-blocking.

## Earlier unreleased external-audit preparation

- added prominent legal/disclaimer layer without attempting to waive non-waivable rights;
- added executive audit and zero-cost tooling review;
- reviewed the supplied runtime/browser/research candidates and kept the core dependency-free;
- accepted Crawl4AI, Scrapy and Playwright only as optional public read-only transport/rendering adapters;
- added OpenArg MCP and Vigía/OpenArg as optional Argentine discovery sources with primary-source verification requirements;
- added machine-readable zero-cost tooling policy.


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