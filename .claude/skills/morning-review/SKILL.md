---
name: morning-review
description: >-
  Use this skill to generate Makir's daily morning briefing combining calendar,
  emails, tasks, and OKR progress into a single actionable overview. Trigger this
  skill whenever Makir says good morning, gm, asks "what's on my plate today",
  "what do I have today", "daily overview", "start of day", "brief me", "what's
  happening today", "run me through today", invokes /gm, or opens a conversation
  in the morning without a specific request. Also trigger when Makir asks about
  his schedule, priorities, or agenda for the day. When in doubt about whether
  to trigger, trigger — a morning briefing is never unwelcome at the start of a
  session.
allowed-tools: Read, Bash, Glob, Grep, WebSearch, mcp__google-workspace__*, mcp__memory__*
---

# Morning Review

Generate a daily briefing that gives Makir a full picture of his day in under 2 minutes of reading. The goal is to eliminate the need for him to check calendar, email, and tasks separately — one briefing covers everything.

## Process

1. **Load memory** — Query Memory MCP for persistent context (active deals, litigation status, key relationships). This avoids re-reading large files unnecessarily and gives you context for interpreting what matters today.

2. **Calendar** — Fetch today's events via Google Calendar MCP. List all meetings with times (ET), attendees, and any attached agendas. If a meeting is within the next 2 hours, flag it prominently so Makir can prep.

3. **Email** — Check for unread priority emails via Gmail MCP. Focus on:
   - Emails from known contacts (cross-reference ~/Work/shared/contacts/)
   - Anything flagged urgent or mentioning deadlines, legal, financial terms
   - Emails from litigation contacts (Dayo, Marley, Sarit, Karl, Julie) always surface first — litigation moves fast and missing a 24-hour window can be costly

4. **Tasks** — Read ~/Work/shared/tasks.yaml. Surface:
   - Overdue items (these go at the top — they represent accumulated risk)
   - Due today (action needed now)
   - Due within 3 days (needs prep or follow-up)
   - Blocked items (flag the blocker so Makir can unblock)

5. **Goals** — Read ~/Work/shared/goals.yaml. Note any key results marked "at_risk" — these are the things that could derail the quarter if ignored.

6. **Synthesize** — Combine into the briefing format below. Lead with the single most important thing Makir should focus on today.

## Output Format

**Example:**

```
### Good Morning, Makir — Wednesday, March 5, 2026

**Today's Focus**: Position paper simultaneous exchange with TON — review and
submit by end of day. McCarthy call prep needs to be finalized for Friday.

---

**Alerts** (items needing immediate attention)
- EDC call is 5 days overdue — scope working capital and political risk insurance
- SR&ED specialist search still open — Leyton/Ayming didn't work out

**Schedule** (3 meetings, 4 hours of focus time available)
| Time (ET) | Event | Notes |
|-----------|-------|-------|
| 10:00 AM  | TCS follow-up call | Prep: review registration status |
| 2:00 PM   | Team sync | Agenda: Oando call debrief |

**Priority Emails** (2 need response)
- **Dayo Adu**: RE: Position Paper — Final draft attached for review — High
- **Eleas Eduga**: Scheduling engagement call — Proposed 3 times next week — Medium

**Pending Actions**
- [ ] Call EDC (overdue since Feb 28)
- [ ] Finalize McCarthy call brief (due tomorrow)
- [ ] Follow up with accountant on tax filings

**OKR Check-in**
- NRG Bloom Obj 1 (TON dispute): On track — position exchange today
- NRG Bloom Obj 3 (Funding): At risk — SR&ED and EDC calls still not made
- Coldstorm: No movement — all KRs still not_started
```

## Design Decisions

- **Times in ET**: Makir operates in Eastern Time. Mixing timezones creates confusion and missed meetings.
- **500-word cap**: The briefing should be scannable in under 2 minutes. If it runs longer, Makir will skim and miss things. Prioritize ruthlessly — put the most important items first and cut the rest.
- **Actionability over completeness**: Every line should either tell Makir what to do or inform a decision. "FYI" items belong in email triage, not the morning briefing.
- **Fallback gracefully**: If MCP servers are unavailable (network issues, auth expiry), work with local files and note what could not be checked. A partial briefing is better than no briefing.
