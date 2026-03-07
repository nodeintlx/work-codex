# Big Law Litigation Tech Stack — 2025/2026

**Compiled:** March 6, 2026
**Purpose:** Map what Am Law 100 / Magic Circle / Canadian Big 6 spend on litigation tech — identify the capability gap an agentic AI system can close
**Classification:** Coldstorm AI Strategic Intelligence

---

## BOTTOM LINE

Top law firms spend **$1.5M–$2.5M+ per year** on litigation technology for a 50-attorney department. The core stack: Westlaw ($500K-$900K), Harvey AI ($720K), Relativity eDiscovery ($200K-$500K), Lex Machina analytics ($50K-$150K), and trial tools ($50K-$100K). Solo practitioners have access to **less than 5%** of this capability. The gap is not intelligence — it's infrastructure. An agentic AI system built on Claude API + open legal databases can replicate 60-70% of this stack at near-zero marginal cost.

---

## 1. LEGAL RESEARCH PLATFORMS

### What Big Law Uses

| Tool | What It Does | Cost | Who Uses It |
|------|-------------|------|-------------|
| **Westlaw Precision/Advantage** | AI-enhanced legal research, statutes, case law | $500K–$900K/yr (50 attorneys) | 198 of Am Law 200 |
| **Harvey AI** | Autonomous legal research, drafting, analysis | $1,200/seat/mo, 20-seat min ($288K/yr floor) | A&O Shearman (3,500 lawyers), PWC, top firms |
| **CoCounsel (Thomson Reuters)** | AI research grounded in Westlaw, prevents hallucination | $220–$500/mo standalone | 20,000+ firms |
| **vLex/Vincent AI** | Multi-jurisdictional research, cross-border | $300/yr starting | International firms |
| **Microsoft Copilot** | General AI assistance, document analysis | $30/user/mo | Firm-wide at Clifford Chance |

### The Pricing Gap

- Solo practitioner Westlaw: **$133–$266/month** (one state, basic)
- Am Law 100 Westlaw: **$500K–$900K/year** (full access)
- That's a **568x pricing ratio** for access to the same underlying data

### What This Means for You

Harvey AI is completely inaccessible below $288K/year. CoCounsel at $500/mo is the realistic ceiling for a self-represented litigant. But Claude API + CanLII (free) + the verification workflow in your legal-counsel skill replicates the core research function at near-zero cost. The key difference: Harvey won't hallucinate citations because it's grounded in Westlaw. You must manually verify on CanLII — which is why the skill enforces that step.

---

## 2. eDISCOVERY / DOCUMENT REVIEW

### What Big Law Uses

| Tool | What It Does | Cost | Notes |
|------|-------------|------|-------|
| **Relativity** | Enterprise eDiscovery, AI review (aiR), evidence management | $50K–$200K+ implementation | 198 of Am Law 200 |
| **Everlaw** | Cloud-native eDiscovery, predictive coding | ~$250/mo starting | #1 ranked on G2, 4 consecutive quarters |
| **DISCO** | eDiscovery with best UX (9.4/10), AI classification | Mid-market pricing | Best for smaller cases |
| **Logikcull** | Accessible eDiscovery entry point | $199–$395/mo + $25-40/GB | Best for solo/small firm |

### AI-Assisted Review (TAR 2.0 / CAL)

- **Technology Assisted Review** saves $50K–$100K per case on large document sets
- **Continuous Active Learning**: AI learns from reviewer decisions in real-time
- Concept clustering: automatically groups related documents
- Predictive coding: estimates relevance before human review

### What You've Already Built

The Operation Fresh Eyes evidence analysis (18 game-changers from 2,700+ WhatsApp messages + 84 emails) functionally replicated what Relativity aiR does — at zero cost. The difference: Relativity produces court-admissible review logs. Your analysis produces strategic intelligence. For SRL purposes, the strategic intelligence is what matters.

---

## 3. CASE STRATEGY / LITIGATION ANALYTICS

### What Big Law Uses

| Tool | What It Does | Cost |
|------|-------------|------|
| **Lex Machina** | Judge analytics, opponent analysis, damages comparables | $300/yr starting |
| **Westlaw Litigation Analytics** | Court/docket mining, outcome prediction | Bundled with Precision |
| **AAA Resolution Simulator** | Simulates arbitrator decisions from documents | New (March 4, 2026) |

### Key Capability

Lex Machina covers 94 federal district courts. You can look up:
- How a specific judge rules on motions to dismiss, summary judgment
- What damages ranges a judge has awarded in similar cases
- How opposing counsel performs (win rate, settlement rate, average timeline)
- Comparable case outcomes for damages anchoring

### Relevance

- **AAA Resolution Simulator** (launched March 4, 2026) — directly relevant to your arbitration strategy. Simulates arbitrator decisions from your documents. Worth tracking.
- Lex Machina at $300/year is actually accessible — consider subscribing if you file in Alberta

---

## 4. DRAFTING TOOLS

### What Big Law Uses

| Tool | What It Does | Cost |
|------|-------------|------|
| **Harvey AI** | Full drafting with legal reasoning | $1,200/seat/mo |
| **CoCounsel** | Drafting grounded in Westlaw citations | $220-500/mo |
| **Microsoft Copilot** | General document drafting | $30/user/mo |
| **Spellbook** | Contract-specific AI drafting | ~$500/mo |

### The Citation Verification Problem

- **SDNY Feb 2026 (Rakoff ruling)**: Public AI tool outputs are NOT privileged. Firms moving to private instances.
- **Zhang v. Chen (2024 BCSC 285)**: Canadian lawyer cited AI-hallucinated cases, held personally liable for costs
- **Hussein v. Canada (2025 FC 1060)**: Special costs imposed for AI-hallucinated citations

**Your advantage as an SRL**: You're not subject to law society professional conduct rules. But you ARE subject to the court's expectation of accuracy. The legal-counsel skill's mandatory CanLII verification step is your equivalent of Harvey's Westlaw grounding.

---

## 5. TRIAL PREPARATION

### What Big Law Uses

| Tool | What It Does | Cost |
|------|-------------|------|
| **TrialDirector** | Exhibit management, courtroom presentation | Custom quote |
| **OnCue** | Cloud-based trial presentation | $80/mo |
| **LIT Suite (TrialPad)** | iPad-native courtroom presentation | ~$200 |
| **CaseMap/TimeMap** | Case chronology, fact-issue linking | Discontinued (but widely used legacy) |

### What You Need

For an SRL, the critical tool is **timeline visualization**. CaseMap/TimeMap was the gold standard but is discontinued. Modern alternatives:
- Build visual timelines in Google Sheets or a timeline tool
- The cc-list removal chronology should be a visual graphic, not a document list
- Courts respond to visual exhibits — especially patterns shown on a timeline

---

## 6. SETTLEMENT ANALYTICS

### What Big Law Uses

| Tool | What It Does |
|------|-------------|
| **LexisNexis Verdict & Settlement Analyzer** | Industry's largest verdict/settlement database |
| **VerdictSearch** | 200,000+ verdicts, 15+ search criteria |
| **Jury verdict prediction market** | $1.18B (2024) → $4.15B projected (2033) |

### What You Can Access

- CanLII case law for comparable Canadian damage awards (free)
- Web searches for published settlement amounts in comparable disputes
- The Energy Venture Partners v Malabu precedent ($110.5M for circumvention) as your ceiling anchor

---

## 7. THE ANNUAL SPEND — BIG LAW LITIGATION DEPARTMENT

| Line Item | Annual Cost (50 attorneys) |
|-----------|--------------------------|
| Westlaw Advantage | $500K–$900K |
| Harvey AI | ~$720K |
| Relativity eDiscovery | $200K–$500K |
| Lex Machina + analytics | $50K–$150K |
| Trial tools | $50K–$100K |
| **Total** | **$1.5M–$2.5M+** |

### The AI Adoption Gap

| Metric | Large Firms | Solo Practitioners |
|--------|------------|-------------------|
| AI adoption rate | 46% | 18% |
| Westlaw access level | Full ($900K/yr) | Basic ($133/mo) |
| Harvey AI access | Yes ($288K min) | No |
| eDiscovery AI | Relativity aiR | Manual review |

---

## 8. MAGIC CIRCLE / CANADIAN BIG 6 — AI LEADERS

| Firm | AI Investment | What They're Doing |
|------|-------------|-------------------|
| **A&O Shearman** | Harvey AI | 3,500 lawyers, 43 offices, deepest integration |
| **Linklaters** | Proprietary "Laila" chatbot | 60K prompts/week, 20 dedicated AI Lawyers (hired Nov 2025) |
| **Clifford Chance** | Microsoft Copilot | Firm-wide rollout, 50 support staff made redundant |
| **Freshfields** | Google partnership | KCL LL.M. program, triple-track AI strategy |
| **McCarthy Tetrault** | Not disclosed | Tier 1 Canadian tech law, full-service AI advisory |
| **Osler** | Not disclosed | Band 1 Chambers Canada for IT/privacy, AI litigation guidance |

---

## 9. THE GAP — WHAT BIG LAW CAN DO THAT YOU CURRENTLY CANNOT

| Capability | Big Law Tool | Cost | Can You Replicate with AI? |
|-----------|-------------|------|---------------------------|
| Comprehensive legal research | Westlaw + Harvey | $1.2M/yr | **Mostly** — Claude + CanLII + verification |
| Large document review | Relativity aiR | $200K+/yr | **Yes** — Already did with Operation Fresh Eyes |
| Judge/opponent analytics | Lex Machina | $300/yr | **Partially** — web research + CanLII case analysis |
| Automated drafting | Harvey + CoCounsel | $720K/yr | **Yes** — Claude + template + verification |
| Settlement comparables | Verdict Analyzer | Bundled | **Partially** — CanLII + web research |
| Trial presentation | TrialDirector | Custom | **Yes** — Google Slides/Sheets + timeline tools |
| Multi-channel evidence synthesis | None (manual) | Associate hours | **Your advantage** — this is what you built |

### Where You Actually Have an Edge

**Multi-channel evidence synthesis** — ingesting WhatsApp, email, call transcripts, financial models, and court records simultaneously and finding patterns across them — is something **no single Big Law tool does well**. Relativity handles documents. Harvey handles research. Nobody combines both with strategic analysis. Your Operation Fresh Eyes methodology is genuinely novel.

---

## 10. RELEVANCE TO COLDSTORM AI

### The Market Gap

Harvey ($288K minimum), Relativity (enterprise only), DISCO (eDiscovery only), Lex Machina (court data only) — **none covers multi-channel evidence synthesis + OSINT + sanctions screening + strategic analysis**. That is the Coldstorm gap.

### Pricing Validation

- Old one-pager: $3,000/month retainer — **confirmed too low**
- Market supports: $5,000–$8,000/month retainer
- Per-case EDD: $1,500–$2,000
- Per-case OSINT: $300–$1,000
- Crisis investigation: $2,500–$8,000

### Sales Hook

**SDNY Rakoff ruling (Feb 2026)**: Public AI tool outputs are not privileged. This is a direct sales hook for private/privileged AI deployment — exactly what Coldstorm offers Swiss Fox.

### Competitive Threat

**Advocacy** (new entrant, Relativity Labs + Fenwick & West backing, $3.5M seed 2026) is the closest future competitor. Monitor closely.

---

## Sources

- [Legal Tech Spending +9.7% — LawNext](https://www.lawnext.com/2026/01/legal-tech-spending-surges-9-7-as-firms-race-to-integrate-ai-says-report-on-state-of-legal-market.html)
- [Harvey AI Pricing — eesel.ai](https://www.eesel.ai/blog/harvey-ai-pricing)
- [Harvey + LexisNexis — Artificial Lawyer](https://www.artificiallawyer.com/2025/06/30/harvey-lexisnexis-the-potential-pricing-impact/)
- [Inside Harvey — TechCrunch](https://techcrunch.com/2025/11/14/inside-harvey-how-a-first-year-legal-associate-built-one-of-silicon-valleys-hottest-startups/)
- [CoCounsel Legal Launch — LawNext](https://www.lawnext.com/2025/08/thomson-reuters-launches-cocounsel-legal-with-agentic-ai-and-deep-research-capabilities.html)
- [Westlaw Pricing — Lawyerist](https://lawyerist.com/reviews/online-legal-research/westlaw/)
- [eDiscovery Comparison — TrustArray](https://trustarray.com/en-us/insights/articles/relativity-everlaw-or-disco-choosing-the-right-platform-for-your-firm)
- [Lex Machina 2025 Damages Report — GlobeNewswire](https://www.globenewswire.com/news-release/2025/07/29/3123430/0/en/Lex-Machina-2025-Damage-Awards-Litigation-Report.html)
- [Linklaters AI Team — Legal Cheek](https://www.legalcheek.com/2025/11/linklaters-unveils-20-strong-ai-lawyer-team/)
- [Magic Circle AI Investment — AMPLYFI](https://amplyfi.com/blog/ai-market-intelligence-transforms-uk-legal-sector-as-magic-circle-leads-200m-investment-wave/)
- [AI Access to Justice — ABA Journal](https://www.americanbar.org/groups/journal/articles/2025/access-to-justice-how-ai-powered-software-can-bridge-the-gap/)
- [Advocacy Platform — AI Journal](https://aijourn.com/context-driven-litigation-platform-advocacy-emerges-from-stealth-raises-3-5-million-in-seed-funding/)
- [Logikcull Pricing](https://www.logikcull.com/pricing)
- [Canadian AI in Litigation — Osler](https://www.osler.com/en/insights/updates/artificial-advocacy-how-canadian-courts-and-legislators-are-responding-to-generative-ai/)
