# Coldstorm AI — 5 Production AI Compliance & Investigation Systems
## System Definitions, Architecture, and Tooling
### Last Updated: 2026-03-03 (v2 — research-validated)

These are Coldstorm's five core AI systems. Each is a configurable agentic workflow
with defined data sources, tool integrations, and deployment architecture. Systems 1-2
are in active daily production. Systems 3-5 are architecturally complete with real
tooling validated through market research — deployable on client engagement.

---

## System 1: Litigation Intelligence Engine
**Status:** Production (active daily use)
**Built for:** Live multi-party commercial dispute (proof of concept)

**What it does:**
- Ingests and cross-references large evidence sets (WhatsApp exports, email threads, contracts, court filings)
- Identifies contradictions, admissions, and patterns across hundreds of documents
- Generates ranked evidence summaries with deployment strategy recommendations (deploy vs. hold)
- Drafts position papers, damages analyses, and legal theory assessments
- Tracks litigation timelines, deadlines, and counsel communications

**Architecture:**
- Multi-agent system: parallel evidence analysis agents + synthesis agent + strategy agent
- Structured output: ranked findings with confidence levels and source citations
- Memory layer: persistent case context across sessions (knowledge graph)

**Demonstrated results:**
- Analyzed 9 WhatsApp chat exports + 150+ email threads in a single session
- Identified 18 game-changing evidence items that manual review missed
- Produced expenditure ledger, damages analysis, and 5-theory litigation path analysis
- Supporting a multi-jurisdictional dispute with two independent law firms

---

## System 2: Executive Operations Agent (Chief of Staff)
**Status:** Production (active daily use)
**Built for:** CEO/Founder workflow management

**What it does:**
- Morning briefing generation: calendar, email triage, task prioritization, deadline tracking
- Proactive risk surfacing: overdue items, stale communications, approaching deadlines
- Cross-workstream intelligence: connects developments across litigation, partnerships, funding, operations
- Automated file updates: tasks, contacts, timelines updated in real-time
- Multi-company data isolation: strict confidentiality boundaries between entities

**Architecture:**
- Persistent memory system (knowledge graph) for session-to-session continuity
- Gmail, Calendar, Drive integration via MCP servers
- Skill-based routing: specialized agents for email drafting, research, financial analysis, meeting prep
- Rules engine: security policies, formatting standards, proactive behavior triggers

**Demonstrated results:**
- Manages active task list of 30+ items across 3 workstreams
- Processes and triages inbox from 10+ key contacts with priority categorization
- Tracks litigation deadlines, partnership pipeline, and funding applications simultaneously
- Proactively flags risks and suggests next actions without being prompted

---

## System 3: Crypto Transaction Tracer (AI-Enhanced)
**Status:** Production-ready (architecture complete, tooling validated, deployable on engagement)
**Built for:** Blockchain forensics and investigation reporting

**What it does:**
- Traces fund flows across multiple chains using a combination of free and licensed APIs
- Produces structured investigation reports from raw blockchain data
- Cross-references on-chain data with sanctions lists, entity labels, and OSINT
- Generates SAR/STR-ready summaries with regulatory-specific formatting
- Risk-scores addresses using multi-source attribution with explicit confidence levels
- Detects high-risk patterns: layering, structuring, mixing, cross-chain bridge usage

**Data Sources & Tool Stack:**

| Layer | Tool | Cost | What It Provides |
|-------|------|------|-----------------|
| AML Risk Scoring | AnChain.AI AML MCP (open-source) | Free entry tier | Sanctions screening, risk scores, agentic AML workflows |
| Entity Attribution | Arkham Intelligence API | Free base / token premium | 800M+ address labels, SQL access, entity pages |
| BTC Tracing | Blockstream Esplora API | Free, self-hostable | UTXO tracing, spending status, mempool |
| EVM Tracing | Etherscan V2 API | Free (500K req/mo) | 60+ EVM chains, transactions, token transfers, labels |
| Fund Flow Analysis | Bitquery Coinpath GraphQL | Credit-based | Closest open equivalent to Chainalysis fund flow — mathematical flow algorithms + ML clustering |
| Custom Analytics | Dune Analytics | $399/mo (Plus) | SQL over 70+ chains, 700K+ community dashboards |
| Smart Money Intel | Nansen API/MCP | $69/mo | 500M+ wallet labels, DeFi flow tracking |
| Sanctions | OFAC SDN List + OpenSanctions | Free | Sanctioned address screening, self-hostable |
| BTC Mempool | Mempool.space API | Free, open-source | Real-time mempool data, fee estimation |

**Architecture:**
```
Input: Target address(es) or transaction hash(es)
  │
  ├─→ AnChain.AI MCP: Risk score + sanctions check
  ├─→ Arkham API: Entity attribution lookup (800M+ labels)
  ├─→ Etherscan/Blockstream: Full transaction history retrieval
  ├─→ Bitquery Coinpath: Multi-hop fund flow trace
  ├─→ OFAC SDN + OpenSanctions: Sanctions screening
  │
  ▼
Agent Synthesis Layer (LLM — cloud or local):
  ├─→ Cross-references all data sources
  ├─→ Builds fund flow narrative
  ├─→ Flags risk patterns (mixer, bridge, sanctioned exposure)
  ├─→ Tags confidence level per attribution:
  │     OFAC-confirmed | Exchange-attributed (high) | Community-labeled (moderate) | Unattributed
  │
  ▼
Output: Structured Investigation Report
  ├─→ Executive summary + risk assessment
  ├─→ Fund flow diagram (text-based or exportable)
  ├─→ Address-by-address breakdown with source citations
  ├─→ SAR/STR pre-draft (jurisdiction-specific: FINMA, FINTRAC, FinCEN)
  ├─→ Recommendations (escalate, monitor, close)
```

**Confidence Tiering (explicit in every report):**
- **Tier 1 — Authoritative**: OFAC SDN match, confirmed exchange hot wallet → ~100% confidence
- **Tier 2 — High**: AnChain.AI risk score + Arkham entity attribution → 85-95% confidence
- **Tier 3 — Moderate**: Community labels (Etherscan, Breadcrumbs) → 70-85% confidence
- **Tier 4 — Low/Unattributed**: On-chain pattern only, no entity mapping → flagged for manual review

**What this system does NOT do (honest boundary):**
- Does not replicate Chainalysis Reactor's proprietary clustering (requires $100K+ license)
- Does not provide court-admissible attribution (requires enterprise vendor + expert witness)
- Does not demix novel mixer outputs (requires Chainalysis proprietary intelligence)
- When a case requires these capabilities, Coldstorm recommends the client license Chainalysis/TRM directly — and Coldstorm operates it

**Deployment options:**
- Cloud: Claude API or GPT-4 + external API calls to data sources
- On-premise: Ollama (Llama 3/Mistral/DeepSeek) + self-hosted AnChain.AI MCP + OpenSanctions Docker
- Hybrid: LLM on cloud, sensitive client data stays local, only address hashes sent to external APIs

**Monthly operating cost:** $0-$500 (free tier) to $500-$1,500 (production with Dune + Nansen + Bitquery credits)

---

## System 4: Due Diligence Report Automator
**Status:** Production-ready (architecture complete, tooling validated, deployable on engagement)
**Built for:** Investigation and advisory firms (Swiss Fox, law firms, compliance teams)

**What it does:**
- Automated multi-source intelligence gathering on subjects (individuals and companies)
- Produces structured DD reports following industry standard format (Kroll/K2/FTI structure)
- Cross-references findings across corporate registries, sanctions, courts, and media
- Beneficial ownership tracing through corporate hierarchy APIs
- Jurisdiction-aware: adapts regulatory context per target country
- Every finding tagged with source URL and confidence level — no unsourced claims

**Data Sources & Tool Stack:**

| Layer | Tool | Cost | What It Provides |
|-------|------|------|-----------------|
| OSINT Orchestration | SpiderFoot OSS (self-hosted) | Free | 200+ data sources, REST API, scan automation |
| Corporate (Global) | OpenCorporates API | ~$250/mo (commercial) | 200+ jurisdictions, normalized company data |
| Corporate (UK) | Companies House API | Free | UK companies + PSC beneficial ownership |
| Corporate (US) | SEC EDGAR API | Free, no auth | Public company filings, XBRL financials |
| Corporate (Swiss) | Zefix REST API | Free | Swiss commercial register |
| Corporate Hierarchy | GLEIF API | Free, no auth | LEI lookup, parent/subsidiary chains, updated 3x daily |
| Sanctions/PEP | OpenSanctions (self-hosted Docker) | Free non-commercial | 269+ datasets, sanctions + limited PEP (28 countries) |
| Sanctions/PEP (prod) | ComplyAdvantage Starter API | $100/mo | 60+ sanction jurisdictions, full PEP, adverse media NLP |
| Court Records (US) | CourtListener RECAP API | Free | US federal litigation, millions of documents |
| Court Records (CA) | CanLII | Free (manual) | Canadian case law, all provinces |
| Court Records (UK) | BAILII | Free (manual) | UK/Irish case law |
| Adverse Media | GDELT DOC 2.0 API | Free | Global news, 65 languages, 15-min updates |
| Adverse Media | Web Search (Brave/Tavily) | Included | Recent news + LLM synthesis |
| Infrastructure | Shodan API | $49 one-time or $69/mo | Attack surface, technology stack, exposure |
| Social/Dark Web | Social Links SL API | $0.15-$0.40/call | Social media, Telegram, blockchain, dark web |
| Email/Domain | theHarvester | Free | Email harvesting, subdomain enumeration |

**Architecture:**
```
Input: Subject name + known identifiers (DOB, company name, jurisdiction)
  │
  ├─→ SpiderFoot OSS: Automated OSINT scan (200+ sources)
  ├─→ OpenCorporates + Companies House + GLEIF + Zefix: Corporate profile + hierarchy
  ├─→ SEC EDGAR: US public company filings (if applicable)
  ├─→ ComplyAdvantage or OpenSanctions: Sanctions + PEP + adverse media screening
  ├─→ CourtListener + CanLII + BAILII: Litigation history (US/CA/UK)
  ├─→ GDELT + Web Search: Adverse media sweep
  ├─→ Shodan: Infrastructure exposure (if relevant)
  ├─→ Social Links SL API: Social media / dark web (per-case, targeted)
  │
  ▼
Agent Synthesis Layer (LLM — cloud or local):
  ├─→ Deduplicates and cross-references all findings
  ├─→ Classifies adverse findings by severity and source reliability
  ├─→ Flags inconsistencies (e.g., director listed in two jurisdictions with different details)
  ├─→ Generates structured report following industry-standard DD format
  │
  ▼
Output: Due Diligence Report (10-section format)
  1. Executive Summary + Risk Rating (Low/Medium/High)
  2. Subject Identification (confirmed identity, aliases, addresses)
  3. Corporate Affiliations (current + historical directorships, shareholdings)
  4. Sanctions & Watchlist Screening (OFAC, EU, UN, national lists)
  5. PEP & Regulatory Status
  6. Litigation & Legal History (by jurisdiction)
  7. Adverse Media & Reputation (sourced, classified by type)
  8. Financial Intelligence (where accessible)
  9. Source Disclosure (every finding has a URL)
  10. Appendices (raw search results, screenshots)
```

**Confidence and Liability Framework:**
- Every adverse finding tagged: **Confirmed** (government source) / **Reported** (media, with URL) / **Flagged** (AI-detected, requires verification)
- "Flagged" items explicitly marked as "requires further investigation" — never presented as fact
- Human review mandatory before any report delivered to client
- Report includes methodology disclosure and data limitation statement

**What this system does NOT do (honest boundary):**
- Does not replace human investigator judgment on complex cases
- PEP coverage limited to 28 countries on free tier (ComplyAdvantage fills this gap at $100/mo)
- GDELT adverse media has ~55% accuracy on key fields — used for signal detection only, not citation
- Private company data in non-UK/US/Swiss jurisdictions is thin without OpenCorporates commercial
- Does not access proprietary databases (D&B, Orbis, World-Check) without client-provided credentials

**Market positioning:**
- Kroll/FTI charges $3,000-$15,000+ per enhanced DD report, 5-10 business day turnaround
- Coldstorm AI-assisted report: $500-$1,500, 24-48 hour turnaround
- Positioned as "AI-accelerated, human-verified" — NOT "fully automated"

**Deployment options:**
- Cloud: Claude API + external data source API calls
- On-premise: Ollama + SpiderFoot OSS + OpenSanctions Docker + local data processing
- Hybrid: LLM on cloud, subject PII stays local, only names/identifiers sent to screening APIs

**Monthly operating cost:** $350-$500 (production: OpenCorporates + ComplyAdvantage + Shodan)

---

## System 5: Compliance Monitoring & Alert Triage
**Status:** Production-ready (architecture complete, tooling validated, deployable on engagement)
**Built for:** Crypto exchanges, fintechs, and VQF/FINMA-supervised financial institutions

**What it does:**
- Ingests transaction monitoring alerts from any surveillance source (CSV, API, or direct integration)
- AI-powered triage: classifies alerts by true-positive probability, reduces false positives
- Generates preliminary investigation narratives for escalated alerts
- Auto-drafts SAR/STR reports with jurisdiction-specific formatting
- Escalation queue with supporting evidence summaries
- Trend analysis across alert volume, typologies, and counterparty patterns

**Data Sources & Tool Stack:**

| Layer | Tool | Cost | What It Provides |
|-------|------|------|-----------------|
| Transaction Monitoring (crypto) | Jube (open-source, AGPLv3) | Free, self-hosted | Real-time AML monitoring, ML detection, Docker/K8s |
| Transaction Monitoring (alt) | Marble (open-source) | Free, self-hosted | Fraud/AML decision engine, any infrastructure |
| Crypto Risk Scoring | AnChain.AI AML MCP | Free entry | Address risk scores, sanctions exposure |
| Crypto Risk Scoring (alt) | TRM Labs BLOCKINT API | Enterprise pricing | 100+ chains, behavioral signals (when client pays) |
| Sanctions Screening | OpenSanctions (self-hosted) | Free non-commercial | 269+ datasets, on-premise for data sovereignty |
| Sanctions Screening (prod) | ComplyAdvantage API | $100/mo | 60+ jurisdictions, PEP, adverse media, sub-second |
| SAR Filing (US) | moov-io/fincen (Go library) | Free, open-source | FinCEN BSA XML generation and validation |
| SAR Filing (intl) | GoAML XML schema | Standard | Used by 60+ countries including African FIUs |
| KYC Integration | SumSub API | Client-provided | Identity verification, onboarding data |
| LLM (SAR Drafting) | Ollama + Llama 3/Mistral | Free, on-premise | SAR narrative generation, fully private |
| LLM (alt) | Claude API | Usage-based | Higher quality drafting for non-sensitive workflows |

**Architecture:**
```
Alert Sources (any combination):
  ├─→ Client's existing surveillance system (Eventus, Scila, Nasdaq SMARTS)
  ├─→ Jube (self-hosted, open-source) — for clients without existing monitoring
  ├─→ Marble (self-hosted) — lightweight alternative
  ├─→ CSV/API manual ingestion
  │
  ▼
AI Triage Layer:
  ├─→ Alert classification: True Positive / Likely False Positive / Uncertain
  ├─→ Risk scoring: composite of transaction pattern + counterparty risk + behavioral signals
  ├─→ Context aggregation: pulls KYC record, transaction history, prior alerts, counterparty entity
  ├─→ Priority ranking: highest-risk alerts surfaced first
  │
  ▼
Investigation Assist:
  ├─→ Auto-generates preliminary case narrative from alert data
  ├─→ Cross-references with AnChain.AI / OpenSanctions for crypto-specific intel
  ├─→ Flags connections to prior cases (same counterparty, same typology)
  ├─→ Produces escalation recommendation with supporting evidence
  │
  ▼
SAR/STR Drafting:
  ├─→ LLM generates first-draft SAR narrative from case data (on-premise for privacy)
  ├─→ Regulatory formatting: FinCEN BSA XML (via moov-io/fincen), FINTRAC, FINMA/MROS, GoAML
  ├─→ Quality checks: verifies required fields, narrative completeness, typology classification
  │
  ▼
Human Review (MANDATORY — regulatory requirement):
  ├─→ Compliance officer reviews AI-drafted SAR
  ├─→ Approves, edits, or rejects
  ├─→ Files via appropriate channel (BSA E-Filing, MROS, F2R)
```

**Regulatory Compliance:**
- FinCEN (Oct 2025 FAQ): AI-assisted SAR drafting explicitly permitted. Human approval required.
- EU AI Act (Aug 2026): Compliance AI classified as high-risk. Must allow human oversight. Explainability required.
- FINRA 2026: Human-in-the-loop protocols required for agentic AI in compliance.
- All AI decisions produce explainable audit trails (feature attribution, source citations)

**Performance Benchmarks (validated by industry data):**

| Metric | Legacy (Rule-Based) | With Coldstorm System 5 | Source |
|--------|-------------------|------------------------|--------|
| False positive rate | 90-95% | 15-30% | Unit21 (Bakkt: 15%), industry consensus |
| Alert review automation | 0% | 57-93% | Unit21 (Nexo: 93%) |
| SAR drafting time | 25-315 min | 10-60 min (60-75% reduction) | FinCEN estimates + NICE Actimize data |
| Analyst case capacity | X cases/month | 2-3x cases/month | Eventus, Feedzai, Unit21 client data |

**What this system does NOT do (honest boundary):**
- Does not replace the compliance officer's judgment or approval — human-in-the-loop is non-negotiable
- Does not provide regulatory filing credentials (client must register with FinCEN, MROS, FINTRAC)
- False positive reduction requires tuning on client's historical alert data (30-90 day ramp-up period)
- Behavioral ML models require labeled training data — cold-start with rules, improve with feedback

**Deployment options:**
- Full on-premise: Jube + OpenSanctions + Ollama (zero data leaves infrastructure — ideal for Swiss FADP)
- Hybrid: Jube on-premise + AnChain.AI API (only address hashes sent externally, not client PII)
- Cloud: For non-regulated or internal-use deployments

**Monthly operating cost:**
- Self-hosted (free tools): $0/month + hardware
- Production (with ComplyAdvantage + AnChain enterprise): $100-$500/month + consulting fees

---

## Deployment Options (All Systems)

| Mode | Description | Best For |
|------|-------------|----------|
| **Cloud API** | LLM runs on Claude/GPT-4 APIs, data sources called externally | Non-sensitive workflows, internal operations, speed |
| **On-Premise (Local)** | Ollama + open-source LLMs (Llama 3.3, Mistral Large, DeepSeek R1) on client hardware. Self-hosted data tools (SpiderFoot, OpenSanctions, Jube, AnChain.AI MCP) | Client investigation data, GDPR/FADP, Swiss data sovereignty |
| **Hybrid** | LLM on cloud, sensitive data processing on local. Only non-PII identifiers (addresses, hashes, company names) sent to external APIs | Balanced cost/privacy — recommended default |

---

## Total Cost Summary

| Component | Free Tier | Production Tier |
|-----------|-----------|----------------|
| System 3 (Crypto Tracer) | $0/mo (AnChain free + Arkham free + public APIs) | $500-$1,500/mo (Dune + Nansen + Bitquery) |
| System 4 (DD Automator) | $0/mo (all free APIs) | $350-$500/mo (OpenCorporates + ComplyAdvantage + Shodan) |
| System 5 (Compliance) | $0/mo (Jube + OpenSanctions + Ollama) | $100-$500/mo (ComplyAdvantage + AnChain enterprise) |
| **Total data stack** | **$0/mo** | **$950-$2,500/mo** |

Note: Client engagement revenue should cover data costs. At a $3,000/mo retainer, data costs represent 8-30% of revenue — standard for data-driven consulting.

---

## Notes
- Systems 1 and 2 are in active daily production use — battle-tested
- Systems 3, 4, and 5 have validated tooling, defined architectures, and real data source integrations. They formalize Makir's domain expertise from Binance (market surveillance, 150M+ users) and Swiss Fox (Chainalysis investigations, 2024) into repeatable AI-powered workflows
- All systems can be demonstrated in a live walkthrough using the free tool tiers
- All systems are adaptable to full on-premise deployment for Swiss FADP/GDPR compliance
- AnChain.AI MCP server (github.com/AnChainAI/aml-mcp) is the recommended starting point for Systems 3 and 5
- Confidence tiering and human-in-the-loop are built into every system by design — not bolt-ons
