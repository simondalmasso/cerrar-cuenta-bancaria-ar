# Executive audit

**Audit date:** 2026-10-02  
**Manifest version:** 1.2.0-dev (unreleased)  
**Jurisdiction:** Argentina  
**Primary subject:** personas humanas / usuarios de servicios financieros  
**Core runtime dependencies:** 0  
**Bank-operation capability:** intentionally none

## Executive summary

`cerrar-cuenta-bancaria-ar` is a vendor-neutral Agent Skill that guides a human through bank-account closure in Argentina. Its architecture is intentionally asymmetric:

```
official source → AI analysis → human instruction
                         X
             authenticated bank operation
```

The project is designed to remain useful with only `SKILL.md`, its local references and public official sources. External MCP/API/browser tooling is optional and must fail open to the official-source path, never to autonomous banking.

## What is controlled

- source hierarchy: BCRA / Argentina.gob.ar / official bank / official case-law;
- evidence classes: FACT / BANK_CLAIM / USER_CLAIM / INFERENCE / OPEN_GAP;
- account-type branching, including current-account debt and cheque branches;
- economic decomposition of balance, interest, taxes and residual charges;
- escalation ladder and evidence preservation;
- prompt-injection boundary for web/PDF/MCP content;
- no secrets and no authenticated banking;
- pinned optional PyPI MCP artifacts with recorded SHA-256, dependency metadata and yanked-state checks;
- installer-origin, dirty-tree, local-ahead/divergence, branch-state and malicious-upstream regression tests;
- GitHub Actions pinned by immutable SHA;
- 43 adversarial scenario specifications separated from behavioral execution;
- verified case-law registry limited to official judiciary publications, with explicit relevance and limits per precedent;
- presentation/research navigation that separates authority from discovery tooling;
- machine-readable A–G handoff plus FAST/LIVE/FORENSIC response modes;
- special-case routing and post-close monitoring kept outside the normal tree;
- legal source drift monitoring with explicit `LEGAL_REAUDIT_REQUIRED` triggers;
- synthetic-only examples and optional bank-profile schema without hardcoded bank protagonists.

## What is deliberately not claimed

- no guarantee that a bank will close an account;
- no legal advice or professional representation;
- no certification that a legal text remains substantively current merely because its URL/content marker is reachable;
- no executed cross-model behavioral certification;
- no autonomous complaint submission;
- no home-banking automation.

## Zero-cost policy

Core operation costs **USD 0** and requires no hosted service.

Optional integrations are admitted only if:
1. core still works without them;
2. their cost/free-tier status is explicit;
3. they are read-only for this workflow;
4. failure degrades to official sources;
5. they do not introduce bank credentials.

The full candidate review is in [TOOLING-AUDIT.md](TOOLING-AUDIT.md).

## External tools accepted as optional

- OpenArg MCP — conditional free tier, public-data discovery only;
- Vigía/OpenArg — free public regulatory discovery, primary-source verification required;
- Crawl4AI — optional local public-web extraction;
- Scrapy — optional local static crawling;
- Playwright — optional local rendering for public JS pages only.

None is installed or required by this repository.

## Legal posture

The repository carries MIT licensing plus a separate [legal disclaimer](../DISCLAIMER.md). The disclaimer expressly states that this is not legal/financial advice, does not create representation, does not guarantee outcomes, and does not purport to waive non-waivable legal rights or liabilities.

## Assurance evidence

Automated checks cover:

- repository structure and local links;
- JSON/provenance registry invariants;
- accidental secrets;
- `SKILL.md` literal-escape regression;
- installer foreign-origin rejection;
- malicious branch-upstream rejection;
- core source transport/content identity;
- pinned PyPI metadata and artifact SHA-256.

Behavioral evals remain **specifications** until run by a particular model/host.

## Residual risks / next hardening

Current release blockers / residuals:

1. **Behavioral evals reales todavía no ejecutados** en un host/modelo; el repo ya incluye contrato de evidencia y verificador, pero no finge un PASS.
2. tag + GitHub Release inmutables pendientes hasta que el behavioral gate pase.
3. continued review of third-party free-tier/license drift.

## Release gate

A release candidate should not be called green unless:

- `validate-skill` passes on the exact HEAD;
- `source-integrity` passes on the source/registry version being released;
- no core legal claim is based only on a secondary source;
- no required dependency has a monetary cost;
- `DISCLAIMER.md`, `SECURITY.md`, `LICENSE` and `CHANGELOG.md` are present;
- legal claims embedded in evals are re-verified whenever `references/sources-ar.md` changes;
- installer dirty-tree and local-ahead/trojan regressions are green on Bash and PowerShell;
- any external auditor findings classified P0/P1 are resolved, not merely hidden by documentation;
- `registry/release-gate.json` marks all release-critical gates PASS;
- the release commit uses a consistent manifest/eval/README version and receives an immutable tag.
