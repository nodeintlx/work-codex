---
name: weekly-review
description: >-
  Full weekly review — completed tasks, next week calendar, goal progress,
  carryover items, stale follow-ups, and next week priorities.
user-invocable: true
---

Conduct a comprehensive end-of-week review across all workstreams.

## Execution

1. **Completed this week** — Read ~/Work/shared/tasks.yaml. List all tasks marked done this week, grouped by company.

2. **Carryover items** — Identify tasks that were due this week but not completed. Recommend: carry forward, delegate, or drop.

3. **Next week calendar** — Use `gws` CLI:
   ```bash
   gws calendar events list --params '{"calendarId": "primary", "timeMin": "NEXT_MON_DATET00:00:00-05:00", "timeMax": "NEXT_FRI_DATET23:59:59-05:00", "singleEvents": true, "orderBy": "startTime"}'
   ```
   Highlight key meetings and prep needed.

4. **Goal progress** — Read ~/Work/shared/goals.yaml. Update key results where progress occurred. Flag any OKRs at risk with specific reasons.

5. **Stale follow-ups** — Search sent emails for unreplied threads:
   ```bash
   gws gmail users messages list --params '{"userId": "me", "q": "in:sent newer_than:14d"}'
   ```
   Flag any sent 3+ days ago with no response.

6. **Next week priorities** — Generate a ranked priority list for next week based on deadlines, OKR impact, and momentum.

7. **Save context** — Update Memory MCP with key decisions and status changes from the review. Update tasks.yaml with carryover items and new priorities.

## Output Format

### Weekly Review — Week of [Date]

**Wins This Week**
- NRG Bloom: [items]
- Coldstorm: [items]

**Carried Over** (needs attention)
- [Task]: [reason] -> [recommendation]

**Next Week Preview**
| Day | Key Events |
|-----|-----------|
| Mon | [events] |

**OKR Check-in**
- [Objective]: [status] — [what changed]

**Awaiting Response** (3+ days)
| Sent To | Subject | Days Waiting | Action |
|---------|---------|-------------|--------|

**Next Week Priorities**
1. [Priority — why it matters]
2. [Priority — why it matters]
3. [Priority — why it matters]
