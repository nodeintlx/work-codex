---
name: prep
description: >-
  Prepare for the next upcoming meeting or a specific meeting — attendee research,
  talking points, related documents, and strategic recommendations.
user-invocable: true
---

Trigger the meeting-prep skill for the next upcoming meeting or a specified one.

## Execution

1. **Find the meeting** — Use `gws` CLI to check calendar:
   ```bash
   gws calendar events list --params '{"calendarId": "primary", "timeMin": "NOW_ISO", "timeMax": "48H_LATER_ISO", "singleEvents": true, "orderBy": "startTime"}'
   ```
   If Makir specified a meeting (e.g., "/prep McCarthy call"), search for that specific event.

2. **Run meeting-prep skill** — Full attendee profiles, recent communications, related documents, talking points.

3. **Check contacts** — Load attendee profiles from ~/Work/shared/contacts/.

4. **Search related files** — Search ~/Work/knowledge/ and project directories for relevant analysis.

5. **Type-specific prep**:
   - **Legal calls** (McCarthy, Moroom): Include litigation status, legal theories, evidence inventory, strategic questions. Trigger litigation-tracker and arbitration-readiness skills for context.
   - **Partnership meetings** (Oando, prospects): Include company research, competitive landscape, proposed deal structure. Trigger pipeline-tracker for context.
   - **Funding calls** (EDC, TCS, IRAP): Include program requirements, eligibility summary, specific ask. Trigger grant-tracker for context.

6. **Output** — Follow the meeting-prep skill format. Include strategic goals for each talking point.
