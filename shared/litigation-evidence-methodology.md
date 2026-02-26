# Litigation Evidence Collection & Analysis Methodology

**Purpose:** Systematic framework for collecting, organizing, and verifying evidence in business disputes and litigation. Designed to be repeatable across cases and to prevent evidence gaps.

**Origin:** Lessons learned from NRG Bloom v. TON Infrastructure (Feb 2026). First-pass evidence collection missed critical Axxela relationship emails, an unencrypted JV Agreement in WhatsApp exports, and the $0.03/kWh pricing origin -- all of which were sitting in available data sources but weren't found because the search was counterparty-centric rather than relationship-mapped.

**Last updated:** 2026-02-22

---

## Phase 1: Scope the Universe

Before collecting a single piece of evidence, define what you're looking for and where it might be.

### 1.1 Define the Legal Claims

Start with the legal document (demand letter, contract, complaint) and extract every factual claim that needs proving. Create a numbered checklist:

- Dates (when did X happen?)
- Dollar figures (what was promised, paid, owed?)
- Statements (who said what to whom?)
- Actions (who did what?)
- Omissions (who failed to do what?)

**Each claim becomes a verification target.** The evidence collection process is driven by these targets, not by a general "find everything" approach.

### 1.2 Map Every Entity and Relationship

Do NOT search only for the counterparty. Map every entity that touches the dispute:

| Category | Examples |
|----------|---------|
| **Direct counterparty** | The opposing company and all its personnel |
| **Third-party partners** | Gas suppliers, power companies, community representatives |
| **Brokers / intermediaries** | Anyone who facilitated introductions or deals |
| **Professional advisors** | Lawyers, accountants, consultants on both sides |
| **Community / government** | Local officials, community liaisons, regulatory bodies |
| **Internal team** | Your own employees, directors, investors who may have relevant communications |
| **Financial institutions** | Banks, payment processors, mining pools |

For each entity, list:
- All known email addresses and domains
- All known phone numbers (for WhatsApp searches)
- All known communication channels (email, WhatsApp, Telegram, Slack, etc.)
- The nature of the relationship and its relevance to the claims

### 1.3 Inventory All Data Sources

List every place evidence might exist:

| Source | Search Method | Priority |
|--------|--------------|----------|
| **Gmail** | Gmail MCP search by sender, keyword, date range | Critical |
| **Google Drive** | Drive MCP search for shared documents, spreadsheets, agreements | Critical |
| **WhatsApp exports** | Local file analysis -- chat text AND attachment files | Critical |
| **Signed agreements** | PDF files -- check multiple locations (email attachments, Drive, WhatsApp exports, local folders) | Critical |
| **Financial records** | Invoices, payment confirmations, mining pool dashboards | High |
| **Calendar** | Meeting history, attendee lists | Medium |
| **Social media** | LinkedIn messages, Twitter DMs if relevant | Low |
| **Physical records** | Photos, videos, voice recordings | Medium |

**Important:** The same document may exist in multiple locations in different states (encrypted vs. unencrypted, draft vs. signed, complete vs. redacted). Always check all locations.

---

## Phase 2: Collect by Relationship

For each entity identified in Phase 1, systematically search all data sources.

### 2.1 Email Collection

For each entity/domain:

```
Search 1: from:{domain} -- all inbound emails from this entity
Search 2: to:{domain} -- all outbound emails to this entity
Search 3: {entity name} -- any email mentioning this entity
Search 4: {key terms} from/to:{domain} -- targeted searches for specific topics
```

**Date strategy:** Start with the EARLIEST possible date. Don't assume you know when the relationship began. Search broadly first, then narrow.

**Attachment strategy:** Search `has:attachment from:{domain}` to find all documents shared by that entity. Agreements, proposals, invoices, and technical documents are often attachments, not inline text.

**CC/BCC strategy:** Check who was cc'd on emails over time. Changes in cc lists often reveal circumvention (someone being quietly removed) or escalation (lawyers being added).

### 2.2 WhatsApp Collection

For each WhatsApp export:

1. **Read the full chat text** -- analyze chronologically, extract key quotes and dates
2. **Inventory ALL attachments** in the export directory:
   - PDFs (agreements, invoices, proposals)
   - Images (screenshots, photos of documents, site photos)
   - Videos (site visits, demonstrations)
   - Audio (voice messages, call recordings)
   - Documents (spreadsheets, presentations)
3. **Attempt to read every PDF** -- try multiple methods (Read tool, PyPDF2, pdfplumber). A PDF that appears encrypted in one location may be unencrypted in another.
4. **Cross-reference** -- if the chat mentions "I sent you the agreement," find the corresponding attachment file

### 2.3 Document Collection

For signed agreements and legal documents:

1. Check all possible locations (email attachments, Drive, WhatsApp exports, local files)
2. Attempt extraction from every copy -- different copies may have different encryption states
3. Extract and record: parties, dates, key terms, termination provisions, dispute resolution clauses, exclusivity/non-compete/non-circumvention clauses
4. **Pay special attention to:** termination notice periods, cure periods, governing law, dispute resolution mechanisms -- these are often the most contested provisions

### 2.4 Financial Evidence

For financial claims:

1. Payment records (bank transfers, crypto transactions, invoices)
2. Mining pool records (hashrate allocations, payout history)
3. Operational cost records (land lease payments, staff salaries, equipment purchases)
4. Shared financial models and projections (Google Sheets, Excel files)

---

## Phase 3: Build the Chronological Timeline

### 3.1 Unified Timeline

Create a single chronological document that integrates ALL sources. Each entry must include:

- **Date** (precise, with timezone where relevant)
- **Event description** (factual, not interpretive)
- **Source tag** (e.g., `[WA-MB]`, `[EM]`, `[DOC]`)
- **Key quote** (verbatim where available)
- **Participants** (who was present/copied)

### 3.2 Phase Identification

Group timeline entries into phases that correspond to the narrative arc of the dispute. Common patterns:

1. Relationship formation (promises, agreements)
2. Value creation (work performed, introductions made)
3. First signs of trouble (missed payments, broken commitments)
4. Escalation (disputes, threats, renegotiation)
5. Circumvention / bad faith (going behind someone's back)
6. Crisis (breakdowns, shutdowns, third-party interference)
7. Termination
8. Post-termination (demand letters, responses, negotiation)

### 3.3 Gap Detection

As you build the timeline, flag:

- **Date gaps:** Periods where no evidence exists but events clearly occurred
- **Source gaps:** Events mentioned in one source but not corroborated by others
- **Missing documents:** Agreements or communications referenced but not found
- **Contradictions:** Different sources telling different stories about the same event

---

## Phase 4: Verify Against Legal Claims

### 4.1 Claim-by-Claim Cross-Reference

Create a verification document that maps every legal claim to specific evidence:

```
### Claim X.X: [Quoted claim from legal document]

**Rating:** VERIFIED / SUPPORTED / PARTIALLY VERIFIED / VERBAL ONLY / GAP

**Evidence:**
- [Source tag] [Date]: [Specific quote or document reference]
- [Source tag] [Date]: [Corroborating evidence]

**Gaps:**
- [What's missing and where to look for it]
```

### 4.2 Rating System

| Rating | Definition | Action |
|--------|-----------|--------|
| **VERIFIED** | Direct quote, document, or contemporaneous record located | None -- evidence is solid |
| **SUPPORTED** | Consistent with multiple sources but no single direct proof | Document the supporting evidence chain |
| **PARTIALLY VERIFIED** | Some evidence found but not all details confirmed | Targeted search for missing details |
| **VERBAL ONLY** | Based on in-person statements requiring witness testimony | Obtain written statement / affidavit |
| **GAP** | No evidence located in collected materials | Urgent -- search additional sources |
| **DATE CORRECTION** | Evidence found but dates don't match legal document | Flag for lawyer to correct |

### 4.3 Scorecard

Maintain a scorecard showing verification rates by section. Target: 80%+ verified before proceeding to legal action.

---

## Phase 5: Deep Dive on Weak Sections

### 5.1 Targeted Research

For every claim rated below VERIFIED:

1. Re-search Gmail with more specific queries (exact dates, names, subject lines)
2. Check WhatsApp exports for the specific timeframe
3. Look for the evidence in a different source than where you first searched
4. Check if the counterparty's own communications confirm the claim (admissions, non-denials)

### 5.2 Cross-Source Triangulation

When one source mentions an event, search for it in every other source:

- WhatsApp mention of "the Axxela meeting" → search Gmail for meeting minutes on that date
- Email reference to "as discussed on the call" → check WhatsApp for call logs on that date
- Agreement reference to "Addendum No. 1 dated July 3" → search for the actual addendum

### 5.3 Non-Denial Analysis

When the opposing party responds to a demand letter or complaint, analyze what they DO NOT deny. Non-denials are powerful evidence because they suggest the claim is true but the counterparty has no defense.

---

## Phase 6: Organize for the Lawyer

### 6.1 Folder Structure

```
litigation-{counterparty}/
  CONTEXT.md              -- Entry point: narrative, key people, file inventory
  unified-chronology.md   -- Master timeline, all sources
  {source}-analysis.md    -- One analysis file per major source
  {relationship}-analysis.md -- Dedicated files for key third-party relationships
  demand-letter-cross-reference.md -- Claim verification document
  tactical-analysis.md    -- Legal strategy analysis
  *.pdf                   -- Agreements, demand letters, responses
  {whatsapp-export}/      -- Raw chat exports with attachments
```

### 6.2 CONTEXT.md Requirements

Every litigation folder must have a CONTEXT.md that serves as the entry point. It must include:

1. **Narrative summary** -- what happened, in plain language
2. **Core pattern** -- the opponent's behavioral pattern distilled
3. **Key people table** -- every relevant person with role and alignment
4. **Evidence file inventory** -- every file in the folder with description
5. **Current legal posture** -- phase, positions, deadlines
6. **Cross-references** -- links to related cases or matters

### 6.3 Handoff Checklist

Before handing the folder to a lawyer, verify:

- [ ] Every factual claim in the demand letter is cross-referenced to evidence
- [ ] All gaps are documented with recommendations for filling them
- [ ] Key quotes are verbatim with source tags and dates
- [ ] Agreements have been read and key clauses extracted
- [ ] The opposing party's response has been analyzed for non-denials
- [ ] A tactical analysis exists identifying strengths and vulnerabilities
- [ ] All dates are accurate and timezone-consistent

---

## Common Mistakes to Avoid

1. **Searching only the counterparty's email domain.** Third-party relationships (suppliers, community contacts, brokers) often hold the most important evidence.

2. **Assuming encrypted PDFs can't be read.** The same document may exist unencrypted in WhatsApp exports, Google Drive, or email attachments. Check every copy.

3. **Not reading WhatsApp attachment directories.** The chat text is only half the evidence. Agreements, invoices, photos, and technical documents are in the attachment files.

4. **Collecting evidence first, then reading the legal document.** The legal document should drive the evidence collection, not the other way around. Start with the claims, then find the evidence.

5. **Treating the first pass as complete.** The first pass catches obvious evidence. The second pass, guided by the legal claims, finds the evidence that wins the case. Always do both.

6. **Not tracking who is cc'd on emails.** Changes in cc lists over time reveal circumvention, escalation, and shifting alliances. This was the key evidence in the Axxela circumvention: Makir was cc'd through June 17, removed June 24-July 2, then re-added July 3.

7. **Not checking the counterparty's response for non-denials.** What they don't deny is often as important as what they do deny.

8. **Organizing by source instead of by relationship.** A file called "email-analysis.md" that covers all emails is less useful than separate analyses for each key relationship (Axxela, Agnes, Nelson, etc.).

---

## Application Beyond Litigation

This methodology applies to any business relationship that requires evidence management:

- **Partnership due diligence** -- before entering a deal, document the relationship origin and terms
- **Investor relations** -- maintain a clear record of commitments, milestones, and communications
- **Regulatory compliance** -- ensure all required communications and approvals are documented
- **Contract disputes** -- have evidence ready before a dispute becomes litigation
- **IP protection** -- document the origin and development of proprietary relationships and opportunities

**The best time to collect evidence is before you need it. The second best time is systematically, with a methodology.**

---

*Framework developed from NRG Bloom v. TON Infrastructure evidence collection (Feb 2026). To be updated as new cases provide additional lessons.*
