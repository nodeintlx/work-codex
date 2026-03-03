---
name: followup
description: Check what needs follow-up — stale emails awaiting response, overdue tasks, idle workstreams, and contacts who haven't replied
user-invocable: true
---

# Follow-Up Check

Identify everything that's fallen through the cracks or needs a nudge.

## Process
1. **Stale Emails**: Search Gmail for emails SENT by makir@nrgbloom.com in the last 14 days. For each, check if there's been a reply. Flag any with no response after 3+ days.
2. **Overdue Tasks**: Read tasks.yaml — list all tasks past their due date with days overdue.
3. **Idle Workstreams**: Check tasks.yaml for any in_progress task with no update in 5+ days.
4. **Contact Follow-ups**: Check ~/Work/shared/contacts/ for any contact with a next_follow_up date that has passed.
5. **Waiting-on-Others**: List items where Makir is waiting for someone else to act (counterparty-owned actions).

## Output Format

### Follow-Up Report — [Date]

**Emails Awaiting Response** (sent by Makir, no reply 3+ days)
| Sent To | Subject | Sent Date | Days Waiting | Suggested Action |
|---------|---------|-----------|-------------|-----------------|
| [Name] | [Subject] | [Date] | [X] | [Nudge / Call / Escalate] |

**Overdue Tasks**
| Task | Due | Days Overdue | Impact |
|------|-----|-------------|--------|
| [Task] | [Date] | [X] | [What's blocked by this] |

**Idle Workstreams** (no activity 5+ days)
- [Workstream]: Last touched [date] — [recommended action]

**Waiting on Others**
| Who | What | Since | Suggested Nudge |
|-----|------|-------|----------------|
| [Person] | [Item] | [Date] | [Draft nudge or call] |

**Recommended Priority Actions**
1. [Most impactful follow-up to do right now]
2. [Second]
3. [Third]

For each recommended action, offer to draft a follow-up email or suggest exact wording for a call/text.
