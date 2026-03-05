---
name: arbitration-readiness
description: "Use this skill to track readiness for formal arbitration or litigation proceedings -- evidence packages, witness preparation, legal theory completeness, procedural requirements, and filing deadlines. Trigger it when negotiations fail or show signs of failing, when preparing for the McCarthy Tetrault call, when assessing whether NRG Bloom is ready to file, when a limitation period question arises, or when Makir asks 'are we ready to go to arbitration,' 'what do we still need,' 'can we file,' or 'what's our readiness.' Also trigger during any discussion of protective filings, arbitration clause interpretation, witness statements, or expert witness engagement. If the settlement tracker shows stalling or the negotiation window is closing, proactively surface readiness status."
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, mcp__memory__*, mcp__tavily__*
---

# Arbitration Readiness

## What This Skill Does

Ensure NRG Bloom can commence formal arbitration (Nigerian jurisdiction) or litigation (Alberta, via McCarthy Tetrault) at any time. The skill tracks every requirement across five categories so the transition from negotiation to formal proceedings is seamless if negotiations fail.

This matters because the credibility of the litigation threat depends on actual readiness. If counsel discovers that NRG Bloom is not ready to file when the negotiation window closes, the leverage evaporates. Conversely, genuine readiness increases the probability of a favorable settlement because the opposing party can see the threat is real.

For the full evidence file inventory, see `references/evidence-inventory.md`.

## Readiness File

Maintain at ~/Work/nrg-bloom/litigation-ton/arbitration-readiness.yaml

### Schema

```yaml
last_updated: "YYYY-MM-DD"
overall_readiness: "percentage"
target_readiness_date: "YYYY-MM-DD"

jurisdiction_primary:
  forum: "Nigerian Arbitration (Section 7 of SDA)"
  counsel: "Dayo Adu -- Moroom Africa"
  status: "ready | preparing | not_started"

jurisdiction_secondary:
  forum: "Alberta Court of King's Bench"
  counsel: "Sarit Batner -- McCarthy Tetrault"
  status: "ready | preparing | not_started"

categories:
  evidence:
    status: "complete | in_progress | not_started"
    items: [...]  # See checklist below
  witnesses:
    status: "complete | in_progress | not_started"
    items: [...]
  legal_theories:
    status: "complete | in_progress | not_started"
    items: [...]
  procedural:
    status: "complete | in_progress | not_started"
    items: [...]
  financial:
    status: "complete | in_progress | not_started"
    items: [...]
```

## Process

### Step 1: Load Current State

Read arbitration-readiness.yaml (if it exists), query Memory MCP for latest litigation status, and check tasks.yaml for litigation-related tasks.

### Step 2: Audit Each Category

#### A. Evidence Inventory

Check completeness against this checklist. Each item should have its source files identified and compiled:

- [ ] Email evidence (84 verified emails compiled)
- [ ] WhatsApp evidence (all 5 verified chat files)
- [ ] Call transcript evidence (4 recordings)
- [ ] Financial model evidence (David Billay's spreadsheet)
- [ ] Contract evidence (NDA, JV Agreement, SDA, Addendum No. 1)
- [ ] Meeting minutes (Axxela Feb 25 meeting)
- [ ] Expenditure ledger (completed Mar 1)
- [ ] Damages analysis (Axxela circumvention + Alberta path)
- [ ] Phoenix Trading court documents (partial -- need full complaint)
- [ ] Contemporaneous objections (Jul 11 lawyer-approved email, Dec 24 complaint)
- [ ] TON's response letters (Feb 20 + Feb 23)
- [ ] Position papers (NRG Bloom's + TON's when received)

Full file paths for all evidence are in `references/evidence-inventory.md`.

#### B. Witness Preparation

| Witness | Role | Statement Status | Key Topics | Notes |
|---------|------|-----------------|------------|-------|
| Makir Volcy | Fact (primary) | Not started | Origination, operations, circumvention, duress, termination | Cross-exam prep needed: affirmation defense, voluntary agreements, safety issues |
| Julie Peeters | Fact | Requested (Task 9) | "Calculated tactic" admission, devaluation negotiations, operational role | Statement not yet obtained |
| Dayo Adu | Counsel | N/A (not testifying) | -- | -- |
| Financial expert | Expert | Not engaged | Lost profits quantification using David Billay model | Required for damages quantum |
| Electrical expert | Expert | Not engaged | Rebutting safety pretext | May not be needed depending on TON's arguments |

Julie's statement is a known gap. It is less urgent now that Tyler's WhatsApp messages document the devaluation pattern directly, but a contemporaneous witness statement from someone present during the "calculated tactic" admission would significantly strengthen the case.

#### C. Legal Theories

| Theory | Jurisdiction | Research | Case Law | Strength |
|--------|-------------|----------|----------|----------|
| Breach of contract | Nigeria | Complete | Cited in position paper | Strong |
| Wrongful termination | Nigeria | Complete | Cited in position paper | Moderate |
| Fraudulent misrepresentation | Nigeria | Complete | Cited in position paper | Strong |
| Economic duress | Nigeria | Complete | Cited in position paper | Moderate (high bar) |
| Circumvention / unjust enrichment | Both | Complete | Cited in both analyses | Strong |
| Breach of exclusivity | Nigeria | Complete | Cited in position paper | Strong (if JVA survives) |
| Breach of honest performance (Bhasin) | Alberta | Complete | Alberta analysis | Strong |
| Breach of fiduciary duty | Alberta | Complete | Alberta analysis | Moderate-Strong |
| Breach of confidence (LAC Minerals) | Alberta | Complete | Alberta analysis | Moderate |
| Tortious interference | Alberta | Complete | Alberta analysis | Moderate |

The Alberta theories ($1.6M-$6M+ range) provide the litigation escalation threat that makes settlement credible. The Nigerian theories support the primary arbitration path. Both sets are researched -- the question for Sarit Batner on the McCarthy call is which theories to lead with and whether any require additional development.

#### D. Procedural Requirements

- [ ] Limitation period audit (confirm when 2-year clock started -- priority for McCarthy call)
- [ ] Arbitration clause review (Section 7 exact language and scope)
- [ ] Protective filing assessment (Statement of Claim to preserve rights if limitation period is at risk)
- [ ] Conflict check (Sarit Batner -- pending confirmation)
- [ ] Fee arrangement (confirm Dayo absorbs McCarthy costs)
- [ ] Nigerian arbitration rules and procedures
- [ ] Selection of arbitrator
- [ ] Service of notice of arbitration

The limitation period audit is the single most time-sensitive procedural item. If the limitation period has already expired or is about to, everything else is moot. This is the first question for the McCarthy call.

#### E. Financial Requirements

| Item | Estimated Cost | Status |
|------|---------------|--------|
| Nigerian arbitration (Dayo) | Covered by Dayo arrangement | Confirmed |
| McCarthy Tetrault (Alberta) | $290K-$690K (full litigation) | Pre-filing only for now |
| Expert witness (financial) | $30K-$100K | Not yet engaged |
| Expert witness (electrical) | $15K-$50K | May not be needed |
| Court filing fees | $500-$2,000 | Minimal |
| Document preparation | Included in counsel fees | N/A |

### Step 3: Identify Gaps

Flag any category below 80% readiness. Prioritize gaps by their impact on the ability to file -- procedural gaps (limitation period, arbitration clause) are more urgent than evidence compilation gaps because they can make filing impossible.

### Step 4: Present Dashboard

## Output Format

### Arbitration Readiness -- [Date]

**Overall Readiness**: [X]%

**Status by Category**
| Category | Readiness | Critical Gaps |
|----------|-----------|--------------|
| Evidence | X% | [List gaps] |
| Witnesses | X% | [List gaps] |
| Legal Theories | X% | [List gaps] |
| Procedural | X% | [List gaps] |
| Financial | X% | [List gaps] |

**URGENT Items** (deadline within 7 days)
- [Item] -- Due: [Date] -- Owner: [Who]

**Next Steps to Reach 100%**
1. [Highest priority gap]
2. [Second priority]
3. [Third priority]

**Estimated Time to Filing Readiness**: [X days/weeks]

## Key Dates

| Date | Event | Status |
|------|-------|--------|
| Mar 5, 2026 | Position paper exchange | Pending |
| Mar 6, 2026 | McCarthy Tetrault call -- Sarit Batner | Scheduled |
| ~Mar 10-15 | Negotiation window midpoint | Approaching |
| ~Apr 5, 2026 | 30-day negotiation deadline (est.) | Future |
| ~May 20, 2026 | 45-day mediation deadline (est.) | Future |
| Mid-2027 | Limitation period (est. -- must confirm Mar 6) | MUST CONFIRM |

## Readiness Thresholds

Update readiness percentages after every session where litigation status changes. These thresholds guide decision-making:

- **90%+**: Ready to file. Proceed if negotiations fail.
- **70-89%**: Can file with gaps. Identify what can be completed in parallel with proceedings.
- **Below 70%**: Not ready. Recommend against escalation unless forced by limitation period. Focus on gap closure.

If readiness drops below 70% and Makir is considering escalation, present the specific gaps and estimated time to close them so the decision is informed rather than impulsive.

All content is confidential and privileged. Update Memory MCP with readiness changes after each session.
