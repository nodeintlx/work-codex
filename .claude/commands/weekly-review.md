---
name: weekly-review
description: Full weekly review — completed tasks, next week calendar, goal progress, carryover items
user-invocable: true
---

# Weekly Review Process

Conduct a comprehensive end-of-week review:

1. **Completed This Week**: Review ~/Work/shared/tasks.yaml for tasks marked done this week. Summarize accomplishments by company.

2. **Carryover Items**: Identify tasks that were due this week but not completed. Recommend whether to carry forward, delegate, or drop.

3. **Next Week Calendar**: Fetch next week's calendar events via Google Calendar MCP. Highlight key meetings and any prep needed.

4. **Goal Progress**: Review ~/Work/shared/goals.yaml. Update progress on key results where applicable. Flag any OKRs at risk.

5. **Email Follow-ups**: Check for sent emails awaiting responses longer than 3 days.

6. **Action Items**: Generate a prioritized task list for next week.

## Output Format

### Weekly Review — Week of [Date]

**Completed This Week**
- NRG Bloom: [items]
- Coldstorm: [items]
- Personal: [items]

**Carried Over** (needs attention)
- [Task]: [reason for delay] → [recommendation]

**Next Week Preview**
| Day | Key Events |
|-----|-----------|
| Mon | [events] |
| ... | ... |

**OKR Check-in**
- [Objective]: [status] — [notes]

**Awaiting Response**
- [Person]: [subject] — sent [date]

**Next Week Priorities**
1. [Priority item]
2. [Priority item]
3. [Priority item]
