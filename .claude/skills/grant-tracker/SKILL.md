---
name: grant-tracker
description: Track funding applications, grant deadlines, and eligibility requirements for NRG Bloom. Monitor SR&ED, CanExport, EDC, Futurpreneur, and other government programs. Use when checking funding status, preparing applications, or when grant-related emails arrive.
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, mcp__google-workspace__gmail_*, mcp__memory__*
---

# Grant Tracker Skill

## Funding Pipeline File
Maintain at ~/Work/shared/funding.yaml

### Schema
```yaml
last_updated: "YYYY-MM-DD"
programs:
  - id: 1
    name: "Program name"
    agency: "Government body"
    type: grant | loan | tax_credit | insurance | guarantee
    amount: "$X (max available)"
    company: nrg_bloom | coldstorm
    status: researching | eligible | applying | submitted | under_review | approved | rejected
    deadline: "YYYY-MM-DD"
    prerequisites:
      - requirement: "Description"
        met: true | false
        notes: "Status"
    next_action: "What needs to happen"
    next_action_date: "YYYY-MM-DD"
    contact: "Name, phone, email"
    notes: "Context"
    file: "Path to application or research file"
```

## Process
1. **Read** ~/Work/shared/funding.yaml for current state
2. **Check prerequisites** — cross-reference with tasks.yaml (e.g., tax filings → unlock SR&ED)
3. **Check Gmail** for responses from funding bodies (TCS, Futurpreneur, CRA, Revenu Québec)
4. **Flag deadlines** within 30 days
5. **Update** funding.yaml with any changes
6. **Present** funding dashboard

## Output Format

### Funding Dashboard — [Date]

**Summary**: [X] programs tracked, [Y] applications active, $[Z] total potential funding

**Active Applications**
| Program | Type | Amount | Status | Deadline | Next Step |
|---------|------|--------|--------|----------|-----------|
| [Name] | [Type] | [$X] | [Status] | [Date] | [Action] |

**Blocked by Prerequisites**
- [Program]: Needs [requirement] — Currently: [status]

**Approaching Deadlines** (next 60 days)
| Program | Deadline | Days Left | Ready? |
|---------|----------|-----------|--------|
| [Name] | [Date] | [X] | Yes/No — missing: [items] |

**Recently Updated**
- [Program]: [Change summary]

**Opportunities Not Yet Pursued**
- [Program from research files not yet in pipeline]

## Dependency Tracking
Some programs unlock others. Track these chains:
- Corporate tax filings current → SR&ED eligible → CanExport eligible → IRAP eligible
- EDC insurance → unlocks bank financing → enables larger contracts
- Futurpreneur loan → working capital → enables travel to Nigeria

## Rules
- SR&ED FY2024 deadline (June 30, 2026) is the most time-sensitive — always track
- Flag when prerequisites are met — "Tax filings are done! You can now apply for [X]"
- Never share financial details between NRG Bloom and Coldstorm contexts
- Cross-reference ~/Work/nrg-bloom/projects/funding/ for detailed research files
- When a grant is approved, update goals.yaml key results
