---
name: pipeline-tracker
description: Track business development opportunities across NRG Bloom and Coldstorm AI. Monitor deal stages, follow-up deadlines, and next actions for each prospect. Use when checking on partnerships, updating deal status, reviewing business development pipeline, or when Makir asks about prospects.
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, mcp__google-workspace__gmail_*, mcp__google-workspace__calendar_*, mcp__memory__*
---

# Pipeline Tracker Skill

## Pipeline Stages
```
PROSPECT → OUTREACH → RESPONSE → MEETING → PROPOSAL → NEGOTIATION → CLOSED-WON / CLOSED-LOST
```

## Pipeline File
Maintain the pipeline at ~/Work/shared/pipeline.yaml

### Schema
```yaml
last_updated: "YYYY-MM-DD"
deals:
  - id: 1
    name: "Deal name"
    company: nrg_bloom | coldstorm
    counterparty: "Company name"
    stage: prospect | outreach | response | meeting | proposal | negotiation | closed_won | closed_lost
    value: "$X (estimated or quoted)"
    contacts:
      - name: "Name"
        role: "Title"
        email: "email"
    first_contact: "YYYY-MM-DD"
    last_contact: "YYYY-MM-DD"
    next_action: "What needs to happen next"
    next_action_date: "YYYY-MM-DD"
    next_action_owner: "makir | counterparty | dayo | julie"
    notes: "Context and history"
    risk: "low | medium | high"
```

## Process
1. **Read** ~/Work/shared/pipeline.yaml for current state
2. **Check Gmail** for recent emails with pipeline contacts — look for responses, meeting requests, or follow-ups needed
3. **Cross-reference** ~/Work/shared/tasks.yaml for related tasks
4. **Update** pipeline.yaml with any new information
5. **Present** pipeline dashboard

## Output Format

### Pipeline Dashboard — [Date]

**Summary**: [X] active deals, [Y] need follow-up, [Z] meetings scheduled

**By Stage**:
| Deal | Company | Stage | Value | Next Action | Due | Owner |
|------|---------|-------|-------|-------------|-----|-------|
| [Name] | [Co] | [Stage] | [$X] | [Action] | [Date] | [Who] |

**Needs Attention** (overdue or stale)
- [Deal]: Last contact [X days ago]. Recommended: [action]

**Recent Movement**
- [Deal]: Moved from [stage] → [stage] on [date]

**Suggested Outreach**
- [Prospect idea based on goals.yaml and market context]

## Rules
- Deals with no contact in 7+ days should be flagged
- Always check if a deal's next_action_owner is "counterparty" — if so, it's a waiting game, don't nag Makir
- When a deal moves stages, update both pipeline.yaml and tasks.yaml
- Save contact details to ~/Work/shared/contacts/ when new people enter the pipeline
- Separate NRG Bloom and Coldstorm deals clearly
- After presenting pipeline, suggest 1-2 prospects from goals.yaml that aren't in the pipeline yet
