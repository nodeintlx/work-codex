---
name: grant-tracker
description: >-
  Use this skill to track funding applications, grant deadlines, and eligibility
  requirements for NRG Bloom and Coldstorm AI. Trigger whenever Makir asks about
  "funding", "grants", "SR&ED", "tax credits", "government money", "subsidies",
  "applications", "CanExport", "EDC", "Futurpreneur", "IRAP", "FACE", "BDC",
  "PME MTL", "Scale AI", "cloud credits", or any Canadian government program
  name. Also trigger when grant-related emails arrive (from TCS, CRA, Revenu
  Quebec, Innovation Canada), when Makir asks "what funding can we get", "what's
  the status on applications", "are we eligible for", or when a prerequisite
  changes status (e.g., tax filings completed) — because prerequisites unlocking
  means new programs become eligible and Makir should know immediately.
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, mcp__google-workspace__*, mcp__memory__*
---

# Grant Tracker

Track every funding opportunity from discovery through approval. Government funding is Makir's primary runway strategy — the stakes are high, deadlines are hard, and many programs have prerequisite chains where completing one step unlocks multiple others. This skill ensures nothing falls through the cracks and Makir always knows what is available, what is blocked, and what to do next.

## Funding Pipeline File

Maintain at `~/Work/shared/funding.yaml`:

```yaml
last_updated: "2026-03-05"
programs:
  - id: 1
    name: "SR&ED Tax Credit (FY2024)"
    agency: "CRA"
    type: tax_credit
    amount: "$50K-$150K (estimated, depends on eligible expenditures)"
    company: nrg_bloom
    status: researching
    deadline: "2026-06-30"
    prerequisites:
      - requirement: "Corporate tax filings current (T2 + CO-17)"
        met: false
        notes: "Accountant working on it — follow up overdue"
      - requirement: "SR&ED specialist engaged (contingency fee)"
        met: false
        notes: "Leyton no answer, Ayming didn't understand. Trying G6, Northbridge, RDBASE."
    next_action: "Find and engage alternative SR&ED specialist"
    next_action_date: "2026-03-07"
    contact: "TBD — specialist not yet engaged"
    notes: "IQ offers bridge financing on SR&ED refund — cash within weeks of filing, not 6 months. Contingency fee model = zero upfront cost. Combined SR&ED + CRIC = up to 65% refund."
    file: "~/Work/nrg-bloom/projects/funding/sred-call-scripts-2026-03-04.md"
```

## Process

1. **Read state** — Load ~/Work/shared/funding.yaml for current programs and their statuses.

2. **Check prerequisites** — This is the most important step. Cross-reference with tasks.yaml to see if any prerequisites have changed status. Many programs form dependency chains (see below), and a single prerequisite completing can unlock multiple applications at once.

3. **Check email** — Search Gmail for responses from funding bodies: TCS, Futurpreneur, CRA, Revenu Quebec, Innovation Canada, IRAP, FACE, EDC. Government responses are often time-sensitive — they may request additional information with a short window to reply.

4. **Flag deadlines** — Surface any deadlines within 60 days. Government grant deadlines are typically hard — missing one means waiting months or years for the next cycle. The 60-day window gives enough lead time to prepare applications properly.

5. **Update** — Write changes to funding.yaml.

6. **Present dashboard** — Use the output format below.

## Dependency Chains

This is the core strategic insight of grant tracking: programs are not independent — they form chains where completing one step unlocks several others. Understanding these chains lets Makir prioritize the highest-leverage actions.

**Chain 1: Tax Filings -> Tax Credits -> Applications**
```
Corporate tax filings current (T2 + CO-17)
  |-> SR&ED claim eligible (up to $150K refund)
  |     |-> IQ bridge financing (cash within weeks of SR&ED filing)
  |-> CanExport application eligible (need GST 34 return)
  |-> IRAP eligibility confirmed
  |-> General grant eligibility (most programs require filings current)
```

**Chain 2: EDC -> Banking -> Contracts**
```
EDC scoping call completed
  |-> Political Risk Insurance (90% coverage on Nigeria exposure)
  |-> TELP working capital guarantee (through your bank)
  |     |-> Bank provides working capital line
  |           |-> Enables larger contracts and Nigeria operations
```

**Chain 3: Futurpreneur -> Working Capital -> Travel**
```
Futurpreneur loan approved ($75K + $40K follow-on)
  |-> Working capital for operations
  |-> Enables Nigeria travel for Oando engagement
  |-> Mentorship access for business planning
```

**What this means in practice**: Getting the tax filings done (Chain 1 root) is the single highest-leverage action for the entire funding workstream. It unblocks SR&ED, CanExport, IRAP, and general grant eligibility simultaneously. When a prerequisite at the root of a chain completes, proactively flag every program it unlocks.

## Output Format

```
### Funding Dashboard — March 5, 2026

**Summary**: 12 programs tracked, 3 applications active, $1.2M+ total potential

**Active Applications**
| Program | Type | Amount | Status | Deadline | Next Step |
|---------|------|--------|--------|----------|-----------|
| Futurpreneur BESP | Loan | $75K+$40K | In progress | Mar 15 | Provide additional info |
| FACE Loan Fund | Loan | $250K | In progress | Mar 7 | Submit application |
| SR&ED FY2024 | Tax credit | $50K-$150K | Researching | Jun 30 | Find specialist |

**Blocked by Prerequisites**
- SR&ED: Needs (1) tax filings current, (2) specialist engaged — both unmet
- CanExport: Needs Certificate of Incorporation + GST 34 return

**Approaching Deadlines** (next 60 days)
| Program | Deadline | Days Left | Ready? |
|---------|----------|-----------|--------|
| CanExport SMEs | May 29 | 85 | No — missing: GST 34, Certificate of Inc. |
| SR&ED FY2024 | Jun 30 | 117 | No — missing: specialist, tax filings |

**Prerequisite Alert**
- Tax filings completion would unlock: SR&ED, CanExport, IRAP, general eligibility
  (4 programs, est. $300K+ combined). This is the highest-leverage single action.

**Opportunities Not Yet Pursued**
- ECO Canada DS4Y ($30K salary reimbursement) — not yet contacted
- PME MTL clean tech grant ($60K non-repayable) — not yet visited
```

## Design Decisions

- **60-day deadline window**: Government applications require preparation — financial statements, business plans, supporting documents. Surfacing deadlines at 30 days is often too late. The 60-day window ensures Makir has time to prepare properly and is not rushing applications (rushed applications get rejected).
- **SR&ED gets permanent priority**: The SR&ED FY2024 deadline (June 30, 2026) is the most time-sensitive hard deadline in the funding pipeline. Missing it means losing the entire tax credit for that fiscal year permanently. Always track its status and surface blockers.
- **Flag when prerequisites complete**: When a prerequisite status changes to met, proactively announce every program it unlocks. Example: "Tax filings are done! This unlocks SR&ED, CanExport, and IRAP — recommend starting SR&ED specialist engagement immediately." This is where the dependency chain logic earns its value.
- **Company separation**: Financial details for NRG Bloom and Coldstorm must stay separated. Some programs (like cloud credits) may apply to both companies — track these with `company: both` but present them in the appropriate company context.
- **Cross-reference research files**: Detailed research on each program lives in ~/Work/nrg-bloom/projects/funding/ and ~/Work/knowledge/. Link to these from the funding.yaml entries so Makir can dive deeper when needed. When a grant is approved, update goals.yaml key results to reflect progress.
