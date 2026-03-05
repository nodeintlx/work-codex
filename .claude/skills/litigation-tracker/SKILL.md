---
name: litigation-tracker
description: "Use this skill to track legal disputes, deadlines, evidence status, and counsel communications for NRG Bloom. Trigger it whenever Makir asks about the TON dispute status, any litigation deadline, the McCarthy Tetrault engagement, evidence readiness, or counsel communications. Also trigger when emails arrive from Dayo Adu, Marley Broda, Sarit Batner, Karl Tabbakh, Julie Peeters, or any mediator. Use it during /status and /gm to populate the litigation section. Use it when preparing for any legal call, when a new legal development surfaces in email, when checking limitation periods, or when Makir says anything about 'the case,' 'TON,' 'arbitration,' 'Dayo,' or 'McCarthy.'"
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, mcp__google-workspace__search_gmail_messages, mcp__google-workspace__get_gmail_message_content, mcp__google-workspace__get_gmail_thread_content, mcp__memory__*
---

# Litigation Tracker

## What This Skill Does

Track every aspect of NRG Bloom's legal matters -- active disputes, upcoming deadlines, evidence inventory status, counsel engagement, and strategic developments. The skill exists because litigation has hard deadlines (limitation periods, filing dates, exchange dates) where missing even one can be catastrophic, and because the dispute touches multiple workstreams (settlement, arbitration prep, counsel engagement) that need a single coherent view.

## Active Matters

The primary active matter is NRG Bloom v. TON Infrastructure. All litigation files live in:
- Dispute timeline and evidence: ~/Work/nrg-bloom/litigation-ton/
- Legal research and analysis: ~/Work/knowledge/
- Case documents: ~/Work/nrg-bloom/legal/

For the full evidence inventory with file paths and search patterns, read `references/evidence-inventory.md`.

## Process

### Step 1: Load Context
- Query Memory MCP for the "TON Dispute" entity and related observations. Memory often has the most recent status without needing to re-read large files.
- Read ~/Work/nrg-bloom/litigation-ton/CONTEXT.md for dispute background (if it exists).
- Check tasks.yaml for all litigation-tagged tasks.

### Step 2: Check Communications
Search Gmail for recent correspondence (last 48 hours) from:
- **Counsel**: Dayo Adu (dayo.adu@moroomafrica.com), Sarit Batner (McCarthy Tetrault)
- **Mediator/Opposing**: Marley Broda, Karl Tabbakh
- **Internal**: Julie Peeters (julie@nrgbloom.com)

Any email from opposing counsel or the mediator should be flagged immediately -- these often contain deadlines or require a response.

### Step 3: Check Deadlines
Scan for any litigation deadline within 7 days. Apply these escalation thresholds:
- **7+ days out**: Inform -- mention in dashboard.
- **3 days out**: Flag with a preparation checklist. Ensure all prerequisites are in motion.
- **1 day out**: Urgent -- surface at the top of any response, even if Makir asked about something else.
- **Overdue**: Critical -- escalate immediately with recommended action.

Limitation periods deserve special handling because they are irrecoverable if missed. Flag them 6 months before expiry, and re-flag monthly until confirmed preserved.

### Step 4: Update
When new developments come in during a session:
1. Update the relevant timeline file in ~/Work/nrg-bloom/litigation-ton/
2. Update tasks.yaml with new action items or status changes
3. Save key facts and status changes to Memory MCP
4. Tell Makir what was updated.

### Step 5: Present Dashboard

## Output Format

### Litigation Status -- [Date]

**Active Matters**: [count]

**[Matter Name]** -- [Status: Negotiation / Pre-Litigation / Filed / Discovery / Trial]

**Critical Deadlines**
| Date | Event | Status | Owner |
|------|-------|--------|-------|
| [Date] | [What] | Confirmed/Pending/At Risk | [Who] |

**Recent Developments** (last 7 days)
- [Date]: [Development summary]

**Pending Actions**
- [ ] [Action item] -- Owner: [who] -- Due: [date]

**Evidence Inventory** (summary -- see references/evidence-inventory.md for full index)
| Category | Items | Status |
|----------|-------|--------|
| WhatsApp chats | [X] verified | Complete/In Progress |
| Email threads | [X] verified | Complete/In Progress |
| Call transcripts | [X] | Complete/In Progress |
| Court records | [list] | Obtained/Needed |

**Counsel Status**
| Firm | Role | Last Contact | Next Step |
|------|------|-------------|-----------|
| [Firm] | [Role] | [Date] | [Action] |

**Strategic Notes**
- [Key strategic consideration]

## Confidentiality

All litigation content is confidential and privileged. Do not share litigation details outside of the NRG Bloom context, and do not include litigation information in Coldstorm outputs or cross-company summaries unless Makir explicitly requests it.

When preparing for lawyer calls, read the relevant analysis files from the evidence inventory (references/evidence-inventory.md) to ensure talking points are grounded in documented evidence rather than memory or summaries.
