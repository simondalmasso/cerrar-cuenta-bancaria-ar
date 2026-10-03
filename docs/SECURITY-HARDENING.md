# Security hardening

This repository keeps banking operations out of scope, but the repository itself still needs software-supply-chain protection.

## Baseline adopted from GitHub Security Lab guidance

The project reviewed `GitHubSecurityLab/gh-secure` at commit
`a04d1c144f5d1b63a8aa5cd7946e8ceafa709a2a`.

Useful controls from that project:

1. branch protection / rulesets;
2. private vulnerability reporting;
3. secret scanning with push protection;
4. Dependabot;
5. CodeQL code scanning.

The tool itself is **not** a runtime dependency of this skill.

## What is enforced in this repository

Repository-controlled configuration now includes:

- `.github/dependabot.yml` for GitHub Actions update PRs;
- `.github/workflows/security-codeql.yml` for Python CodeQL;
- immutable commit SHAs for third-party GitHub Actions;
- `persist-credentials: false` on checkout;
- local secret-pattern scanning in `scripts/validate_repo.py`;
- installer red-team regression tests;
- provenance checks for optional PyPI artifacts.

## GitHub settings — verified active

Administrator review completed on **2026-10-03**.

Verified repository settings:

- active ruleset [**24426791 — Protect main**](https://github.com/simondalmasso/cerrar-cuenta-bancaria-ar/rules/24426791) targeting `refs/heads/main`;
- branch deletion blocked;
- non-fast-forward updates blocked;
- changes to `main` require a pull request;
- required status check: `validate`;
- secret scanning: **enabled**;
- push protection: **enabled**;
- private vulnerability reporting: **enabled**;
- Dependabot security updates: **enabled**.

These controls live in GitHub settings rather than in the repository tree, so the evidence is recorded in `registry/release-gate.json`.

For an administrator using GitHub CLI, the reviewed helper can still be used as an **operator tool**:

```bash
gh extension install GitHubSecurityLab/gh-secure
gh secure status --repo simondalmasso/cerrar-cuenta-bancaria-ar
gh secure --repo simondalmasso/cerrar-cuenta-bancaria-ar --dry-run
```

Only after reviewing the dry run should an administrator choose whether to apply settings.

Current administrator-verified state:
- repository is public;
- ruleset `24426791` is active on `main`;
- secret scanning and push protection are enabled;
- private vulnerability reporting is enabled;
- Dependabot security updates are enabled.

## Strix

Strix can add independent code-review, supply-chain and penetration-testing assurance, but scans may consume credits and contact authorized targets.

Policy for this project:

- optional external assurance only;
- repository/code scope only unless separately authorized;
- never use bank credentials, banking sessions or customer evidence;
- do not launch a paid/credit-consuming scan without explicit approval;
- findings are evidence, not proof that the legal guidance is correct.

A Strix connection was requested during the audit, but authorization was not granted in-session; therefore no Strix scan result is claimed.

## Other host plugins

General coding/research/browser plugins may help the operator, but they are not dependencies of this repository. In particular, browser-capable tooling must remain subject to the existing rule: public read-only research only, never authenticated banking.

## Release gate

A stable release should require:

- normal CI PASS;
- CodeQL workflow PASS for the candidate commit or a documented reason it was not applicable;
- no known committed secret;
- repository security settings reviewed by an administrator — **PASS 2026-10-03**;
- behavioral eval gate completed separately.


## External audit evidence policy

The project also reviewed Cloudflare's `security-audit-skill` methodology. It is not installed or required.

For future hostile audits, use this lightweight verdict discipline:

- **CONFIRMED** — reproduced or directly established from current source/evidence;
- **NEEDS_VALIDATION** — source-grounded concern with one decisive unresolved fact;
- **REJECTED** — disproved by current source, test, or authoritative evidence.

A severity label from an external model is not evidence. Findings should be independently re-read and, when safe, reproduced before becoming release blockers. Defense-in-depth wishes that do not cross a real trust boundary remain hardening notes, not vulnerabilities.

This policy is intentionally smaller than Cloudflare's full multi-agent workflow: no Node validator, no mandatory sub-agents, and no sandboxed target execution are added to the bank skill.
