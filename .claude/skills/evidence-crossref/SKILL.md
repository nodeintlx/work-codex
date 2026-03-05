---
name: evidence-crossref
description: "Use this skill to cross-reference any claim, statement, or argument against NRG Bloom's complete evidence base (84 verified emails, ~2,700 WhatsApp messages, 4 call transcripts, financial models, court records). Trigger this skill whenever anyone asks to verify a fact about the TON dispute, check whether a claim is supported or contradicted by evidence, find corroboration for a legal argument, prepare an evidence package for arbitration or litigation, or assess the strength of any factual assertion related to the NRG Bloom v. TON matter. Also use it when reviewing opposing documents to map each claim against available evidence, when preparing for lawyer calls that require evidence citations, or when Makir asks 'do we have proof of X,' 'is this true,' 'find evidence for,' or 'what does the record show.'"
allowed-tools: Read, Glob, Grep, mcp__memory__*
---

# Evidence Cross-Reference Engine

## What This Skill Does

Search NRG Bloom's complete evidence inventory to find supporting or contradicting evidence for any claim. The evidence base is large (84 emails, ~2,700 WhatsApp messages, 4 call recordings, financial models, and court records spread across dozens of files) and manually searching it is slow and error-prone. This skill knows where everything lives and how to search efficiently.

The full evidence inventory with file paths lives in `references/evidence-inventory.md`. Read that file to locate specific sources.

## How to Search

### Single Claim Verification

When asked to verify a specific statement or fact:

1. **Parse** the claim into searchable components -- extract names, dates, amounts, events, and quoted phrases.
2. **Search the email timeline first** -- it is chronologically organized and covers the full dispute arc (master-verified-email-timeline-2025.md).
3. **Search WhatsApp files** -- use the person-based and topic-based search patterns in references/evidence-inventory.md to pick the right files.
4. **Search call transcripts** for verbal admissions, denials, or context that emails lack (verified-call-transcripts.md).
5. **Check the cross-reference overlay** for same-day activity across email and WhatsApp (cross-reference-email-whatsapp.md) -- this often reveals coordination or contradictions.
6. **Assign a verdict**:
   - **VERIFIED**: Documentary evidence directly confirms the claim with minimal ambiguity.
   - **PARTIALLY VERIFIED**: Some evidence supports the claim but gaps or caveats exist.
   - **CONTRADICTED**: Documentary evidence directly contradicts the claim.
   - **UNVERIFIABLE**: No evidence found in any source.

### Document-Wide Cross-Reference

When asked to cross-reference an entire document (a position paper, demand letter, etc.):

1. Extract every factual claim from the document. Read the whole thing -- skipping sections risks missing a vulnerability or an impeachment opportunity.
2. Process each claim through the single-claim workflow.
3. Compile results into an evidence matrix (see output format).
4. Surface contradictions and impeachment opportunities prominently -- these are the most strategically valuable findings.

### Arbitration Evidence Package

When assembling evidence for formal proceedings:

1. Identify all claims that need to be proven under the legal theory.
2. For each claim, build a source chain: email + WhatsApp + call + document. Multi-source corroboration is much stronger than any single source.
3. Organize chronologically -- arbitrators follow timelines better than topic clusters.
4. Note gaps where witness testimony would be needed.
5. Flag evidence that TON does not know exists (held-back) -- this determines what can be used for impeachment versus what has already been disclosed.

## Deployed vs. Held-Back Evidence

This distinction is strategically critical. "Deployed" evidence has been shared with TON through position papers. "Held-back" evidence has not been disclosed and serves as impeachment ammunition.

When reporting findings, always indicate which category the evidence falls into:
- **Deployed**: Cite freely in arguments and correspondence.
- **Held-back**: Recommend whether to deploy now or reserve for impeachment.

The held-back evidence list is in references/evidence-inventory.md under "Held-Back Evidence."

## Output Format

### Evidence Cross-Reference: [Query/Claim]

**Claim**: "[Exact text being verified]"

**Evidence Found**:
| Source | Date | Content | Supports/Contradicts | Strength | Deployed? |
|--------|------|---------|---------------------|----------|-----------|
| [email/WhatsApp/call/doc] | [Date] | [Quote or summary] | S/C | Strong/Moderate/Weak | Yes/No |

**Verdict**: [VERIFIED / PARTIALLY VERIFIED / CONTRADICTED / UNVERIFIABLE]

**Notes**: [Caveats, gaps, additional context, or impeachment potential]

## Integrity

Provide the exact source reference for every finding -- file path plus line number or message date. Vague attributions ("WhatsApp messages suggest...") cannot be verified or cited in proceedings and should not be used.

If evidence is not in the files, report UNVERIFIABLE. Fabricating or extrapolating evidence would undermine credibility of the entire case if counsel relies on a citation that does not exist.

If evidence has already been fact-checked (see fact-check-position-paper.md in the evidence inventory), note that to avoid redundant verification.

All output is confidential and privileged.
