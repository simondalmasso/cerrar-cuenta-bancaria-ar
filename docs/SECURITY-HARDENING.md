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

## What still lives in GitHub settings

The following cannot be guaranteed by files alone:

- branch protection / repository rulesets;
- secret scanning and push protection;
- private vulnerability reporting;
- Dependabot security alerts.

For an administrator using GitHub CLI, the reviewed helper can be used as an **operator tool**:

```bash
gh extension install GitHubSecurityLab/gh-secure
gh secure status --repo simondalmasso/cerrar-cuenta-bancaria-ar
gh secure --repo simondalmasso/cerrar-cuenta-bancaria-ar --dry-run
```

Only after reviewing the dry run should an administrator choose whether to apply settings.

Current API-visible state during this audit:
- repository is public;
- no repository rulesets were returned;
- the connected GitHub integration could not read legacy branch-protection settings, so absence of branch protection is **not** inferred from that 403.

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
- repository security settings reviewed by an administrator;
- behavioral eval gate completed separately.
