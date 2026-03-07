---
name: counter-analysis
description: "Use this skill to analyze opposing party legal documents against NRG Bloom's evidence base. Trigger it whenever TON Infrastructure sends a position paper, demand letter, response letter, settlement offer, or any legal correspondence. Also trigger when Makir receives documents from opposing counsel, from the mediator (Marley Broda), or when preparing rebuttals for negotiation sessions or arbitration. Use it when Makir says 'analyze their response,' 'what are they arguing,' 'tear this apart,' 'find the weaknesses,' or asks to prepare a counter-argument. Also use when TON's position paper arrives for the simultaneous exchange."
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, mcp__memory__*, mcp__tavily__*
---

# Counter-Analysis

## What This Skill Does

Systematically dissect opposing legal documents against NRG Bloom's complete evidence base (84 verified emails, ~2,700 WhatsApp messages, 4 call transcripts, financial models, and court records). The skill produces a structured rebuttal assessment that rates every opposing argument, maps impeachment opportunities, and recommends a response strategy.

This matters because opposing documents often mix strong arguments with weak ones, and the instinct is to react emotionally to the most provocative claims. This skill forces a disciplined, evidence-based analysis that separates genuine vulnerabilities from bluster.

## Evidence Base

Read `references/evidence-inventory.md` for the full file inventory, search patterns, and held-back evidence list. That file is the canonical index -- use it to locate any source file.

## Process

### Step 1: Load Framework

1. Read ~/Work/nrg-bloom/litigation-ton/ton-counter-analysis-framework-2026-03-04.md -- this contains the anticipated arguments and pre-mapped counters.
2. Query Memory MCP for the latest litigation status, including any developments since the framework was last updated.
3. Read ~/Work/nrg-bloom/litigation-ton/CONTEXT.md for dispute background if needed.

### Step 2: Ingest the Opposing Document

Read the entire incoming document -- every paragraph, every footnote, every exhibit reference. The most dangerous arguments are often buried in subordinate clauses or footnotes, not in the headline positions. Extract:
- Every factual claim (things they say happened)
- Every legal argument (theories of liability or defense)
- Every settlement position (numbers, conditions, deadlines)
- Every disclosure or document reference (what they reveal or withhold)

Flag any arguments not anticipated in the counter-analysis framework -- these require fresh analysis and may indicate a shift in strategy.

### Step 3: Cross-Reference Against Evidence

For each claim extracted in Step 2, search the evidence base systematically. Use the search patterns in `references/evidence-inventory.md` to find sources efficiently:

1. Master email timeline: ~/Work/nrg-bloom/litigation-ton/master-verified-email-timeline-2025.md
2. Verified WhatsApp files: ~/Work/nrg-bloom/litigation-ton/verified-whatsapp-*.md
3. Call transcripts: ~/Work/nrg-bloom/litigation-ton/verified-call-transcripts.md
4. Source-linked evidence index: ~/Work/nrg-bloom/litigation-ton/source-linked-evidence-index.md
5. Master evidence summary: ~/Work/nrg-bloom/litigation-ton/master-evidence-summary-2026-02-25.md

### Step 4: Rate Each Argument

Apply this scale -- it helps Makir and counsel prioritize where to focus energy:

| Rating | Meaning | Action |
|--------|---------|--------|
| **DEVASTATING COUNTER** | Documentary evidence directly and unambiguously contradicts this claim | Lead with this in rebuttal |
| **STRONG COUNTER** | Strong evidence significantly undermines this claim | Include in rebuttal |
| **MODERATE COUNTER** | Evidence partially addresses this, but the argument has some merit | Address but don't overcommit |
| **WEAK COUNTER** | Genuine vulnerability -- our evidence is thin here | Flag for Dayo/Sarit's attention |
| **NEW ARGUMENT** | Not previously anticipated in framework | Requires fresh analysis before rating |

### Step 5: Map Impeachment Opportunities

Check whether any claim can be impeached by held-back evidence (see "Held-Back Evidence" in references/evidence-inventory.md). For each impeachment opportunity, recommend whether to:
- **Deploy now**: The rebuttal value outweighs the surprise value. Use when the claim is central to their case.
- **Hold for arbitration**: The surprise value at hearing is greater. Use when the claim is peripheral or when revealing this evidence would tip them off to adjust their position.

### Step 6: Produce the Report

## Output Format

### Counter-Analysis: [Document Name] -- [Date]

**IMMEDIATE FLAGS**
- [Anything requiring urgent action -- deadlines, admissions, threats, surprises]

**SETTLEMENT POSITION**
| Their Number | Our Number | Gap | Walk-Away Floor |
|---|---|---|---|
| [X] | $727K USD | [Y] | $500K USD |

**VERDICT**: [Within range / Below floor / Bad faith]

**TOP 5 WEAKEST ARGUMENTS** (where our evidence is strongest)
1. [Claim] -- RATING -- [Our evidence with source citation]
2. ...

**TOP 3 STRONGEST ARGUMENTS** (genuine vulnerabilities for us)
1. [Claim] -- RATING -- [Our best counter and why it falls short]
2. ...

**IMPEACHMENT OPPORTUNITIES**
| Their Claim | Held-Back Evidence | Deploy Now or Hold? | Reasoning |
|---|---|---|---|
| [Claim] | [Evidence source] | [Recommendation] | [Why] |

**NEW ARGUMENTS** (not in framework)
| Argument | Initial Assessment | Evidence Needed |
|---|---|---|

**DISCLOSURE ANALYSIS**
| Item Requested/Referenced | Provided? | What It Reveals |
|---|---|---|

**RECOMMENDED RESPONSE**
- Tone: [Aggressive / Measured / Conciliatory] -- with reasoning
- Key points to address: [List]
- Evidence to deploy: [List with source files]
- Timeline: [When to respond]

**IMPLICATIONS FOR COUNSEL**
- [Updated priorities for Sarit Batner / Dayo Adu based on what this document reveals]

**UPDATED SETTLEMENT STRATEGY**
- [Any changes to negotiation approach]

## After Producing the Report

1. Update Memory MCP with key findings -- especially any new arguments not in the framework.
2. Update tasks.yaml with new action items arising from the analysis.
3. If the document reveals information relevant to arbitration readiness, note it for the arbitration-readiness skill.

All output is confidential and privileged.
