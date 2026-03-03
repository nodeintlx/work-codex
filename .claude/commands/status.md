---
name: status
description: Quick dashboard across all active workstreams — litigation, pipeline, funding, tasks, and OKRs
user-invocable: true
---

# Quick Status Dashboard

Generate a concise status overview across ALL active workstreams. This is the "one-glance" view Makir needs to know where everything stands.

## Process
1. Read ~/Work/shared/tasks.yaml — count by status (in_progress, todo, overdue, blocked)
2. Read ~/Work/shared/goals.yaml — check key result statuses
3. Read ~/Work/shared/pipeline.yaml (if exists) — active deals summary
4. Read ~/Work/shared/funding.yaml (if exists) — active applications summary
5. Check Gmail for any unread from key contacts (last 24h)
6. Check calendar for next 48 hours

## Output Format

### Status Dashboard — [Day, Date]

**Litigation**
- [Matter]: [1-line status] — Next: [action] by [date]

**Pipeline**
- [Deal]: [Stage] — Next: [action] by [date]

**Funding**
- [X] active, [Y] approaching deadline — Next: [action]

**Tasks**: [X] in progress, [Y] overdue, [Z] due this week

**OKRs at Risk**
- [Key result]: [why it's at risk]

**Inbox**: [X] unread from key contacts

**Next 48h**: [meetings or deadlines]

**Top 3 Priorities Right Now**
1. [Most urgent/impactful thing]
2. [Second]
3. [Third]

Keep the entire output under 400 words. This is a dashboard, not a report.
