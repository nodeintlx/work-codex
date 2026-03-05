---
name: status
description: >-
  Quick dashboard across all active workstreams — litigation, pipeline, funding,
  tasks, and OKRs. One-glance view of where everything stands.
user-invocable: true
---

Generate a concise status dashboard across ALL active workstreams. This is the "one-glance" view — keep it under 400 words.

## Execution

1. **Tasks** — Read ~/Work/shared/tasks.yaml. Count by status (in_progress, todo, overdue, blocked).

2. **Goals** — Read ~/Work/shared/goals.yaml. List at_risk key results.

3. **Pipeline** — Read ~/Work/shared/pipeline.yaml (if exists). Active deals summary.

4. **Funding** — Read ~/Work/shared/funding.yaml (if exists). Active applications summary.

5. **Email** — Quick unread check via `gws` CLI:
   ```bash
   gws gmail users messages list --params '{"userId": "me", "q": "is:unread newer_than:1d", "maxResults": 10}'
   ```

6. **Calendar** — Next 48 hours via `gws` CLI.

7. **Litigation** — Trigger litigation-tracker skill for status line.

8. **Settlement** — Trigger settlement-tracker skill for current positions.

## Output Format

### Status Dashboard — [Day, Date]

**Litigation**: [1-line status] — Next: [action] by [date]
**Settlement**: [Current offer gap] — [ABOVE/BELOW floor]
**Pipeline**: [X] active deals — Next: [action]
**Funding**: [X] active, [Y] approaching deadline
**Tasks**: [X] in progress, [Y] overdue, [Z] due this week
**OKRs at Risk**: [list]
**Inbox**: [X] unread from key contacts
**Next 48h**: [meetings or deadlines]

**Top 3 Priorities Right Now**
1. [Most urgent/impactful]
2. [Second]
3. [Third]
