# Awesome DSH FDE

English | [中文](./README.zh-CN.md)

A field guide for **Forward Deployed Engineers (FDEs)** bringing DeepSeek Harness (DSH) into a company: what to use for connecting business systems and data, keeping permissions under control, and finding ready-made capabilities by industry.

> **How entries are picked**
> - Plugins come from the [dshfind.com](https://dshfind.com) snapshot of 2026-11-03 (26,253 repositories). Only installable, non-archived projects that are not flagged as risky are included, then hand-picked for enterprise use. Star counts are as of the snapshot.
> - 🏢 means the project is published under the vendor's or institution's own GitHub organization. That is not a DeepSeek endorsement — verify before you deploy.
> - DSH is still a developer preview and its plugin API will break. Being listed does not mean production-proven; run it in a pilot first.
> - Corrections and suggestions: see [CONTRIBUTING.md](./CONTRIBUTING.md).

## Contents

- [FDE playbook](#fde-playbook)
- [Enterprise platforms and governance](#enterprise-platforms-and-governance)
- [Identity, security and compliance](#identity-security-and-compliance)
- [Observability and operations](#observability-and-operations)
- [Messaging and collaboration](#messaging-and-collaboration)
- [Office documents](#office-documents)
- [Databases and analytics](#databases-and-analytics)
- [Knowledge bases and retrieval](#knowledge-bases-and-retrieval)
- [Browser and desktop automation (legacy systems)](#browser-and-desktop-automation-legacy-systems)
- [Industry solutions](#industry-solutions)
  - [Finance and ERP](#finance-and-erp)
  - [Investment research](#investment-research)
  - [Legal and IP](#legal-and-ip)
  - [Healthcare and life sciences](#healthcare-and-life-sciences)
  - [Manufacturing and engineering](#manufacturing-and-engineering)
  - [E-commerce and retail](#e-commerce-and-retail)
  - [Government and tendering](#government-and-tendering)
  - [Human resources](#human-resources)
  - [Marketing and content](#marketing-and-content)
  - [Research](#research)
- [Case studies and articles](#case-studies-and-articles)
- [Related lists](#related-lists)

## FDE playbook

Patterns distilled from deployment write-ups and community projects — not an official standard.

1. **Ask first: whose identity makes the call?** Most business systems authorize per user. A shared service account only fits read-only, non-personal data. For per-user data, use the employee's own token, OAuth delegation, or a short-lived identity token (JWT) issued by your platform, and let the source system decide permissions instead of copying them into the agent layer.
2. **Then: where does the call run?** Systems with an API are called server-side. Legacy systems that are intranet-only, need the employee's live session, or can only be operated through a web page belong on the employee's machine via browser automation — don't store employee passwords on a server.
3. **Read-only first; writes need approval.** Ship query tools in phase one. Every write needs human confirmation and an audit record.
4. **Mask sensitive data before it reaches the model** — national ID numbers, phone numbers, bank cards.
5. **One front door.** Route model calls through an enterprise gateway (quotas, audit), and aggregate business systems behind a single MCP endpoint, so each employee's DSH has one thing to configure.
6. **Vet plugins too.** Run static scanning and health checks before publishing a plugin internally, and pin versions.
7. **Roll out in stages**: get it working locally, pilot one scenario in one department, then consider private deployment and company-wide rollout. Community write-ups commonly plan in 1-, 3- and 6-month steps.
8. **Track known security issues**: early versions had a sandbox escape through the local control API (see [Case studies and articles](#case-studies-and-articles)), and indirect prompt injection succeeds often enough to matter. Upgrade promptly and never expose the Web UI directly to the internet.

## Enterprise platforms and governance

- [hikariming/dsh-ee](https://github.com/hikariming/dsh-ee) — Self-hosted enterprise platform for DSH: connect company systems and knowledge, build AI micro-apps, and ship them reviewed and permissioned to every employee.
- [himovo/movo](https://github.com/himovo/movo) ⭐517 — Turns DSH into a self-hosted enterprise agent platform with knowledge, deep research, content generation, browser automation and admin controls.
- 🏢 [iflytek/skillhub](https://github.com/iflytek/skillhub) ⭐5367 — iFlytek's self-hosted enterprise skill registry: versioned skill packages, RBAC and audit logs, Docker / Kubernetes deployment.
- [01men/ybkkasi](https://github.com/01men/ybkkasi) ⭐66 — AI asset governance: one ledger for MCP servers, skills and agents, with lifecycle states, 85 permission points, cost attribution by department × agent × skill, and an audit trail.
- [aiworkskills/deepseek-harness-server](https://github.com/aiworkskills/deepseek-harness-server) — Connect existing business systems to DSH without forking it: OAuth-delegated identity, one runtime per user, object-level authorization on business APIs.
- [git4oc/DSH-BOOT](https://github.com/git4oc/DSH-BOOT) — Multi-tenant agent platform on the DSH core: tenant isolation, audit, approvals, quota billing, session persistence.
- [slywalker2006/dsh-passwords](https://github.com/slywalker2006/dsh-passwords) ⭐81 — Server-grade gateway: remote access, automatic HTTPS, sub-user permissions and quotas, enforced sandboxing, audit log.
- [xgone/dsh-remote](https://github.com/xgone/dsh-remote) ⭐45 — Use DSH securely from a remote browser with login, MFA and roles.
- [pointer-a/dsh-server-login](https://github.com/pointer-a/dsh-server-login) ⭐32 — Multi-tenant DSH hosting: users register, an admin approves them, and each gets an isolated DSH environment.
- [mickymultani/deepseek-harness-enterprise-suite](https://github.com/mickymultani/deepseek-harness-enterprise-suite) — Open-source enterprise plugins, governance controls and connector templates (early stage).

## Identity, security and compliance

- [PensiveFei/dsh-secure-audit](https://github.com/PensiveFei/dsh-secure-audit) ⭐86 — Read-only security and compliance plugin: prompt-injection detection, Chinese PII redaction, local configuration audit with reproducible reports.
- [PerryLink/dsh-mask](https://github.com/PerryLink/dsh-mask) ⭐16 — PII masking middleware: names, phones, IDs, bank cards and keys become placeholders before reaching the model and are restored for display; the restore table stays in memory.
- [toby-bridges/api-relay-audit](https://github.com/toby-bridges/api-relay-audit) ⭐905 — Audits API relays and LLM proxies for prompt injection, model substitution, tool-call rewriting and SSE anomalies.
- [delta-box/deltabox-lite](https://github.com/delta-box/deltabox-lite) ⭐304 — Lightweight agent sandbox with diff, commit and abort.
- [SteelUnion/dsh-confirm-gate](https://github.com/SteelUnion/dsh-confirm-gate) ⭐60 — Counts persistent operations per turn and makes the model stop and ask for confirmation past a threshold.
- [openguardrails/OpenGuardrailsBench](https://github.com/openguardrails/OpenGuardrailsBench) ⭐60 — Reproducible benchmark for AI guardrails across safety, security, privacy and policy, with Chinese and English cases (edition 0.1 is a synthetic pilot).
- [Eligahyu/dsh-sentinel-scanner](https://github.com/Eligahyu/dsh-sentinel-scanner) — Static security scan for plugins (code execution, credentials, exfiltration, obfuscation, install scripts) with a 0–100 risk score. Useful as a gate when vetting plugins.
- 🏢 [omdsh-dev/dsh-plugin-check](https://github.com/omdsh-dev/dsh-plugin-check) ⭐26 — Plugin health check: manifest, patch format, build pitfalls.
- [feely0208/dsh-bundle-cn-skills](https://github.com/feely0208/dsh-bundle-cn-skills) — Chinese compliance skills: copy red lines, AI-content labeling, personal-information protection checklist, secret scanning. Fully offline.

## Observability and operations

- [loongsuite/dsh-plugin](https://github.com/loongsuite/dsh-plugin) ⭐31 — OpenTelemetry tracing: each agent turn becomes a GenAI span tree (LLM calls with TTFT, tool runs, token usage), exported over OTLP to Jaeger, Tempo, Langfuse and others.
- 🏢 [TencentCloud/tencentcloud-agentobs-sdk-dsh](https://github.com/TencentCloud/tencentcloud-agentobs-sdk-dsh) ⭐14 — Sends DSH traces straight to Tencent Cloud Log Service (CLS), no OTLP collector needed.
- [tma1-ai/dsh-otel](https://github.com/tma1-ai/dsh-otel) ⭐10 — Traces, metrics and logs in GreptimeDB with seven Grafana dashboards: tokens, money and time per run.
- [guhanfei-ai/dsh-grafana](https://github.com/guhanfei-ai/dsh-grafana) — Query Grafana dashboards, metrics and alerts from chat.
- [runzhliu/deepseek-harness-docker](https://github.com/runzhliu/deepseek-harness-docker) ⭐146 — Community Docker / Kubernetes packaging: hardened image, Compose, Helm chart.
- 🏢 [huaweicloud/huaweicloud-devkit](https://github.com/huaweicloud/huaweicloud-devkit) ⭐70 — Huawei Cloud's official agent plugin: skills, MCP tools, guardrails, cloud sandbox.
- [caoyiwei850/dsh-ssh-ops](https://github.com/caoyiwei850/dsh-ssh-ops) ⭐48 — Drive SSH from chat with dangerous-command protection and a side terminal.
- [Khorsheed/dsh-ankh-guard](https://github.com/Khorsheed/dsh-ankh-guard) — Self-hosting guard: after the agent changes code it runs build and tests before restarting, and rolls back automatically if the service won't come up.

## Messaging and collaboration

- [xmanrui/dsh-im](https://github.com/xmanrui/dsh-im) ⭐3148 — Connect Feishu, WeChat, DingTalk, WeCom, QQ, Slack and more (9 channels) to DSH by QR code or bot credentials.
- 🏢 [DingTalk-Real-AI/dsh-dingtalk](https://github.com/DingTalk-Real-AI/dsh-dingtalk) ⭐21 — DingTalk connector.
- 🏢 [omdsh-dev/dsh-lark](https://github.com/omdsh-dev/dsh-lark) ⭐59 — Feishu / Lark bot channel.
- [zhuiyueya/dsh-im-gateway](https://github.com/zhuiyueya/dsh-im-gateway) ⭐59 — Aggregated gateway for 20+ chat platforms.
- [THEWOLFWALKER/dsh-notifier](https://github.com/THEWOLFWALKER/dsh-notifier) ⭐59 — Notification and remote-control plane: 28 outbound channels, 6 inbound controls.
- [nicecx/dsh-relay](https://github.com/nicecx/dsh-relay) — Relay approvals and questions to chat channels through one shared adapter contract.
- [wxkingstar/SpecFusion](https://github.com/wxkingstar/SpecFusion) ⭐76 — Search 65,600+ API docs from 20 Chinese open platforms in chat — handy when writing integrations.

## Office documents

- 🏢 [dream-num/univer-workspace](https://github.com/dream-num/univer-workspace) ⭐2267 — Open-source office workspace where people and agents create, collaborate and review together.
- 🏢 [dream-num/dsh-univer-office](https://github.com/dream-num/dsh-univer-office) ⭐660 — A real office environment for DSH: sheets, docs, slides and relational tables with versioned changes and isolated worktrees for multi-agent work.
- 🏢 [FylarOpen/dsh-fylar-office-editor](https://github.com/FylarOpen/dsh-fylar-office-editor) ⭐263 — Office preview, editing and DOCX generation built on the Fylar Office SDK.
- [sueccku/dsh-plugin-wps-office-next](https://github.com/sueccku/dsh-plugin-wps-office-next) ⭐29 — Operate WPS spreadsheets, documents and slides in Chinese conversation, including batch PDF export.
- [copylee711/dsh-office](https://github.com/copylee711/dsh-office) ⭐20 — Edit the Word / Excel / PowerPoint file you already have open, with changes visible live (Windows).
- 🏢 [omdsh-dev/dsh-office](https://github.com/omdsh-dev/dsh-office) ⭐30 — Generate, read and edit xlsx, pdf and pptx.
- [HuanLinOTO/dsh-plugin-mineru](https://github.com/HuanLinOTO/dsh-plugin-mineru) ⭐51 — MinerU parsing of PDF, images and Office files into structured Markdown / JSON; a good preprocessing step before knowledge-base ingestion.
- [17897693/dsh-wen](https://github.com/17897693/dsh-wen) — Read, write and convert office formats, with built-in offline OCR for Chinese scans.
- [liustack/pptwise](https://github.com/liustack/pptwise) ⭐27 — Builds real, editable PowerPoint decks (not HTML) locally, no API key needed.

## Databases and analytics

- 🏢 [omdsh-dev/dsh-data-agent](https://github.com/omdsh-dev/dsh-data-agent) ⭐217 — Connect a database for conversational analysis and business insights.
- [niuhuoshan/dsh-connect](https://github.com/niuhuoshan/dsh-connect) — Data-source connector: metadata discovery, AI semantic modeling, read-only SQL, fixed HTTP API calls.
- [mengqi1436/dsh-db-tool](https://github.com/mengqi1436/dsh-db-tool) — Chat-driven admin for 8 databases, with per-project grants and confirmation for dangerous operations.
- [OtterMind/sqlx](https://github.com/OtterMind/sqlx) — Database CLI for agents with encrypted data sources and on-demand native / JDBC workers.
- [duyanta123/dsh-data-insight](https://github.com/duyanta123/dsh-data-insight) — CSV analysis with DuckDB, charts and report templates.
- [Onenightcarnival/dsh-toolkit](https://github.com/Onenightcarnival/dsh-toolkit) — Database workbench, S3 storage, OpenTelemetry export and browser control.
- [nomicore-ai/nomicore](https://github.com/nomicore-ai/nomicore) — A self-describing, governed data core: schemas, ownership, validation and semantics travel with the data.
- [duhu2000/dsh-mcp-connector](https://github.com/duhu2000/dsh-mcp-connector) ⭐103 — MCP data-marketplace connector for enterprise, financial, legal, patent and research data; OAuth, API keys, HTTP / stdio.

## Knowledge bases and retrieval

- [Soren-ABT/dsh-knowledge](https://github.com/Soren-ABT/dsh-knowledge) ⭐89 — Knowledge base and RAG: chunking, local embeddings, hybrid search, management panel.
- [PerryLink/dsh-library](https://github.com/PerryLink/dsh-library) ⭐24 — Local document library with hybrid semantic + keyword search, diversity re-ranking and citation checks; no model downloads.
- [Rxiain/dsh-openviking](https://github.com/Rxiain/dsh-openviking) ⭐19 — OpenViking retrieval, resource management, auto-recall and session memory.
- [chenkezhen480/pinakes-rs](https://github.com/chenkezhen480/pinakes-rs) — Self-hosted knowledge service: an LLM-maintained wiki plus a business graph, with no LLM or database on the read path; HTTP and MCP.
- [mingzeng21/dsh-obsidian](https://github.com/mingzeng21/dsh-obsidian) ⭐40 — Search, read, write and move notes in a local Obsidian vault.
- [poco-ai/Agentero](https://github.com/poco-ai/Agentero) ⭐1074 — Research workspace for humans and agents: PDF Q&A with citations, vault, writing.

## Browser and desktop automation (legacy systems)

Often the only way to get data out of systems without an API. Prefer running these on the employee's machine with their own session.

- [Fisfzy/dsh-ego-browser](https://github.com/Fisfzy/dsh-ego-browser) ⭐409 — An agent-oriented Chromium: semantic snapshots, semantic clicking, form filling, per-task isolated browser spaces.
- [drscrewdriver/dsh-browser-cdp](https://github.com/drscrewdriver/dsh-browser-cdp) ⭐24 — Drive a real Chrome over CDP, with live screenshots and login import.
- [angelky7/dsh-browser-control](https://github.com/angelky7/dsh-browser-control) ⭐53 — A Chrome extension plus DSH plugin that controls the employee's own browser.
- [SheepofSheep/dsh-doyourweb](https://github.com/SheepofSheep/dsh-doyourweb) ⭐40 — Reference and control tabs already open in Chrome / Edge.
- [anweat/dsh-browser](https://github.com/anweat/dsh-browser) ⭐31 — Self-contained browser runtime bundling Playwright (Chromium).
- 🏢 [Tabbit-Browser/dsh-tabbit](https://github.com/Tabbit-Browser/dsh-tabbit) ⭐121 — Tabbit Browser plugins for DSH.
- [momasiku/dsh-pilot](https://github.com/momasiku/dsh-pilot) ⭐145 — Windows desktop automation: CAD, WPS, browsers, WeChat.
- [Anionex/dsh-computer-use](https://github.com/Anionex/dsh-computer-use) ⭐89 — macOS computer use built on accessibility APIs, refusing actions based on stale screen state, with scoped permissions.
- [dttxorg/deepseekeyes](https://github.com/dttxorg/deepseekeyes) — Auditable vision and cross-platform computer use that keeps evidence for every step.
- [monagisa/dsh-plugin-shop-accounts](https://github.com/monagisa/dsh-plugin-shop-accounts) — One Chrome profile per store: log in once, keep the session alive with scheduled checks. A useful reference for managing many accounts with web login sessions.

## Industry solutions

### Finance and ERP

- [EthanYoQ/Invoice-Downloader](https://github.com/EthanYoQ/Invoice-Downloader) ⭐533 — Collects PDF / OFD / XML e-invoices from mailboxes, OCRs, files and summarizes them in Excel for expense claims.
- [988hj7tczd-oss/dsh-invoice-tools](https://github.com/988hj7tczd-oss/dsh-invoice-tools) — Parses Chinese e-invoice PDFs into structured JSON with amount cross-checks and builds expense reports.
- [zhang787jun/dsh-finance](https://github.com/zhang787jun/dsh-finance) — Finance and accounting workflows adapted from Anthropic's Finance examples.
- [maxmilian/dsh-odoo](https://github.com/maxmilian/dsh-odoo) — Read-only Odoo ERP tools with an opt-in, restricted draft-create tool — a good example of read-first, limited-write design.

### Investment research

- [PerryLink/dsh-industry-research](https://github.com/PerryLink/dsh-industry-research) ⭐215 — Industry and company research: methodology skills, value-chain mapping, policy and news tracking, auditable reports.
- [PerryLink/dsh-research-report](https://github.com/PerryLink/dsh-research-report) ⭐212 — Verifiable report engine: every claim is bound to an evidence snapshot, and sealed reports are tamper-evident.
- [hancao97/hanai-investment-dsh](https://github.com/hancao97/hanai-investment-dsh) ⭐120 — Local-first A-share research workbench: dashboards, valuation, versioned reports.
- [davidalmeida90/finance-agent-kit](https://github.com/davidalmeida90/finance-agent-kit) — Equity valuation skills and data MCPs (SEC filings, sector beta).

### Legal and IP

- 🏢 [yuandian-ailaw/yuandian_dsh_plugin](https://github.com/yuandian-ailaw/yuandian_dsh_plugin) — Huayu Yuandian legal-data plugin.
- [duhu2000/qcc-mcp-legal-oauth](https://github.com/duhu2000/qcc-mcp-legal-oauth) — One-click OAuth to Qichacha's regulation and case-law MCP — a reference for per-user authorization.
- [MiaoQichuan/new-litigation-visualization](https://github.com/MiaoQichuan/new-litigation-visualization) ⭐141 — Litigation visualization: timelines, chronologies, adversarial maps, legal-relationship diagrams.
- [yuc16/PatentRadar](https://github.com/yuc16/PatentRadar) ⭐67 — Enter a patent publication number, get a competitor infringement analysis.
- [ai-tools-mtl/Aurify](https://github.com/ai-tools-mtl/Aurify) — Patent drafting gatekeeper: searches Chinese patents to judge whether an idea is worth filing, then walks through the full disclosure document.
- [ByronLeeeee/dsh-legal-dashboard](https://github.com/ByronLeeeee/dsh-legal-dashboard) — Matter-aware legal dashboard and document tools.
- [wesky820/dsh-law](https://github.com/wesky820/dsh-law) — Local legal workbench with case board, calendar and deadlines.

### Healthcare and life sciences

- [sagirimo/BioDSH](https://github.com/sagirimo/BioDSH) ⭐65 — Bioinformatics agent desktop for clinicians and wet-lab scientists, with offline mode.
- [bowang-lab/dsh-medomni](https://github.com/bowang-lab/dsh-medomni) — Medical image analysis.
- [wp-a/dsh-academic-paper-search](https://github.com/wp-a/dsh-academic-paper-search) — Chinese academic search with citation verification, citation graphs, MeSH and clinical-trial search.

### Manufacturing and engineering

- [27painter/dsh-sw-cad](https://github.com/27painter/dsh-sw-cad) — SolidWorks and AutoCAD automation (Windows, COM).
- [LAU-MARS/dsh-cad](https://github.com/LAU-MARS/dsh-cad) ⭐32 — 2D and 3D CAD.
- [AmethystLuna/embedded-workbench](https://github.com/AmethystLuna/embedded-workbench) ⭐29 — Embedded C/C++ firmware skills: FreeRTOS, Keil, HardFault triage.
- [JoeyZzZzZz/treasure-map](https://github.com/JoeyZzZzZz/treasure-map) — Firmware analysis over MCP: dangerous calls found, and which functions changed between two versions.
- [Fantasality/dsh-origin-plugin](https://github.com/Fantasality/dsh-origin-plugin) ⭐36 — Drive OriginLab scientific plotting from chat, 74 tools (Windows).
- [liuhange789/data-asset-inspector](https://github.com/liuhange789/data-asset-inspector) — 30 inspection plugins: data-asset registration, government data checks, AML compliance, BIM inventory, pipeline inspection.

### E-commerce and retail

- [lunw/shopline-ai-toolkit-dsh](https://github.com/lunw/shopline-ai-toolkit-dsh) — SHOPLINE developer MCP bridge and SHOPLINE skills.
- [Tulipe1735/dsh-plugin-kefu](https://github.com/Tulipe1735/dsh-plugin-kefu) — E-commerce customer-service desk: product knowledge base, grounded replies, hand-off queue, Taobao / JD open-platform channels.
- [mirror9933/dsh-pixmart](https://github.com/mirror9933/dsh-pixmart) — Product imagery: hero, detail, ad and white-background images.
- [shine-233/dsh-waimao](https://github.com/shine-233/dsh-waimao) — Cross-border B2B lead generation: prospect search, WhatsApp review desk, email follow-ups, CRM, quote PDFs.

### Government and tendering

- [linhut/gongwen-skill](https://github.com/linhut/gongwen-skill) ⭐99 — Full official-document workflow under GB/T 9704: format checks and fixes, native Word revisions and comments, fact checks.
- [ExElectron/dsh-tool-hongtou](https://github.com/ExElectron/dsh-tool-hongtou) ⭐27 — Standard red-header official documents: the LLM writes only a structured outline, and the layout comes from deterministic rendering.
- [Ramenne/DeepSeek-Harness-Gov](https://github.com/Ramenne/DeepSeek-Harness-Gov) — Government edition of DSH: a public-service WebUI and official-document plugin.
- [maike-china/rejection-check](https://github.com/maike-china/rejection-check) — Tender rejection-clause checks: extracts disqualifying clauses, runs three rounds of risk checks, outputs a PDF report.
- [zslzxy/aitoubiaoling-bid-review](https://github.com/zslzxy/aitoubiaoling-bid-review) — Risk review of commercial and technical bids.

### Human resources

- [Viy1204/recruiting-copilot](https://github.com/Viy1204/recruiting-copilot) ⭐105 — Recruiting workflow: role definition, sourcing on BOSS Zhipin and Liepin, résumé evaluation, interview scheduling, candidate ledger and daily reports.
- [MaxHou-infinity/dsh-scout](https://github.com/MaxHou-infinity/dsh-scout) — Evidence-driven company and role due diligence.

### Marketing and content

- 🏢 [redfox-data/redfox-community-dsh](https://github.com/redfox-data/redfox-community-dsh) — RedFox Data: 100+ social-media data skills (Douyin, Xiaohongshu, Kuaishou, Bilibili, WeChat Official Accounts, Weibo, TikTok and more).
- [jerryjiao/dsh-wewrite](https://github.com/jerryjiao/dsh-wewrite) — WeChat Official Account writing pipeline; scheduled runs only save drafts, and a human always presses publish.
- [aiworkskills/dsh-wechat-article](https://github.com/aiworkskills/dsh-wechat-article) — WeChat Official Account operations: topic, draft, layout, images, publish.
- [Finderchangchang/brewreel](https://github.com/Finderchangchang/brewreel) ⭐178 — Vertical promo videos from cheap models, with advertising-law wording checks.

### Research

- [1692775560/dsh-Mimir-Academic-research](https://github.com/1692775560/dsh-Mimir-Academic-research) ⭐553 — Research workbench: live LaTeX compile, arXiv library, experiment tracking, GPU-server job orchestration.
- [Vncntvx/dsh-zotero](https://github.com/Vncntvx/dsh-zotero) ⭐58 — Search and read Zotero papers in chat and audit the literature trail.

## Case studies and articles

As of November 2026 we could **not find any public, named enterprise DSH production case with measured results**. Below are the most useful deployment guides, reviews and security research; outcome figures claimed in them are not independently verified.

- [DeepSeek Harness hands-on guide: five steps to enterprise adoption](https://www.53ai.com/news/OpenSourceLLM/2026082496831.html) (53AI, Chinese) — Environment, model, permissions, plugin development, packaging domain knowledge. HR example: social-insurance lookup, housing-fund calculation and background checks as separate plugins. Includes a 1 / 3 / 6-month roadmap.
- [DeepSeek Harness enterprise deployment](https://www.toutiao.com/article/7680883943696056838/) (Toutiao, Chinese) — Failures seen when demo configs go to production: lost tasks, sandbox escapes, permission sprawl, no session persistence, concurrency stalls.
- [DeepSeek Harness enterprise agent build, hands-on](https://deepseek.csdn.net/6a82cb06662f9a54cb9dd38a.html) (CSDN, Chinese) — An FDE delivery flow: discovery → knowledge foundation → standardized skills (contract review, report analysis, ticket handling) → register retrieval, skill and enterprise-API plugins → sandbox, logging and rate limits → canary release.
- [DeepSeek Harness Review: Production Readiness](https://wavect.io/blog/deepseek-harness-enterprise-review/) (Wavect) — A strong foundation for a contained engineering pilot.
- [DeepSeek Harness Sandbox Escape and Agent Containment](https://labs.cloudsecurityalliance.org/research/csa-research-note-deepseek-harness-sandbox-escape-20260910-c/) (CSA) — Flawed authentication on the local control API (port 3080 by default) allowed a sandbox escape; 0.1.1-rc.2 and earlier are affected.
- [DeepSeek Harness in Developer Preview](https://www.marktechpost.com/2026/08/17/deepseek-ai-releases-deepseek-harness-in-developer-preview/) (MarkTechPost) — Developer infrastructure, not a product; regulated enterprises can pilot it locally for private-repo coding, model evaluation and approval policies.
- [DeepSeek Harness (dsh): Installed and Benchmarked](https://flowtivity.ai/blog/deepseek-harness-open-source-agent-explained/) (Flowtivity) — Treat it as an evaluation and prototyping platform for now; revisit production once the API stabilizes.
- [DeepSeek Harness architecture analysis and implementation guide](https://intl.cloud.baidu.com/en/article/8946258) (Baidu AI Cloud) — Mentions uses in finance, customer support and IT operations with outcome figures, but names no companies.
- [DeepSeek Harness reaches 1.54M daily users, plans an official plugin market](https://www.ithome.com/1/023/011.htm) (IT Home, Chinese) — Official figures: about 35,000 third-party plugins; DeepSeek invites companies to ship products and services as plugins.

## Related lists

- [dshfind.com](https://dshfind.com) — DSH plugin directory and learning site, and the data source for this list.
- [libukai/awesome-deepseek-harness](https://github.com/libukai/awesome-deepseek-harness) — General DSH resource list.
- [the-beating-light-of-the-nail/awesome-dsh-plugin-stock](https://github.com/the-beating-light-of-the-nail/awesome-dsh-plugin-stock) — Stock, finance and quant plugins.

## License

[CC0 1.0](./LICENSE)
