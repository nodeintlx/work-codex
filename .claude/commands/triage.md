---
name: triage
description: >-
  Triage the email inbox — categorize and process unread emails by urgency,
  draft responses, and present actionable summary.
user-invocable: true
---

Run the email-triage skill to process Makir's unread emails.

## Execution

1. **Fetch emails** — Use `gws` CLI for efficient bulk fetch:
   ```bash
   gws gmail users messages list --params '{"userId": "me", "q": "is:unread", "maxResults": 50}'
   ```
   Then fetch metadata for each message. Fall back to Gmail MCP if gws unavailable.

2. **Classify** — Apply the email-triage skill's 5-category framework (URGENT / ACTION / REVIEW / FYI / ARCHIVE).

3. **Cross-reference** — Check ~/Work/shared/contacts/ for sender context. Litigation contacts always surface as URGENT.

4. **Draft responses** — For ACTION items, draft concise responses. Present for Makir's review before saving as Gmail drafts.

5. **Present** — Follow the email-triage skill output format. Tag each email by company (NRG Bloom / Coldstorm / Personal).

Never send emails — drafts only, and only after Makir approves.
