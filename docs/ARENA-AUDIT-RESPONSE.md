# Arena hostile-audit response — 2026-10-03

> **Documento histórico.** Registra el estado y los hallazgos al momento de esa auditoría; no representa el estado actual del candidato. Para el estado vigente usar [registry/release-gate.json](../registry/release-gate.json) y [RELEASE-GATE.md](RELEASE-GATE.md).

External audit target: `7319259bb4fc7a1281d752dea590f237cacac11e`.

This response does **not** accept findings by severity label alone. Each claim was checked against the audited tree and, where needed, against the official source.

## Disposition

| Finding | Disposition | Result |
|---|---|---|
| P0-001 behavioral evals NOT_RUN | **CONFIRMED / OPEN** | Stable release remains blocked. No fake run was created. |
| P0-002 legal drift only warned | **CONFIRMED / FIXED** | `LEGAL_REAUDIT_REQUIRED` now exits non-zero and blocks source-integrity until reviewed. |
| P0-003 general guide vs specific BCRA unresolved | **FALSE POSITIVE / HARDENED** | Precedence already existed in `sources-ar.md`, `decision-tree.md`, S2 and S26. It is now explicit in always-loaded `SKILL.md` and enforced structurally. |
| P0-004 Schvind / JURISTECA 55539 nonexistent | **FALSE POSITIVE** | Official JURISTECA ID 55539 and full-text PDF exist. Live official case-law identity checks were added. |
| P1-001 installer accepts malicious fork / needs fixed SHA | **FALSE POSITIVE** | Installer requires canonical owner/repo origin, rejects foreign origin, dirty/ahead/diverged/detached states and lands exactly on verified `origin/main`. A fixed SHA would defeat legitimate updater semantics; stable release immutability is handled by tag/release gate. |
| P1-002 binaries not scanned | **ACCEPTED, DIFFERENT FIX** | Repository now rejects unknown/binary **tracked** content instead of pretending regex secret scanning detects malware in binaries. |
| P1-003 Actions can escalate despite permissions | **OVERSTATED / HARDENED** | Token capabilities remain bounded by declared workflow permissions. Validator now additionally permits write scope only for CodeQL `security-events: write`; other workflows may not request write scopes. |
| P1-004 prompt-injection coverage narrow | **CONFIRMED / FIXED** | Added PDF, email, screenshot, malicious-link and evidence-exfiltration attacks. |
| P1-005 G requires every linked product closed | **FALSE POSITIVE / CLARIFIED** | G applies to the target product. Linked products may legitimately remain open if separately documented; post-close text now makes that explicit. |
| P2-001 sources not checked live | **ALREADY CONTROLLED** | Core sources are checked live by source-integrity and material legal claims require live verification when available. |
| P2-002 precedent could be used as norm | **ALREADY CONTROLLED / HARDENED** | SKILL and jurisprudence guide already forbid it; two additional precedent-misuse evals were added. |
| P2-004 critical external links not checked | **PARTLY TRUE / FIXED FOR AUTHORITY LINKS** | Core legal sources and verified case-law endpoints are now live-checked. Generic documentation links are not promoted to legal release gates. |

## Behavioral status at audit time

At the time of this audit, the remaining material blocker was:

```
behavioral-evals = NOT_RUN
immutable-release = PENDING
```

This paragraph is historical. Current release status is maintained only in [registry/release-gate.json](../registry/release-gate.json).

## Jurisprudence correction

The audit claim that **Schvind Myriam Inés c/ Compañía Financiera Argentina S.A.** did not exist was independently rechecked. The official JURISTECA publication identifies:

- Fallo ID 55539;
- Causa 234535-2021-0;
- Sala II;
- 14/03/2024;
- official full-text PDF under JURISTECA.

The repository therefore keeps the precedent and adds machine-checkable official-host/identity metadata instead of deleting a real case.
