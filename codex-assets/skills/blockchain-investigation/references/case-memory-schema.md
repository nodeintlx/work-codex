# Case Memory Schema

Use one YAML file per investigation. Keep the file factual and update it as the case evolves.

## Required top-level fields

- `case_id`: stable slug
- `title`: short human-readable title
- `updated_at`: ISO timestamp
- `status`: active, monitoring, closed, or superseded
- `objective`: one-sentence target
- `constraints`: operational assumptions that drive the scan
- `sources`: CSV, DB, API, or user-supplied evidence
- `known_addresses`: labeled addresses already accepted into the record
- `candidate_addresses`: ranked candidates with evidence and confidence
- `watchlist`: the addresses that should be monitored going forward
- `timeline`: dated events and what changed
- `findings`: current evidence
- `inferences`: current analytical conclusions
- `open_questions`: unresolved issues
- `next_actions`: concrete next steps

## Field rules

- `constraints` should include startup date, expected hashrate, payout cadence, and exclusion rules.
- `known_addresses` should be reserved for wallets already grounded by evidence or user knowledge.
- `candidate_addresses` should include both supporting and disqualifying facts.
- `watchlist` should contain a priority and the trigger to watch for.
- `findings` should remain evidentiary.
- `inferences` should remain analytical and reversible.

## Confidence values

Use one of:
- `high`
- `medium`
- `low`

## Address object shape

```yaml
- label: TON_PRIMARY
  address: bc1...
  role: primary_candidate
  confidence: high
  first_seen: 2026-03-07
  last_seen: 2026-03-22
  evidence:
    - fresh wallet starting inside target window
    - 15 straight daily Luxor receipts
  disqualifiers: []
  notes: No spends yet.
```
