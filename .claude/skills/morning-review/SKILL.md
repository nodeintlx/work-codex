---
name: morning-review
description: Generate a personalized morning briefing by analyzing today's calendar events, unread priority emails, pending tasks, and action items. Use when Makir says good morning, asks about his day, requests a daily overview, or invokes /gm.
allowed-tools: Read, Bash, Glob, Grep, WebSearch, mcp__google-workspace__*, mcp__memory__*
---

# Morning Review Skill

## Process
1. **Calendar**: Fetch today's calendar events via Google Calendar MCP. List all meetings with times, attendees, and any attached agendas.
2. **Email**: Check for unread priority emails via Gmail MCP. Focus on emails from known contacts (cross-reference ~/Work/shared/contacts/) and anything flagged urgent.
3. **Tasks**: Read ~/Work/shared/tasks.yaml for pending and overdue items. Highlight anything due today or past due.
4. **Goals**: Read ~/Work/shared/goals.yaml for quarterly context. Note any key results that need attention.
5. **Synthesize**: Combine into a structured briefing.

## Output Format

### Good Morning, Makir — [Day, Month Date, Year]

**Today's Focus**: [1-sentence summary based on calendar + priorities]

**Schedule** (X meetings, Y hours of focus time available)
| Time | Event | Notes |
|------|-------|-------|
| HH:MM | Meeting name | Key attendee or context |

**Priority Emails** (X need response)
- **[Sender]**: [Subject] — [1-line summary] — [Urgency: High/Medium]

**Pending Actions**
- [ ] [Task from yesterday or overdue items]
- [ ] [Follow-ups from recent meetings]

**This Week's OKR Progress**
- [Company]: [Quick status on relevant quarterly goals]

## Rules
- All times in Eastern Time (ET)
- If MCP servers are unavailable, work with local files only and note what couldn't be checked
- Keep the briefing under 500 words
- Prioritize actionability over completeness
