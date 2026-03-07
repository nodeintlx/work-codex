---
name: email-triage
description: >-
  Use this skill to process, categorize, and draft responses for Makir's unread
  emails. Trigger whenever Makir says "check my email", "triage", "inbox",
  "any mail", "what came in", "messages", "anything new", "process my emails",
  "handle my correspondence", invokes /triage, or mentions wanting to catch up
  on communications. Also trigger when Makir asks about specific senders or
  whether anyone has replied to something. If an email-related question comes
  up during any other workflow, use this skill to pull the relevant messages.
  When in doubt, check the inbox — Makir would rather see "nothing new" than
  miss something important.
allowed-tools: Read, Write, Glob, Grep, mcp__google-workspace__*, mcp__memory__*
---

# Email Triage

Process Makir's inbox into a prioritized, actionable summary. The goal is to turn an overwhelming inbox into clear buckets with recommended actions, so Makir spends decision-making energy only on emails that truly need his personal attention.

## Classification Framework

Classify each email into one of five categories:

- **URGENT**: Time-sensitive, from key stakeholders, requires same-day response. Anything mentioning financials, legal matters, or deadlines within 48 hours gets classified here regardless of sender — these topics carry inherent risk if delayed.
- **ACTION**: Needs a response within 48 hours, moderate importance, from known contacts. Draft a response for Makir's review.
- **REVIEW**: Informational but relevant — project updates, industry news, newsletters worth reading. No response needed, but Makir should see it.
- **FYI**: CC'd threads, automated notifications, low-priority updates. Archive candidates.
- **ARCHIVE**: Spam, marketing, irrelevant newsletters. Safe to archive immediately.

**Example classifications:**

| Email | Category | Why |
|-------|----------|-----|
| Dayo Adu: "Position paper final — please review by 5pm" | URGENT | Litigation contact + same-day deadline |
| Eleas Eduga: "Great connecting — here's my availability" | ACTION | Active deal contact, needs scheduling response |
| TCS Quebec: "Your registration is confirmed" | REVIEW | Informational, no action needed, but good to know |
| LinkedIn: "You have 3 new connections" | ARCHIVE | Automated notification, no value |
| Unknown sender: "Partnership opportunity in solar" | REVIEW | Business proposal from unknown sender — worth a look but not urgent since no existing relationship |

## Process

1. **Fetch emails** — Pull unread emails from the last 24 hours via Gmail MCP. If doing a catch-up after a gap, extend to 48-72 hours.

2. **Cross-reference senders** — Check ~/Work/shared/contacts/ for relationship context. Known contacts get priority. Litigation contacts (Dayo, Marley, Sarit, Karl, Julie, Segun) always surface as URGENT.

3. **Classify** — Apply the framework above. When uncertain between URGENT and ACTION, consider: "If Makir doesn't see this until tomorrow, could something go wrong?" If yes, it is URGENT.

4. **Draft responses** — For ACTION items, draft concise responses. Present them to Makir for review before saving as Gmail drafts. Drafts are presented first and only saved after Makir approves — sending an email Makir hasn't reviewed could damage a relationship or create a commitment he didn't intend.

5. **Tag by company** — Label each email as NRG Bloom, Coldstorm, or Personal. This keeps context separated — Makir manages two companies with different stakeholders, and mixing context would be confusing and potentially breach confidentiality.

6. **Present summary** — Use the output format below.

## Output Format

```
### Email Triage — Wednesday, March 5, 2026
**12 new emails processed**

**URGENT** (respond today)
- **Dayo Adu** [NRG Bloom] — RE: Position Paper Final: Attached final version for
  your review before simultaneous exchange. Recommended: Review and confirm by 3pm ET.
- **Sarit Batner** [NRG Bloom] — Conflicts Cleared: Teams link for Friday 10am call
  attached. Recommended: Confirm attendance, share prep doc.

**ACTION** (respond within 48h)
- **Eleas Eduga** [NRG Bloom] — Scheduling: Proposed 3 time slots for engagement call.
  Draft ready: Yes — selects Wednesday 2pm slot.
- **Futurpreneur** [NRG Bloom] — Additional Info Request: Need updated financial
  projections. Draft ready: Yes — acknowledges and commits to Friday delivery.

**REVIEW** (read when available)
- **TCS Quebec** [NRG Bloom] — Registration confirmation and next steps guide.
- **Clean Energy Canada** — Newsletter: New federal cleantech incentives announced.

**FYI / ARCHIVE** (6 emails)
- 3 LinkedIn notifications, 2 marketing emails, 1 CC'd thread (no action needed)

**Drafts Created**: 2 — Review above and approve before I save to Gmail drafts.
```

## Design Decisions

- **Drafts require approval**: Sending an email on Makir's behalf without his review could create unintended commitments, use the wrong tone, or share information he would not want shared. Always draft first, present for review, then save to Gmail drafts only after explicit approval.
- **Financial/legal emails are always URGENT**: These topics carry asymmetric risk — the downside of missing a legal deadline or financial issue far outweighs the cost of over-prioritizing.
- **Unknown senders with proposals go to REVIEW**: Unknown senders have no established trust, so they should not consume Makir's immediate attention. But business proposals could be valuable, so they should not be archived unseen.
- **Company tagging**: NRG Bloom and Coldstorm have separate stakeholders. Mixing context in a response — even accidentally mentioning the wrong company's details — would be unprofessional and potentially harmful.
