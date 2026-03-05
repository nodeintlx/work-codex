---
name: meeting-prep
description: >-
  Use this skill to prepare a pre-meeting brief with attendee context, agenda
  review, related documents, and suggested talking points. Trigger whenever Makir
  says "prep me for", "brief me on the call", "who am I meeting", "about to hop
  on a call", "meeting with [name]", "get me ready for", "what should I know
  before", invokes /prep, or asks about an upcoming meeting in detail. Also
  trigger proactively during the morning review if a meeting is within the next
  2 hours. If Makir mentions a person's name and asks "what's the context" or
  "remind me about them", this skill may also be relevant if a meeting is
  imminent. When no specific meeting is named, prep for the next upcoming one.
allowed-tools: Read, Glob, Grep, WebSearch, mcp__google-workspace__*, mcp__memory__*
---

# Meeting Prep

Prepare a comprehensive brief so Makir walks into every meeting informed, confident, and ready to drive the conversation. A good brief eliminates "let me get back to you on that" moments and ensures Makir controls the narrative.

## Process

1. **Meeting details** — Get the specific meeting from Calendar MCP: time, attendees, agenda, attached docs. If no meeting is specified, prep for the next upcoming one — Makir is probably asking because something is imminent.

2. **Attendee context** — For each attendee:
   - Check ~/Work/shared/contacts/ for existing profiles
   - Check Memory MCP for relationship history and past interactions
   - If no profile exists, do a quick web search for professional context (LinkedIn, company website)
   - Note the last interaction date — if it has been a while, Makir may want to acknowledge that

3. **Related communications** — Search recent emails with attendees for context on ongoing discussions. Look for:
   - Open questions from previous exchanges
   - Commitments either party made
   - Tone and relationship dynamics

4. **Related documents** — Search ~/Work/ for documents related to the meeting topic. Include links to any analysis, research, or prep materials that are relevant.

5. **Talking points** — Based on all context, suggest 3-5 talking points or questions. Frame them as strategic recommendations, not just topics — explain what Makir should aim to get out of each point.

## Output Format

**Example:**

```
### Meeting Brief: McCarthy Tetrault — Introductory Call
**Date/Time**: Friday, March 6, 2026 at 10:00 AM ET
**Duration**: 60 minutes
**Location**: Microsoft Teams (link in calendar invite)

**Attendees**
| Name | Role | Relationship | Last Contact |
|------|------|-------------|--------------|
| Sarit Batner | Partner, McCarthy Tetrault | New — intro via Dayo | Feb 28 (email) |
| Dayo Adu | Counsel, Moroom Africa | NRG Bloom legal counsel | Mar 4 (email) |

**Context & Background**
- This is the introductory call to assess whether McCarthy can serve as
  litigation counsel for the TON Infrastructure dispute
- Sarit cleared conflicts on Mar 3 — TON Infrastructure Ltd. is not a client
- Key documents ready to share: Alberta litigation analysis, expenditure ledger,
  Phoenix Trading prior lawsuit analysis

**Recent Communications**
- Feb 28: Sarit requested counterparty name for conflicts check
- Mar 3: Conflicts cleared, Teams link circulated
- Mar 4: Dayo confirmed position paper exchange happening Mar 5

**Suggested Talking Points**
1. **Limitation period audit** — Ask when the 2-year clock started running.
   This determines urgency of any protective filing. (Strategic goal: understand
   if there is a hard deadline driving next steps.)
2. **Arbitration clause (Section 7)** — Get Sarit's read on enforceability and
   whether Alberta courts would compel arbitration. (Strategic goal: know whether
   litigation or arbitration is the likely path.)
3. **Phoenix Trading prior lawsuit** — Present Tyler's 2022 U.S. lawsuit as
   pattern-of-conduct evidence. Ask about admissibility as similar fact evidence
   under Alberta rules. (Strategic goal: establish whether this strengthens
   punitive damages claim.)
4. **Fee structure** — Confirm Dayo absorbs McCarthy costs per existing
   arrangement. (Strategic goal: remove financial ambiguity before engagement
   deepens.)

**Prep Actions**
- [ ] Review position paper exchange results (if received before call)
- [ ] Have expenditure ledger and damages analysis ready to screen-share
- [ ] Confirm Teams link works
```

## Design Decisions

- **Data isolation between companies**: Coldstorm client information should not appear in NRG Bloom meeting preps, and vice versa. Makir runs two separate companies with different stakeholders. If a Coldstorm client's name appeared in an NRG Bloom meeting brief that was screen-shared or forwarded, it would breach confidentiality and damage trust. Always check which company a meeting belongs to and scope your document search accordingly.
- **600-word cap**: Briefs should be thorough but scannable. If Makir needs to spend 10 minutes reading a prep doc, it has failed its purpose. Lead with the most important context and use the talking points to drive focus.
- **Strategic framing for talking points**: Simply listing "topics to discuss" is not useful — Makir already knows the topics. The value is in framing what he should aim to get out of each discussion point. Include the strategic goal in parentheses.
- **Flag conflicts of interest**: If an attendee has relationships with both NRG Bloom and Coldstorm contacts, or appears in litigation-related contexts, flag it explicitly. Makir needs to know before the meeting, not during it.
