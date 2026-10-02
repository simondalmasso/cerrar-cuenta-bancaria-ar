# Tooling audit — zero-cost / scope review

**Date:** 2026-10-02  
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

## Why only three local web adapters were accepted

The skill sometimes needs to read a public bank help page that is difficult to fetch. The smallest useful escalation is:

`native fetch → Crawl4AI/Scrapy → Playwright render-only`

Adding a browser-agent framework, cloud VM or autonomous research stack would not improve the legal/banking reasoning. It would increase dependencies, prompt-injection exposure, credential risk and maintenance.

## Non-negotiable restriction

Accepted web tooling is **transport/rendering only**. It must never receive banking credentials, reuse authenticated cookies, submit forms, click transactional controls or operate home banking.

See [../references/public-web-research.md](../references/public-web-research.md).
