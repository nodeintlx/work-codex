---
name: litigation-tracker
description: Track legal disputes, deadlines, evidence inventory, and counsel communications. Monitor the TON Infrastructure dispute and any future legal matters. Use when checking litigation status, preparing for legal calls, updating dispute timelines, or when legal developments arise in emails.
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, mcp__google-workspace__gmail_*, mcp__memory__*
---

# Litigation Tracker Skill

## Active Matters
Track all legal matters in their respective files:
- TON dispute timeline: ~/Work/nrg-bloom/legal/ton-dispute-timeline-*.md
- Evidence: ~/Work/nrg-bloom/legal/
- Analysis files: ~/Work/knowledge/*litigation*.md, ~/Work/knowledge/*damages*.md

## Process
1. **Load Memory** — query Memory MCP for "TON Dispute" entity and related observations
2. **Read timeline** — get current state of dispute from latest timeline file
3. **Check Gmail** — search for emails from Dayo Adu, Marley Broda, Sarit Batner, Karl Tabbakh, Julie Peeters in last 48 hours
4. **Check deadlines** — flag any litigation deadline within 7 days
5. **Update** timeline and tasks.yaml with any new developments
6. **Present** litigation status dashboard

## Output Format

### Litigation Status — [Date]

**Active Matters**: [X]

**[Matter Name]** — [Status: Negotiation / Pre-Litigation / Filed / Discovery / Trial]

**Critical Deadlines**
| Date | Event | Status | Owner |
|------|-------|--------|-------|
| [Date] | [What] | [Confirmed/Pending/At Risk] | [Who] |

**Recent Developments** (last 7 days)
- [Date]: [Development summary]

**Pending Actions**
- [ ] [Action item] — Owner: [who] — Due: [date]

**Evidence Inventory**
| Category | Items | Status |
|----------|-------|--------|
| WhatsApp chats | [X] analyzed | Complete/In Progress |
| Email threads | [X] analyzed | Complete/In Progress |
| Documents | [list] | Collected/Needed |
| Court records | [list] | Obtained/Needed |

**Counsel Status**
| Firm | Role | Last Contact | Next Step |
|------|------|-------------|-----------|
| [Firm] | [Role] | [Date] | [Action] |

**Strategic Notes**
- [Key strategic consideration]

## Deadline Alert Thresholds
- **7+ days out**: Inform
- **3 days out**: Flag with preparation checklist
- **1 day out**: URGENT — surface at top of any response
- **Overdue**: CRITICAL — escalate immediately

## Rules
- NEVER share litigation details outside of NRG Bloom context
- All litigation content is CONFIDENTIAL and PRIVILEGED
- When new evidence or developments come in, update:
  1. Timeline file
  2. tasks.yaml
  3. Memory MCP (add observations)
- Flag any email from opposing counsel (TON) immediately — don't wait for Makir to ask
- When preparing for lawyer calls, cross-reference all analysis files in ~/Work/knowledge/
- Track limitation periods and flag 6 months before expiry
