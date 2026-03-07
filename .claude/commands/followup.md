---
name: followup
description: >-
  Check what needs follow-up — stale emails awaiting response, overdue tasks,
  idle workstreams, and contacts who haven't replied.
user-invocable: true
---

Identify everything that has fallen through the cracks or needs a nudge.

## Execution

1. **Stale emails** — Search sent emails via `gws` CLI:
   ```bash
   gws gmail users messages list --params '{"userId": "me", "q": "in:sent newer_than:14d"}'
   ```
   For each sent email, check if there is a reply. Flag any with no response after 3+ days.

2. **Overdue tasks** — Read ~/Work/shared/tasks.yaml. List all tasks past their due date with days overdue and what is blocked by the delay.

3. **Idle workstreams** — Check tasks.yaml for any in_progress task not updated in 5+ days.

4. **Contact follow-ups** — Check ~/Work/shared/contacts/ for any contact with a next_follow_up date that has passed.

5. **Waiting on others** — List items where Makir is waiting for someone else to act (counterparty-owned actions from pipeline.yaml and tasks.yaml).

6. **Recommend actions** — For each stale item, recommend: nudge email, phone call, escalate, or drop. Offer to draft follow-up emails.

## Output Format

### Follow-Up Report — [Date]

**Emails Awaiting Response** (3+ days)
| Sent To | Subject | Days Waiting | Action |
|---------|---------|-------------|--------|

**Overdue Tasks**
| Task | Due | Days Overdue | Impact |
|------|-----|-------------|--------|

**Idle Workstreams** (5+ days)
- [Workstream]: Last touched [date] — [action]

**Waiting on Others**
| Who | What | Since | Nudge |
|-----|------|-------|-------|

**Priority Actions**
1. [Most impactful follow-up]
2. [Second]
3. [Third]
