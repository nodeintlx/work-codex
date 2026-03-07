---
name: pipeline-tracker
description: >-
  Use this skill to track and manage business development opportunities across
  NRG Bloom and Coldstorm AI. Trigger whenever Makir asks about "deals",
  "prospects", "partnerships", "business development", "pipeline", "client
  leads", "how's [company name] going", "where are we with [deal]", "any
  movement on [prospect]", invokes /pipeline, or discusses a potential business
  relationship. Also trigger when emails arrive from pipeline contacts, when a
  meeting involves a prospect or partner, or when Makir asks about revenue
  opportunities. If Makir mentions a company name that might be a prospect, check
  the pipeline — even casual mentions like "heard back from Oando?" should
  surface the current deal status.
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, mcp__google-workspace__*, mcp__memory__*
---

# Pipeline Tracker

Track every business development opportunity from first contact to close. The goal is to ensure no deal falls through the cracks and Makir always knows where each opportunity stands, what needs to happen next, and who owns the next action.

## Pipeline Stages

```
PROSPECT -> OUTREACH -> RESPONSE -> MEETING -> PROPOSAL -> NEGOTIATION -> CLOSED-WON / CLOSED-LOST
```

## Pipeline File

Maintain at `~/Work/shared/pipeline.yaml`:

```yaml
last_updated: "2026-03-05"
deals:
  - id: 1
    name: "Oando Gas-to-Power Pilot"
    company: nrg_bloom
    counterparty: "Oando Clean Energy"
    stage: response
    value: "$500K (estimated first-phase)"
    contacts:
      - name: "Eleas Eduga"
        role: "Head of Gas Business"
        email: "eleas.eduga@oandoenergy.com"
      - name: "Chioma Anyamele"
        role: "Sustainability Lead"
        email: "chioma.anyamele@oandoenergy.com"
    first_contact: "2026-02-25"
    last_contact: "2026-03-01"
    next_action: "Follow up with Eleas if no call scheduled by March 7"
    next_action_date: "2026-03-07"
    next_action_owner: "counterparty"
    notes: "Strong initial engagement — responded within 24 hours. Eleas to schedule engagement call."
    risk: "medium"
```

## Process

1. **Read state** — Load ~/Work/shared/pipeline.yaml for current deals.

2. **Check email** — Search Gmail for recent emails with pipeline contacts. Look for responses, meeting confirmations, proposals, or silence that signals a stalling deal.

3. **Cross-reference tasks** — Check ~/Work/shared/tasks.yaml for related action items. Ensure pipeline next_actions and task list are aligned.

4. **Flag stale deals** — Any deal with no contact in 7+ days gets flagged. Seven days is the threshold because business momentum is fragile — prospects are evaluating multiple options, and silence from Makir's side signals low interest. A brief check-in email after 7 days keeps the deal warm without being pushy. However, if next_action_owner is "counterparty", note this context — the ball is in their court, and nagging Makir to follow up would be counterproductive.

5. **Update** — Write changes to pipeline.yaml. When a deal moves stages, also update tasks.yaml to keep both systems in sync.

6. **Present dashboard** — Use the output format below.

## Output Format

```
### Pipeline Dashboard — March 5, 2026

**Summary**: 2 active deals, 1 needs follow-up, 0 meetings scheduled

**By Stage**
| Deal | Company | Stage | Value | Next Action | Due | Owner |
|------|---------|-------|-------|-------------|-----|-------|
| Oando Gas-to-Power | NRG Bloom | Response | $500K | Await Eleas scheduling | Mar 7 | Counterparty |
| [Example] | Coldstorm | Outreach | $25K | Send intro email | Mar 6 | Makir |

**Needs Attention**
- Oando: Last contact 4 days ago (Mar 1). Owner: counterparty. Recommendation:
  wait until Mar 7 deadline, then send light follow-up to Eleas (cc Chioma).

**Recent Movement**
- Oando: Moved from Outreach -> Response on Feb 26 (Chioma looped in Eleas)

**Suggested Prospects** (from goals.yaml)
- OKR: "Identify 2 additional partnership prospects beyond Oando" — currently
  at 0/2. Consider reaching out to other Nigerian gas companies or data center
  operators in West Africa.
```

## Design Decisions

- **7-day stale threshold**: Business development momentum degrades quickly. After a week of silence, the other party starts assuming you have moved on. Flagging at 7 days catches deals before they go cold, while giving enough time for normal business delays (weekends, travel, internal approvals). The flag is a prompt to assess, not an automatic nag.
- **Track next_action_owner**: The most common pipeline mistake is following up when the ball is in the other party's court (annoying) or sitting idle when the ball is in yours (costly). Explicitly tracking ownership prevents both.
- **Separate NRG Bloom and Coldstorm**: Different companies, different value propositions, different stakeholders. Mixing them in pipeline views would create confusion. Always clearly label which company each deal belongs to.
- **Connect to OKRs**: After presenting the pipeline, always check goals.yaml for key results related to business development. If there is a gap (e.g., "2 prospects needed, 0 in pipeline"), surface it with a concrete suggestion. The pipeline tracker is not just a status report — it is a strategic tool.
- **Save new contacts**: When a new person enters the pipeline (cc'd on an email, mentioned as a decision-maker), create a contact record in ~/Work/shared/contacts/. Relationship context accumulates and pays dividends in future interactions.
