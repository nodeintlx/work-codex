---
name: meeting-prep
description: Prepare a comprehensive pre-meeting brief with attendee context, agenda review, related documents, and suggested talking points. Use before meetings, when asked to prep for a meeting, or when reviewing upcoming calendar events in detail.
allowed-tools: Read, Glob, Grep, WebSearch, mcp__google-workspace__*, mcp__memory__*
---

# Meeting Prep Skill

## Process
1. **Meeting Details**: Get the specific meeting from Calendar MCP — time, attendees, agenda, attached docs.
2. **Attendee Context**: For each attendee, check ~/Work/shared/contacts/ for existing profiles. If no profile exists, do a quick web search for professional context.
3. **Related Communications**: Search recent emails with attendees for context on ongoing discussions.
4. **Related Documents**: Search ~/Work/ for any documents related to the meeting topic.
5. **Talking Points**: Based on all context, suggest 3-5 talking points or questions.

## Output Format

### Meeting Brief: [Meeting Title]
**Date/Time**: [Day, Date at Time ET]
**Duration**: [X minutes]
**Location/Link**: [Location or video link]

**Attendees**
| Name | Role/Company | Relationship | Last Contact |
|------|-------------|--------------|--------------|
| [Name] | [Role] | [Context] | [Date] |

**Agenda & Context**
- [Agenda item 1]: [Relevant background]
- [Agenda item 2]: [Relevant background]

**Recent Communications**
- [Date]: [Brief summary of relevant email/message thread]

**Suggested Talking Points**
1. [Point with rationale]
2. [Point with rationale]
3. [Point with rationale]

**Prep Actions**
- [ ] [Any documents to review before the meeting]
- [ ] [Any data to pull]

## Rules
- If no calendar event is specified, prep for the next upcoming meeting
- Keep briefs focused and under 600 words
- Flag any potential conflicts of interest between attendees and NRG Bloom/Coldstorm
- Do not include confidential client information from Coldstorm in NRG Bloom meeting preps (and vice versa)
