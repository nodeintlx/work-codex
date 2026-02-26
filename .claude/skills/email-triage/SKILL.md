---
name: email-triage
description: Process and categorize unread emails by urgency and required action. Draft responses for routine inquiries. Flag items needing Makir's personal attention. Use when asked to check email, triage inbox, process messages, or handle correspondence for NRG Bloom or Coldstorm AI.
allowed-tools: Read, Write, Glob, Grep, mcp__google-workspace__gmail_*, mcp__memory__*
---

# Email Triage Skill

## Classification Framework
- **URGENT**: Time-sensitive, from key stakeholders, requires same-day response. Includes anything mentioning financials, legal, M&A, or deadlines within 48h.
- **ACTION**: Needs response within 48h, moderate importance, from known contacts.
- **REVIEW**: Informational but relevant — project updates, industry news, newsletters worth reading.
- **FYI**: CC'd threads, automated notifications, low-priority updates. Archive candidates.
- **ARCHIVE**: Spam, marketing, irrelevant newsletters. Safe to archive immediately.

## Process
1. Fetch unread emails from the last 24 hours via Gmail MCP
2. Cross-reference senders against ~/Work/shared/contacts/ for relationship context
3. Classify each email using the framework above
4. For ACTION items: draft concise responses (save as drafts, NEVER send)
5. Present summary with recommended actions

## Output Format

### Email Triage — [Date]
**[X] new emails processed**

**URGENT** (respond today)
- **[Sender]** — [Subject]: [1-line summary]. Recommended action: [action]

**ACTION** (respond within 48h)
- **[Sender]** — [Subject]: [1-line summary]. Draft ready: [yes/no]

**REVIEW** (read when available)
- **[Sender]** — [Subject]: [1-line summary]

**FYI / ARCHIVE** ([X] emails)
- [Brief summary of what was filed]

**Drafts Created**: [X] — Review and approve before sending.

## Rules
- NEVER auto-send any email
- Always present drafts for Makir's review before saving to Gmail drafts
- Flag any email mentioning financials, legal matters, or M&A as URGENT regardless of sender
- Respect company separation: tag emails as NRG Bloom or Coldstorm when applicable
- Unknown senders with business proposals → classify as REVIEW, not URGENT
