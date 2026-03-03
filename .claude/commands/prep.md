---
name: prep
description: Prepare for the next upcoming meeting or a specific meeting — attendee research, talking points, related documents
user-invocable: true
---

# Meeting Prep

Trigger the meeting-prep skill for the next upcoming meeting (or a specified meeting).

## Process
1. Check Google Calendar for the next meeting within 48 hours
2. If Makir specified a meeting (e.g., "/prep McCarthy call"), find that specific event
3. Run the full meeting-prep skill: attendee profiles, recent communications, related documents, talking points
4. Check ~/Work/shared/contacts/ for existing profiles on all attendees
5. Search ~/Work/knowledge/ for any analysis or research related to the meeting topic
6. If the meeting is litigation-related, also run litigation-tracker context

## Enhanced Prep for Key Meeting Types

### Legal Calls (McCarthy, Moroom Africa)
- Include: latest timeline status, outstanding legal questions, evidence inventory, strategic considerations
- Pull from: ~/Work/nrg-bloom/legal/, ~/Work/knowledge/*litigation*.md, ~/Work/knowledge/*damages*.md

### Partnership Meetings (Oando, new prospects)
- Include: company research, attendee LinkedIn context, competitive landscape, proposed deal structure
- Pull from: ~/Work/nrg-bloom/projects/, market research files

### Funding Calls (EDC, TCS, grant bodies)
- Include: program requirements, NRG Bloom eligibility summary, specific ask/scope
- Pull from: ~/Work/nrg-bloom/projects/funding/
