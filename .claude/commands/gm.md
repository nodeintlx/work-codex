---
name: gm
description: >-
  Good morning — trigger the daily briefing with calendar, emails, tasks, and priorities.
  Run this when Makir says gm, good morning, or starts a session in the morning.
user-invocable: true
---

Run the morning-review skill to generate Makir's daily briefing.

## Execution

1. **Load memory** — Query Memory MCP for persistent context first.

2. **Calendar** — Use `gws` CLI for token efficiency:
   ```bash
   gws calendar events list --params '{"calendarId": "primary", "timeMin": "TODAY_DATET00:00:00-05:00", "timeMax": "TODAY_DATET23:59:59-05:00", "singleEvents": true, "orderBy": "startTime"}'
   ```
   Fall back to Google Calendar MCP if gws is not authenticated.

3. **Email** — Use `gws` CLI to scan unread:
   ```bash
   gws gmail users messages list --params '{"userId": "me", "q": "is:unread newer_than:1d", "maxResults": 20}'
   ```
   Then fetch details for priority senders only. Fall back to Gmail MCP if needed.

4. **Tasks** — Read ~/Work/shared/tasks.yaml. Flag overdue, due today, due within 3 days.

5. **Goals** — Read ~/Work/shared/goals.yaml. Note at_risk key results.

6. **Synthesize** — Follow the morning-review skill output format. All times in ET. Keep under 500 words.
