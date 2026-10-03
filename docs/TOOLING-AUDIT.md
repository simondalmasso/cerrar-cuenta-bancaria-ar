# Tooling audit — zero-cost / scope review

**Date:** 2026-10-03  
**Rule:** no candidate becomes a required dependency. "Accepted" means optional capability only.

The supplied list contained duplicates; each unique project/service was reviewed once.

| Candidate | Cost/license snapshot | Relevance | Decision |
|---|---|---|---|
| OpenArg / OpenArg MCP | hosted free quota; public Argentine datasets; key required for MCP | useful for locating BCRA/public datasets | **ACCEPT conditional** — discovery only |
| Vigía / OpenArg | public search/feed; MIT repo | highly relevant regulatory discovery incl. BCRA communications | **ACCEPT optional** — verify primary source |
| jslinux/jslinux | no recognized license in repo metadata; last push 2016 | browser Linux demo | REJECT |
| WebVM / leaningtech/webvm | repo Apache-2.0; public CheerpX deployment has usage/license limits for organizations | browser VM | REJECT — no need, licensing caveat |
| WebContainers | free for many uses; commercial API conditions exist | in-browser Node runtime | REJECT — no runtime needed |
| CheerpJ | enterprise Java-in-browser product; licensing not a zero-cost general guarantee | Java runtime | REJECT |
| Puter / HeyPuter/puter | AGPL self-host; hosted model is user-pays/free allowance | cloud OS/runtime | REJECT — unnecessary auth/runtime layer |
| copy/v86 | BSD-2-Clause | x86 browser VM | REJECT — unrelated |
| nodeterm | BUSL-1.1, rolling MIT conversion; Pro features | agent terminal canvas | REJECT — not pure permissive/irrelevant |
| codeswithdev/DEV-OS | MIT | bare-metal OS | REJECT — unrelated |
| dame.dev | could not be reliably verified during audit | unknown | REJECT/UNVERIFIED |
| Railway free VM | anonymous 60-minute VM; free plan credit is limited | ephemeral compute | REJECT — not durable/core-free |
| firecrawl/firecrawl | AGPL-3.0; self-host possible; hosted service exists | web extraction | REJECT — heavy/redundant/licensing surface |
| unclecode/crawl4ai | Apache-2.0; active | LLM-oriented public web extraction | **ACCEPT optional local** |
| assafelovic/gpt-researcher | Apache-2.0; active | autonomous research orchestration | REJECT — duplicates host and may need paid model/search |
| browser-use/browser-use | MIT; active | browser agent/actions | REJECT — action surface conflicts with safety model |
| bytedance/deer-flow | MIT; active | long-horizon agent harness | REJECT — massive scope/duplicate orchestrator |
| D4Vinci/Scrapling | BSD-3-Clause; active | scraping | REJECT — redundant with simpler accepted adapters |
| scrapy/scrapy | BSD-3-Clause; active | deterministic crawling | **ACCEPT optional local** |
| stanford-oval/storm | MIT | LLM research/report generation | REJECT — duplicate research stack/model dependency |
| smicallef/spiderfoot | MIT | OSINT/attack-surface intelligence | REJECT — unrelated |
| microsoft/playwright | Apache-2.0; active | JS rendering/testing | **ACCEPT optional local, public read-only only** |
| NikolaiT/GoogleScraper | Apache-2.0; last push 2021 | search-engine scraping | REJECT — stale/fragile/unnecessary |
| Ryze-AI-Adgent/open-seo-mcp-skills | MIT skills; connector/data-account dependencies | SEO | REJECT — unrelated |
| Panniantong/Agent-Reach | MIT; broad web/social capability; some channels use sessions/cookies/proxies | general web reach | REJECT — authenticated/session scope exceeds this skill |
| citrolabs/ego-lite | MIT; shares real browser logins/cookies with agents | browser automation | **REJECT HARD** — directly conflicts with authenticated-browser prohibition |
| skydive-project/skydive | Apache-2.0 | network topology/protocol analyzer | REJECT — unrelated |
| h4ckf0r0day/obscura | Apache-2.0; active | headless browser for agents/scraping | REJECT — action/browser surface unnecessary |
| watercrawl/WaterCrawl | custom "MIT + restrictions" license; heavy self-host stack | crawling/search | REJECT — custom license + operational weight |
| browser-use/jev-ultrafast | MIT; active | web agent | REJECT — autonomous browser layer |
| TheoLeeCJ/SemIf-OpenJev | MIT | local semantic decision/reranker | REJECT — unrelated decision layer |
| browserbase/stagehand | MIT SDK; local use possible; model/browser cloud may introduce cost | extract + browser actions | REJECT — action surface/model dependency |
| caiiiycuk/emulators / js-dos | GPL-2.0 for emulators repo; browser DOS/Win9x runtime | emulation | REJECT — unrelated |
| gh-secure | MIT; GitHub Security Lab; free security features for public OSS | branch protection/PVR/secret scanning/Dependabot/CodeQL setup | **ACCEPT optional operator tool** — dry-run first; not runtime |
| Strix | hosted/self-hosted security platform; scans may consume credits | code review, supply-chain and pentest assurance | **ACCEPT conditional** — explicit authorization before scans; repo scope only; never banking credentials |
| Prism Legal OS | AGPL-3.0-only; Node 22 + PostgreSQL + Qdrant/object storage; AI features require configured provider and indexed search uses OpenAI | useful ideas: reusable review rulebooks, source-grounded review, saved checkpoints | **ADOPT CONCEPT ONLY** — no code/runtime dependency; independently implement a minimal case-review playbook |
| tjboudreaux/cc-thinking-skills | MIT; portable reasoning-skill catalog | useful generic red-team/map-vs-territory patterns, but overlaps with FORENSIC/review-playbook/security methodology already present | REJECT runtime — no incremental bank-domain value worth another reasoning router |
| Panniantong/Agent-Reach | MIT; Python 3.10+; many channels use cookies, logged-in browser sessions, proxies or external CLIs | broad internet reach | **REJECT HARD for bank skill** — authenticated/session reuse directly conflicts with public-read-only boundary |
| mvanhorn/last30days-skill | MIT; Python 3.12; social/news recency engine, some sources need auth/keys/browser sessions | trend/recent-discussion research | REJECT core — community recency is not legal authority and adds unrelated auth/search surface |
| InsForge/InsForge | Apache-2.0; backend platform with auth, DB, storage, compute, model gateway | app/backend infrastructure | REJECT — unnecessary stateful backend and secret surface; core must stay static/zero-runtime |
| Hugging Face vllm-sr/Decision 2.0 | Apache-2.0 model family; feature-extraction/classification; custom model code; local inference requires compute | experimental decision models | REJECT runtime — not an Agent Skill dependency, adds model/compute/custom-code surface without solving a release blocker |
| cloudflare/security-audit-skill | MIT; multi-phase agent security audit with independent verification and coverage ledger | highly relevant maintainer audit methodology | **ADOPT CONCEPT ONLY** — independent verification + confirmed/needs_validation/rejected + coverage-led review; no runtime dependency/code import |
| Asymptote-Labs/agent-beacon | MIT; local-first agent telemetry/memory capturing prompts, tool calls, files, approvals and MCP activity; optional cloud forwarding | rich behavioral trace provenance | REJECT runtime — high privacy/retention surface for banking context; synthetic eval JSON is sufficient today |

## Why only three local web adapters were accepted

The skill sometimes needs to read a public bank help page that is difficult to fetch. The smallest useful escalation is:

`native fetch → Crawl4AI/Scrapy → Playwright render-only`

Adding a browser-agent framework, cloud VM or autonomous research stack would not improve the legal/banking reasoning. It would increase dependencies, prompt-injection exposure, credential risk and maintenance.

## Non-negotiable restriction

Accepted web tooling is **transport/rendering only**. It must never receive banking credentials, reuse authenticated cookies, submit forms, click transactional controls or operate home banking.

See [../references/public-web-research.md](../references/public-web-research.md).

## Host-level research connectors

Search/research connectors such as Exa, Parallel Search, Liner and Tavily can be useful as **discovery redundancy** when already available in the host. They are intentionally not dependencies and never outrank an official legal source. Undermind is useful for doctrine/scholarly context rather than case-law authority; Powerset Research is useful for evaluating repositories, not legal propositions.

The operational policy is documented in [RESEARCH-STACK.md](RESEARCH-STACK.md).


## Prism Legal OS — qué se integra

Prism sí aporta una idea útil: separar la **lista reutilizable de checks** del resultado jurídico. Su patrón de rulebooks y revisión respaldada por fuentes encaja con el modo FORENSIC.

No se integra el producto ni su código. El proyecto completo tiene otro alcance (gestión contractual/documental), una superficie operativa mucho mayor y licencia AGPL-3.0-only. Además, varias capacidades AI/RAG requieren proveedor configurado e infraestructura adicional.

La adopción local es deliberadamente mínima e independiente:
- `registry/review-playbook.json`: checks estructurados por etapa;
- `references/review-playbook.md`: reglas de uso;
- sin porcentajes de “cumplimiento jurídico”;
- sin importar código, prompts ni plantillas de Prism;
- sin nueva dependencia, servicio, credencial o costo obligatorio.

Esto mantiene el core MIT, USD 0 y vendor-neutral.


## Cloudflare security-audit-skill — qué se integra

Sí suma, pero **como metodología de auditoría del mantenedor**, no como dependencia de la skill bancaria.

Se adoptan cuatro patrones:
- un hallazgo no se acepta solo porque lo propuso el mismo agente que lo encontró;
- separar `confirmed`, `needs_validation` y `rejected`;
- registrar cobertura y gaps, no llenar el informe con “best practices” sin impacto;
- mantener evidencia reproducible y refutar candidatos antes de promoverlos.

No se copia su implementación ni sus validadores Node. El core bancario sigue stdlib/static y USD 0.

## Evaluación de los enlaces nuevos

- **cc-thinking-skills:** buenas técnicas genéricas, pero redundantes con FORENSIC + review playbook + auditorías hostiles ya integradas.
- **Agent-Reach:** queda fuera por diseño; su valor depende justamente de cookies/sesiones/browser reach que esta skill prohíbe para banca.
- **last30days:** útil para tendencias, no para determinar derecho bancario vigente; las fuentes sociales nunca deben outrank BCRA/tribunal oficial.
- **InsForge:** resuelve backend/state/auth/storage, problemas que este repo deliberadamente no tiene.
- **Decision 2.0:** interesante como investigación de modelos de decisión, pero no justifica cargar pesos, custom code o cómputo para una skill textual.
- **Agent Beacon:** trazabilidad potente, pero captura demasiado contexto de sesiones; no se integra en una skill que minimiza evidencia bancaria. Puede reevaluarse exclusivamente para evals sintéticos si aparece una necesidad real.
