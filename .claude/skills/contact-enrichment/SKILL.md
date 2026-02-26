---
name: contact-enrichment
description: Create or update contact records in the shared contacts directory. Enrich with professional context from web searches and email history. Use when meeting new people, after meetings, when asked to add or update a contact, or when building relationship context.
allowed-tools: Read, Write, Glob, Grep, WebSearch, mcp__google-workspace__gmail_search, mcp__memory__*
---

# Contact Enrichment Skill

## Process
1. **Check Existing**: Search ~/Work/shared/contacts/ for existing profile by name or email.
2. **Gather Info**: From provided context (email, meeting, business card), extract key details.
3. **Enrich**: If authorized, do a quick web search for professional context (LinkedIn, company site).
4. **Create/Update**: Write or update the contact JSON file.
5. **Cross-reference**: Check email history for past interactions.

## Contact File Format
Save as ~/Work/shared/contacts/[firstname-lastname].json:

```json
{
  "name": "Full Name",
  "email": "email@example.com",
  "phone": "",
  "company": "Company Name",
  "role": "Title",
  "relationship": "NRG Bloom partner | Coldstorm client | Personal | Industry contact",
  "tags": ["datacenter", "investor", "africa"],
  "location": "City, Country",
  "first_met": "2026-02-22",
  "last_contact": "2026-02-22",
  "next_follow_up": "",
  "interaction_history": [
    {
      "date": "2026-02-22",
      "type": "email | meeting | call | event",
      "summary": "Brief description of interaction"
    }
  ],
  "notes": "Key context about this person and the relationship"
}
```

## Rules
- One file per contact, named as firstname-lastname.json (lowercase, hyphenated)
- Always ask before creating a new contact if the information seems incomplete
- Never include sensitive personal information beyond professional context
- Tag contacts with company relevance: nrg-bloom, coldstorm, or personal
- Update last_contact date whenever a new interaction is logged
