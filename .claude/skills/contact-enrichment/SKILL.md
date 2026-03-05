---
name: contact-enrichment
description: >-
  Use this skill to create or update contact records with professional context
  from web searches and email history. Trigger whenever Makir says "who is
  [name]", "add this contact", "update their info", "look up [name]", "what do
  we know about [person]", or asks about someone's background. Also trigger
  after meetings (to update last_contact and add interaction notes), when new
  names appear in emails during triage, when Makir forwards a business card or
  LinkedIn profile, or when building relationship context for deal prep. If a
  name comes up in conversation that does not have a contact file yet, suggest
  creating one — relationship context compounds over time and the sooner a
  record exists, the more useful it becomes.
allowed-tools: Read, Write, Glob, Grep, WebSearch, mcp__google-workspace__search_gmail_messages, mcp__google-workspace__get_gmail_message_content, mcp__memory__*
---

# Contact Enrichment

Create and maintain contact records so Makir always has relationship context at his fingertips. A well-maintained contact file turns "who was that person again?" into instant recall — previous interactions, company context, and what matters to them.

## Process

1. **Check existing** — Search ~/Work/shared/contacts/ for an existing profile by name or email. If one exists, update it rather than creating a duplicate.

2. **Gather info** — From the provided context (email, meeting, business card, conversation), extract all available details: name, email, phone, company, role, location, how they connect to Makir.

3. **Enrich** — Do a web search for professional context (LinkedIn profile, company website, recent news mentions). This adds depth that helps Makir prepare for future interactions — knowing someone's background and recent activities makes conversations more substantive.

4. **Check email history** — Search Gmail for past interactions with this person. Note the first contact date, most recent exchange, and any open threads or commitments.

5. **Create or update** — Write or update the contact JSON file. If creating a new record and key information is missing (no email, no company), flag this and ask Makir before saving — an incomplete record is better than no record, but confirm the basics are right.

6. **Update memory** — Save key relationship facts to Memory MCP so they persist across sessions.

## Contact File Schema

Save as `~/Work/shared/contacts/firstname-lastname.json` (lowercase, hyphenated):

```json
{
  "name": "Eleas Eduga",
  "email": "eleas.eduga@oandoenergy.com",
  "phone": "+234-XXX-XXX-XXXX",
  "company": "Oando Clean Energy",
  "role": "Head of Gas Business",
  "relationship": "NRG Bloom prospect",
  "tags": ["energy", "nigeria", "gas-to-power", "oando"],
  "location": "Lagos, Nigeria",
  "first_met": "2026-02-26",
  "last_contact": "2026-03-01",
  "next_follow_up": "2026-03-07",
  "interaction_history": [
    {
      "date": "2026-02-26",
      "type": "email",
      "summary": "Introduced by Chioma Anyamele to schedule engagement call"
    },
    {
      "date": "2026-03-01",
      "type": "email",
      "summary": "Proposed 3 time slots for intro call next week"
    }
  ],
  "notes": "Reports to Chioma Anyamele. Manages Oando's gas business including flare capture. Key decision-maker for gas-to-power pilot partnerships. Responded within 24 hours to cold outreach — strong initial engagement signal."
}
```

## Field Guide

| Field | Required | Notes |
|-------|----------|-------|
| name | Yes | Full name as they use it professionally |
| email | Yes | Primary business email |
| phone | No | Include country code for international contacts |
| company | Yes | Current company or organization |
| role | Yes | Current title or role |
| relationship | Yes | One of: NRG Bloom partner/prospect/counsel/investor, Coldstorm client/prospect, Personal, Industry contact |
| tags | Yes | Lowercase, hyphenated keywords for searchability |
| location | No | City, Country format |
| first_met | Yes | Date of first interaction (YYYY-MM-DD) |
| last_contact | Yes | Updated every time a new interaction is logged |
| next_follow_up | No | Set when a follow-up is planned |
| interaction_history | Yes | Chronological log of all meaningful interactions |
| notes | Yes | Key context: what matters to this person, decision-making style, relationship dynamics |

## Design Decisions

- **One file per contact**: Makes lookup fast and avoids merge conflicts. Named by full name in lowercase-hyphenated format for consistency.
- **Tag with company relevance**: Tags like "nrg-bloom" or "coldstorm" ensure contact data stays properly scoped when pulled into meeting preps or pipeline reviews.
- **Update last_contact automatically**: Every time an interaction is logged, update this field. Stale last_contact dates surface in pipeline tracking and help identify relationships that need nurturing.
- **Professional context only**: Contact files should contain professional information relevant to the business relationship. Personal details beyond what is publicly available or voluntarily shared should not be stored.
