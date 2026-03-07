# AI-Powered OSINT, EDD & Investigation Market — Competitive Analysis
## Coldstorm AI Strategic Research | March 6, 2026
## Purpose: Go-to-market strategy for Coldstorm AI's agentic investigation vertical (Swiss Fox use case)

---

## Conclusion First (Time-Constrained Summary)

**The market is ripe for disruption. Coldstorm AI's positioning is correct — but the $3,000/mo retainer in the Swiss Fox one-pager is 40-60% underpriced.**

Key findings:
- The OSINT/EDD market is $12-18B in 2025, growing at 15-27% CAGR
- Incumbents charge $60K-$1.5M/year for platforms that are largely keyword/NLP matching, not agentic
- Boutique EDD reports from Kroll/FTI cost $3,000-$15,000 per report, delivered in 5-10 business days
- Agentic AI can deliver comparable quality in 4-8 hours at $200-$800 cost-to-serve
- Swiss investigation firms are under FINMA pressure to adopt AI (50% already using it) but face governance constraints around explainability and auditability
- The winning model for Coldstorm AI is: per-case pricing anchored at market rate ($1,500-$5,000), retainer at $6,000-$10,000/month, and a sample deliverable to prove the capability

---

## Section 1: Enterprise SaaS Incumbents — Who Sells AI-Powered OSINT/EDD?

### Tier 1: Full-Stack Intelligence Platforms (Government/Large Enterprise)

**Palantir AIP**
- Pricing: Custom enterprise, not published. AIP Bootcamp model has ~75% conversion rate, 5-day workshops
- Typical ACV: $500K-$50M+ (government and large corporate)
- Target: US government (DoD, DHS, FBI), large financial institutions, critical infrastructure
- What their "AI" actually does: Foundry + AIP orchestrates LLMs on top of Palantir's data graph. Genuinely agentic at the high end — automated decision workflows, multi-modal analysis, operational AI. Not just keyword matching.
- Strengths: Unmatched data fusion, government trust, established moat, agentic workflow tooling
- Weaknesses: Prohibitively expensive for mid-market, long procurement cycles, complex integration, "sovereign" requirements
- Coldstorm threat: Zero direct competition — different scale/market entirely.

**Recorded Future**
- Pricing: $60,000-$200,000+/year. Enterprise contracts exceed $200K
- Typical ACV: $80K-$300K for mid-enterprise; $500K+ for government
- Target: Cyber threat intelligence, nation-state threat tracking, financial sector, government
- What their "AI" actually does: NLP-based pattern recognition, entity extraction, predictive risk scoring. Strong on threat intel, weaker on OSINT investigations of people/entities
- Strengths: Deep threat intel data lake, strong brand, integrations ecosystem
- Weaknesses: Primarily cyber-focused, not an EDD/investigation tool, expensive
- Coldstorm threat: Minimal — different use case.

**Babel Street**
- Pricing: Not published. Enterprise/government contract-based. Estimated $100K-$500K+ ACV
- Target: Government intelligence agencies, law enforcement, corporate security
- What their "AI" actually does: Multilingual AI analytics across 40+ languages, real-time social media monitoring, entity resolution, behavioral pattern analysis
- Strengths: Multilingual capability (strongest in market), real-time feeds, government trust
- Weaknesses: High cost, opaque pricing, primarily built for government procurement cycles

**Voyager Labs**
- Pricing: Government-negotiated. Estimated $100K-$1M+ per deployment
- Target: Law enforcement, intelligence agencies
- What their "AI" actually does: Massive open-web, deep web, and dark web scraping with AI-powered behavioral analysis. Controversial — sued by Meta for scraping in 2023.

**Cobwebs Technologies (now Webint)**
- Pricing: Enterprise/government. Estimated $50K-$500K
- Target: Intelligence agencies, large corporates

**ShadowDragon**
- Pricing: Not published. Government procurement via SEWP V, ITES-SW2
- Estimated: $20K-$150K per deployment
- Target: Law enforcement, national security, financial crimes units
- Recently integrated LLMs for case summarization and pattern linking (2025)

**Fivecast**
- Pricing: Not published. Raised $20M Series A (2023). Estimated $50K-$250K per enterprise
- Target: National security, defense, financial crime, corporate security
- What their "AI" actually does: Multi-modal AI analysis (text, image, video). ONYX for AI-enabled analysis, MATRIX for automated high-throughput screening

**Skopenow**
- Pricing: Not published. 1,500+ customers including Fortune 500
- Estimated: $10K-$50K per seat/deployment
- Target: Corporate security, fraud, HR investigations

**Maltego**
- Pricing: Professional Plan $6,600/year (20,000 credits/month). Enterprise: custom (250,000 credits/month, 100+ connectors)
- Target: Corporate security, law enforcement, journalists, pen testers, investigations
- What their "AI" actually does: Link analysis and visualization, entity relationship mapping. Connectors pull from third-party APIs. Not truly agentic — it's a human analyst tool with good data connectivity.
- Strengths: Best visualization tool in the market, 100+ pre-built connectors, Bellingcat-validated
- Weaknesses: GUI-first (not agent-friendly), requires skilled analyst, not automated
- Coldstorm relevance: Tool Coldstorm should integrate (via Maltego Graph API) for relationship visualization.

---

### Tier 2: Compliance/EDD Platforms

**ComplyAdvantage**
- Pricing: Starter from $99.99-$119.99/month. Enterprise: custom. ComplyLaunch: 12 months free for early-stage fintechs
- What it does: Real-time sanctions, PEP, and adverse media screening via API. 10M+ pages/day NLP adverse media processing.
- Target: Fintechs, banks, challenger banks, payment processors
- Strengths: Best API for agent integration at entry level, real-time data, adverse media classification
- Weaknesses: Not an investigation tool — it's a screening tool. Point-in-time checks, not investigative depth.
- Coldstorm relevance: Core stack component — use ComplyAdvantage API for sanctions/PEP/adverse media layer.

**Refinitiv World-Check (LSEG)**
- Pricing: Not published. Average ~$113,000/year; maximum $1.5M. EDD reports available per-order.
- What it does: Industry-standard PEP and watchlist screening database. 400+ analysts, 65 languages. Tiered reports from automated Snapshot to full Enhanced Due Diligence.
- Target: Global banks, law firms, wealth management, government
- Strengths: Regulator-recognized database, gold standard for PEP screening, ISAE 3000/PwC certified, 400 human analysts
- Weaknesses: Very expensive, slow EDD report production (days), not agent-accessible
- Coldstorm relevance: This is who Coldstorm competes with on EDD reports — the $3,000-$15,000 per report market.

**Dow Jones Risk & Compliance**
- Pricing: Not published. Revenue ~$250M in 2023. Enterprise contract-only.
- Strengths: Media integration moat (Dow Jones owns the news)
- Weaknesses: Expensive, limited investigation depth beyond screening

**LexisNexis Nexis Diligence+**
- Pricing: Not published. LexisNexis AML/KYC revenue approaches $800M.
- What it does: Largest provider of AML/KYC data (~36% total industry spend). 7M+ structured profiles, 60+ risk categories.
- Strengths: Largest data asset in the market
- Weaknesses: Expensive, built for large institutions

**Sayari**
- Pricing: Not published. $40M Series C (2021). Enterprise custom.
- What it does: Corporate ownership graph. 2.7B entities from 250+ jurisdictions. Pre-computes beneficial ownership, sanctions exposure, UBO mapping. Analysts find 544% more entities vs. manual.
- Strengths: Best corporate ownership graph in the market. OFAC 50% rule analysis automated.
- Coldstorm relevance: Strong candidate for API integration. Best UBO mapping tool for agent OSINT.

**Moody's (Bureau van Dijk/Orbis)**
- Pricing: ~$50,000-$500,000+ enterprise. Per-report access also available.
- Strengths: Financial data depth, Orbis is gold standard for private company financials

**Exiger (DDIQ)**
- Pricing: Not published. Enterprise custom. AI-powered EDD platform.
- What it does: Automated due diligence for supply chain, third-party risk, compliance.

**Chainalysis**
- Pricing: Starting ~$10K/seat. ARR ~$190M in 2023, projecting $250M in 2024.
- Target: Government (DoD, FBI, IRS = majority of revenue), exchanges, financial institutions
- Coldstorm relevance: Swiss Fox needs crypto tracing capabilities. TRM Labs BLOCKINT API (more accessible) + Chainalysis certification = credibility.

---

### Tier 3: Boutique Investigation Firms (The Real Competitors)

**Kroll (Investigations, Diligence & Compliance)**
- Billing model: Hourly. Client billing rates: $400-$750/hr for senior investigators. EDD reports estimated $3,000-$15,000+
- Turnaround: 5-10 business days standard
- What their "AI" does: Internal tools for document review and pattern analysis. Still primarily human-delivered.
- Strengths: Trusted brand, global network, HUMINT capability, expert witness credibility
- Weaknesses: Expensive, slow, partnership model limits pricing flexibility
- Coldstorm threat: Direct competitor. Coldstorm can deliver comparable output 5-10x faster at 30-50% of the cost.

**Nardello & Co.**
- Band 1 Chambers ranking in all three regions (US, UK, APAC) simultaneously — never done before
- Pricing: Estimated $300-$600/hr for senior investigators. EDD reports $5,000-$20,000+
- AI adoption: Limited — reputation risk from AI errors too high for their brand

**S-RM Intelligence and Risk Consulting**
- AI adoption: Integrating AI for document processing; keeping humans on client-facing outputs

**FTI Consulting**
- Revenue: ~$3.5B (total firm). EDD reports $5,000-$20,000+
- AI adoption: Investing heavily in AI tools for internal efficiency but maintaining human delivery model

**AI-Native Startups**
- **IVIX**: $85M total funding. AI/OSINT for tax compliance. Not EDD — focused on tax authority clients.
- **Social Links**: OSINT platform. Frost & Sullivan 2025 market leader. Per-call pricing ($0.15-$0.40). 500+ sources, 1,700 extraction methods.
- **OSINT Industries**: $19-$99/month subscription. 1,500+ sources. 5,000+ law enforcement departments.
- **Blackdot Solutions (Videris)**: AI-assisted investigation platform. "Human-at-the-heart" positioning.
- **Liferaft**: Canadian OSINT platform acquired by Securitas (Feb 2026). Corporate security focus.

---

## Section 2: How Do They Sell? (Go-to-Market Reality)

### Sales Cycles by Segment

| Segment | Sales Cycle | Decision Maker | Key Criteria |
|---------|-------------|----------------|--------------|
| Government/National Security | 6-24 months | Procurement officer | Security clearance, proven tech |
| Large Financial Institution | 3-12 months | CRO/CCO/Legal | Regulatory recognition, ISAE 3000 |
| Law Firm (AmLaw 100) | 1-3 months | Partner | Credibility, confidentiality, speed |
| PE/Investment Firm | 2-6 weeks | Deal team | Speed, depth, M&A timeline |
| Mid-size Corporate | 1-4 weeks | Legal/Compliance | Price, speed, defensibility |
| Investigation Boutique | 1-2 weeks | Principal/Partner | Quality, speed, margin for resale |

### How Boutique Investigation Firms Price Engagements

- **Hourly billing**: Senior Director $300-$500/hr; Managing Director $400-$750/hr; Analyst $150-$250/hr
- **Per-report flat fee**: Standard DD $750-$3,000; Enhanced DD $3,000-$15,000; Complex investigations $20,000-$150,000+
- **Retainer**: Monthly for ongoing access: $5,000-$25,000/month
- **Contingency**: Rare — only for asset recovery with clear recovery prospects

### The Margin Problem Incumbents Have

- Boutique investigations: Revenue-per-analyst ~$800-$1,200/day billed. Cost ~$400-$600/day. Margin ~30-50%.
- AI compresses delivery time 70-80%. Same billing, 70% lower labor cost = margins expand to 60-80%.
- Kroll/FTI's dilemma: AI threatens the billable-hour model they're built on.
- Coldstorm's opportunity: AI-native delivery at below-market price with above-market speed.

### SaaS Platform vs. Consultancy vs. Coldstorm

| Dimension | SaaS Platform (Sayari, Maltego) | Investigation Consultancy (Kroll) | Coldstorm AI (agentic) |
|-----------|--------------------------------|-----------------------------------|------------------------|
| Output | Raw data, visualizations | Finished report, expert judgment | Finished report + agent trail |
| Human judgment | No (user does the work) | Yes (their analysts) | Yes (Makir reviews output) |
| Speed | Fast (minutes to hours) | Slow (days to weeks) | Fast (hours) |
| Cost | $10K-$1.5M/year subscription | $3K-$20K per report | $500-$5K per report |
| Scalability | High | Low (headcount-constrained) | High (agent-constrained) |

---

## Section 3: The Agentic AI Disruption Opportunity

### What Agents Can Do NOW That Incumbents Cannot

1. **Parallel multi-source OSINT in minutes**: Simultaneously query OpenCorporates, CourtListener, GDELT, OpenSanctions, GLEIF, EDGAR, Zefix — synthesize in 2-4 hours vs. 2-3 days for human analyst.
2. **Cross-jurisdictional ownership mapping**: Approximate 70-80% of Sayari's capability for $300/month in API costs vs. $50K+/year.
3. **Dynamic query generation**: LLM agent reasons about *what to search next* based on findings — following ownership chains, translating names, identifying aliases.
4. **Report production at scale**: Formatted, sourced, client-ready report in 30-60 minutes after data gathering vs. 4-8 hours human writing time.
5. **Adverse media synthesis**: Search, read, summarize across dozens of sources in parallel with severity classification.
6. **Cost structure**: $20-$80 per investigation (API costs) vs. $2,000-$8,000 for human-produced Kroll report.

### Incumbent Moats (Real and Durable)

1. **Proprietary data** (World-Check, Dow Jones): 30+ years of curated PEP/watchlist data — not replicable via OSINT alone.
2. **Regulatory recognition**: World-Check screening recognized by FINMA, FCA, FinCEN. AI output is not — yet.
3. **HUMINT capability**: In-country sources in 150+ jurisdictions for information not online.
4. **Expert witness credibility**: Kroll MD's signature matters in court. AI agent's output does not — yet.
5. **Legal privilege**: Attorney-client privilege requires law firm retainer structure.
6. **Relationships**: Years of deal flow with regulators, law firm GCs, PE firms.

### Incumbent Weaknesses That Agents Exploit

1. **Speed**: 5-10 day turnaround vs. hours.
2. **Price**: $5,000-$20,000/report excludes mid-market. Agents serve at $500-$2,000.
3. **Scale**: Headcount-constrained. Agents scale instantly.
4. **Consistency**: Human analysts vary. Agents produce reproducible outputs.
5. **Auditability**: Agent trail is *better* than human investigator's notes.
6. **24/7 capability**: No business hours limitation.
7. **Jurisdictional breadth**: Simultaneous multi-jurisdiction, multi-language queries.

### Market Direction 2026-2027

- "AI-assisted" becomes table stakes — differentiation window is 12-24 months.
- Expect 2-3 well-funded startups targeting EDD/investigation AI-agent space.
- FINMA Guidance 08/2024 and EU AI Act creating frameworks — not blocking AI use.
- AI-native boutiques will start winning cases from traditional firms.
- Proprietary data moats gradually erode as open-source databases mature.
- Winning positioning: "agent-generated, expert-reviewed."

---

## Section 4: Revenue Model Analysis

### TAM/SAM

| Market Segment | 2025 Size | Growth |
|----------------|-----------|--------|
| Total OSINT market | $12.7B-$18.2B | 15-27% CAGR |
| OSINT software/tools only | $2.6B | 11.8% CAGR |
| Financial crime/EDD sub-vertical | ~$3B | 15.7% CAGR |
| AI-native investigation services | $500M-$1B | 50%+ CAGR |

**Coldstorm SAM**: $50M-$200M globally (boutique AI-investigation consultancy market)

### Pricing Model Comparison

| Model | Revenue Predictability | Best For |
|-------|----------------------|----------|
| Per-case | Low | New clients, proof of concept |
| Retainer | High | Established relationships, recurring volume |
| Platform subscription | Very high | If Coldstorm builds client-facing product |
| Success-based | Variable | Asset recovery, litigation support |

### Recommended Pricing for Coldstorm AI

| Service | Old One-Pager | Recommended | Rationale |
|---------|--------------|-------------|-----------|
| OSINT report (individual) | Not specified | $500-$1,500 | Market entry |
| Standard EDD report | Not specified | $1,500-$3,000 | Mid-market, above LSEG Snapshot |
| Enhanced EDD report | Not specified | $3,500-$7,000 | Competitive with boutiques |
| Complex investigation | Not specified | $8,000-$25,000 | Multi-jurisdiction |
| Monthly retainer (light) | $3,000/mo | $6,000-$8,000/mo | 4-8 standard EDD reports/mo |
| Monthly retainer (full) | N/A | $10,000-$20,000/mo | Embedded investigative partner |

**The $3,000/mo retainer is too low.** Market rate for equivalent capacity is $6,000-$10,000/month minimum.

### Margin Analysis

| Delivery Model | Revenue | Cost-to-Serve | Gross Margin |
|----------------|---------|---------------|--------------|
| Standard EDD (AI + Makir review) | $2,500 | $100-$300 | 88-96% |
| Enhanced EDD (AI + Makir review) | $5,000 | $200-$600 | 88-96% |
| Retainer $8,000/mo (8 reports) | $8,000 | $500-$1,500 | 81-94% |
| Human-delivered (Kroll equivalent) | $5,000 | $3,000-$4,000 | 20-40% |

**80-90% gross margins vs. 20-40% for traditional firms.**

### Case Studies

- **Gruve (cybersecurity services)**: $5M to $15M in 6 months using AI-native delivery. 80% gross margins.
- **IVIX**: $85M raised to commercialize AI/OSINT for tax authorities.
- **Blackdot Solutions**: Built "Videris" AI-assisted investigation platform, acquired enterprise clients.
- **Social Links**: Frost & Sullivan 2025 market leader. Per-call API model.

---

## Section 5: The Swiss Fox Use Case — Strategic Positioning

### How Swiss Investigation Firms Procure Capabilities

1. **In-house analysts**: CHF 70,000-200,000+/year. Limited by headcount.
2. **Network of freelancers**: Case-by-case specialists.
3. **SaaS tools**: Maltego, World-Check, ComplyAdvantage, OSINT Industries.
4. **Sub-contracting to larger firms**: Cases escalated to Kroll or S-RM.
5. **AI tools**: 50% of Swiss financial institutions using AI (FINMA 2025 survey).

### Swiss-Specific Regulatory Context

**FINMA Guidance 08/2024 on AI:**
- AI tools used by regulated institutions must be explainable
- AI outsourcing triggers FINMA outsourcing requirements — data protection, security, audit rights
- No Swiss equivalent to EU AI Act, but FINMA expects consideration of EU requirements
- FINMA 2025 Risk Monitor: AML is one of nine "high" priority risks

**Swiss AML Act (AMLA):**
- Banks/financial intermediaries must apply enhanced due diligence for high-risk clients — mandatory
- 87% of compliance officers expect EDD budgets to increase next 12 months
- Continuing monitoring required — creates recurring demand

**What Makes Swiss Firms Choose AI Agent Framework:**
1. Speed: FINMA timelines are tight. 24-48 hours vs. 5-10 days wins mandates.
2. Auditability: Agent step-by-step trail is competitive advantage vs. handwritten notes.
3. Cost: 40-60% below Kroll pricing.
4. Scale: Capacity expansion without headcount.
5. Confidentiality: Private infrastructure, not ChatGPT.
6. Explainability: Documented agent methodology satisfies FINMA.

### Competitive Positioning

**The unique position**: Coldstorm delivers the investigation. Swiss Fox delivers it to their client. No AI governance burden passes through.

**Swiss Fox tells their clients**: "Our investigation team uses proprietary AI-assisted research workflows." They don't disclose Coldstorm is the AI partner.

**Coldstorm deliverables must be structured for:**
- Every adverse finding backed by source URL and archived screenshot
- Methodology section in every report
- Human review attestation (Makir's sign-off)
- FINMA-compatible language for Swiss-destined reports

---

## Section 6: Recommended Next Steps

### Immediate (Week 1 — by March 10)
1. Complete OSINT sample deliverable (Task 43) — the gate to the relationship
2. Update Swiss Fox one-pager pricing: retainer minimum $6,000-$8,000/month
3. Revise per-case pricing: Standard EDD $2,000-$3,000, Enhanced EDD $4,000-$7,000

### Near-Term (March-April)
4. Build the agentic investigation framework (Task 45):
   - Sanctions/PEP: OpenSanctions self-hosted + ComplyAdvantage API ($99.99/mo)
   - Corporate registry: OpenCorporates ($2,250/yr) + GLEIF free + Zefix free + EDGAR free + Companies House free
   - Adverse media: GDELT free + web search synthesis
   - Court records: CourtListener + PACER ($0.10/page)
   - OSINT: Social Links API ($0.15-$0.40/call)
5. Register OpenCorporates commercial license ($2,250/yr)
6. Get Chainalysis Reactor certification

### Strategic (Q2 2026)
7. Deliver 2-3 sample investigations at market rate ($3,500-$5,000) to reset pricing expectations
8. Build FINMA-compliant methodology documentation
9. Target second Swiss investigation firm — replicate the model

---

## Key Numbers for Conversations

- OSINT market: $12.7-18.2B in 2025, growing at 15-27% CAGR
- EDD budgets increasing: 87% of compliance officers expect increases
- Kroll/LSEG EDD reports: $3,000-$15,000, 5-10 business days
- Coldstorm: $2,000-$7,000, 4-8 hour delivery
- Cost-to-serve: $100-$600/report vs. $2,000-$4,000 for human investigators
- Gross margin: 88-96% vs. incumbent 20-40%
- 50% of Swiss financial institutions already using AI
- FINMA intensifying AML enforcement in 2025

---

## Sources

- [Palantir AIP Bootcamp strategy](https://markets.financialcontent.com/stocks/article/marketminute-2026-3-6-palantir-shares-surge-as-aip-bootcamp-strategy-cementing-dominance-in-enterprise-ai)
- [ComplyAdvantage Pricing](https://complyadvantage.com/pricing/)
- [Refinitiv World-Check Pricing — Vendr](https://www.vendr.com/buyer-guides/refinitiv)
- [Maltego Pricing](https://www.maltego.com/pricing/)
- [Sayari Graph Product](https://sayari.com/product/)
- [Chainalysis Revenue — Sacra](https://sacra.com/c/chainalysis/)
- [Nardello — Chambers](https://chambers.com/law-firm/nardello-co-litigation-support-58:161954)
- [OSINT Market — Global Market Insights](https://www.gminsights.com/industry-analysis/open-source-intelligence-osint-market)
- [OSINT Market — Mordor Intelligence](https://www.mordorintelligence.com/industry-reports/open-source-intelligence-market)
- [LSEG Enhanced Due Diligence](https://www.lseg.com/en/risk-intelligence/due-diligence-services/reports/enhanced)
- [LSEG Rising KYC EDD Costs](https://www.lseg.com/en/insights/risk-intelligence/rising-kyc-enhanced-due-diligence-costs-can-ai-deliver)
- [Agentic AI for OSINT — Babel Street](https://www.babelstreet.com/blog/designing-trustworthy-ai-for-osint)
- [OSINT Year in Review 2025 — ShadowDragon](https://shadowdragon.io/blog/osint-year-in-review-report/)
- [IVIX $60M Raise](https://www.startuphub.ai/ai-news/funding-round/2025/ai-osint-platform-ivix-raises-60-million-to-corner-20-trillion-shadow-economy)
- [AI Disrupting Billable Hours](https://www.chiefaiofficer.com/post/ai-disrupting-professional-services-billable-hours-software-margins)
- [High-Margin AI Business Models 2025](https://www.humai.blog/high-margin-ai-business-models-financial-analysis-2025/)
- [FINMA AI Survey 2025](https://www.finma.ch/en/news/2025/04/20250424-mm-umfrage-ki/)
- [FINMA Guidance 08/2024 on AI](https://www.mll-news.com/finma-guidance-08-2024-governance-and-risk-management-when-using-artificial-intelligence/?lang=en)
- [Switzerland AML Regulations 2025](https://www.sanctions.io/blog/switzerlands-anti-money-laundering-regulations-a-2025-guide)
- [OSINT Industries Pricing](https://www.osint.industries/pricing)
- [Anthropic Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)
- [EU AML and OSINT in Europe 2025-2030](https://smartintelligence.eu/about-osint-services/europe-s-osint-market-in-2025-2030-where-growth-will-come-from/)

---

*Compiled by Coldstorm AI research system | March 6, 2026*
*For internal strategy use only — not for external distribution*
