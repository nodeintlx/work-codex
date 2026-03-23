# AEGIS -> SENTINEL: TON Mining Timeline Memo
**Date:** March 23, 2026
**Sender:** Aegis
**Recipient:** Sentinel
**Classification:** PRIVILEGED - NRG Bloom Inc. v. TON Infrastructure Ltd.

## Purpose

Provide a single clean operational timeline for TON-related Bitcoin mining activity using:

- Luxor daily stats CSV for `TON-NRG`
- Aegis telemetry database for `TON-NRG` and `NRG HASH`
- March 6 bridge-event analysis
- post-March-7 wallet attribution to `bc1q38ck9dvr4c6qrkqn9690rcefvgrw53hxxxln7j`

## Core Conclusion

The best current model is:

1. `TON-NRG` mining begins in the NRG container by **December 22, 2025** at the latest
2. the partnership-era operation runs at smaller scale through January 2026
3. shutdown / sabotage follows on January 27, 2026
4. a March 6 telemetry blip acts as a bridge event between old and new operations
5. from March 7 onward, the new Luxor wallet `bc1q38...` reflects a much larger operation, more consistent with **InfraFlow-scale** mining than with the earlier NRG-container-only phase

## Timeline

### Phase 1: TON-NRG startup

Earliest hard Luxor record:

- `2025-12-22`
- `TON-NRG` daily stats:
  - `2.48 PH/s`
  - `53` workers
  - `53.90%` uptime
  - `0.00102807 BTC`

Interpretation:

- operation is already live by December 22
- this is the earliest hard date now supported by Luxor-export evidence
- user reports startup around December 20, 2025, which is consistent with the CSV appearing slightly after the likely true operational start

### Phase 2: Stable partnership-era mining

From `2025-12-23` through `2026-01-21`, `TON-NRG` settles into a stable pattern:

- about `2.5 to 2.6 PH/s`
- `30` workers
- about `0.00104 to 0.00110 BTC/day`

Combined stable partnership-era production, using:

- `TON-NRG` from Luxor CSV
- `NRG HASH` from Aegis telemetry

Window:

- `2025-12-22` through `2026-01-21`

Totals:

- `TON-NRG`: `0.03227968 BTC`
- `NRG HASH`: `0.00908361 BTC`
- combined: `0.04136329 BTC`
- combined daily average: `0.00133430 BTC/day`

Operational meaning:

- this is the smaller, partnership-era production footprint
- this phase is best understood as the **NRG-container** phase

### Phase 3: Degradation and collapse

By `2026-01-22` onward, performance degrades.

Examples:

- `2026-01-22`: `TON-NRG` falls to `1.94 PH/s`, `0.00082075 BTC`
- `NRG HASH` also weakens materially
- Aegis telemetry continues to support a shutdown / sabotage event on `2026-01-27`

Operational meaning:

- the partnership-era mining profile breaks down before the full shutdown event
- this fits the broader sabotage / exclusion narrative

### Phase 4: March 6 bridge event

Aegis telemetry shows a short restart blip in `TON-NRG` on `2026-03-06`.

Summary-table peak:

- `20` active miners at `2026-03-06T11:20:33.758295`

Worker-layer clarification:

- `15` worker names present during the March 6 window
- `13` show positive `hashrate_5m`

Operational meaning:

- this remains strong bridge evidence linking the old operational environment to the post-March-6 phase
- but it should not be overstated as proof that the full later output came only from the original smaller container

### Phase 5: Post-March-7 large-scale mining

New wallet:

- `bc1q38ck9dvr4c6qrkqn9690rcefvgrw53hxxxln7j`

Observed pattern:

- first funded via Luxor payout on `2026-03-07`
- then `15` straight daily Luxor receipts from `2026-03-08` through `2026-03-22`
- average daily payout:
  - `0.01124447 BTC/day`

Comparison to stable partnership-era combined production:

- partnership-era combined average: `0.00133430 BTC/day`
- post-March-7 wallet average: `0.01124447 BTC/day`
- scale-up: about `8.4x`

Operational meaning:

- the new wallet reflects a materially larger operation
- this later return profile is more consistent with **InfraFlow-scale** deployment than with the earlier NRG-container-only phase

## Recommended Framing

Recommended unified statement:

> "Luxor records show TON-NRG mining activity by December 22, 2025, with a stable partnership-era production profile through January 2026. After the shutdown period, Aegis telemetry records a March 6 bridge event in the legacy workspace. Beginning March 7, 2026, a new Luxor-linked wallet (`bc1q38ck9dvr4c6qrkqn9690rcefvgrw53hxxxln7j`) begins receiving daily payouts at a scale approximately 8.4 times larger than the stable partnership-era combined baseline, supporting the inference that TON transitioned from the earlier NRG-container phase to a larger InfraFlow-scale mining phase."

## Why This Matters

This timeline does four things at once:

- proves earlier partnership-era mining activity with a December 2025 start
- preserves the sabotage / shutdown sequence
- preserves the March 6 operational bridge
- explains why the new wallet's scale is too large to be casually treated as just a simple restart of the earlier smaller setup

## Compact Machine Block

```text
AEGIS_TIMELINE_MEMO_V1
START_HARD_DATE=2025-12-22
PARTNERSHIP_PHASE=NRG_CONTAINER_PHASE
PARTNERSHIP_STABLE_DAILY_BTC=0.00133430_COMBINED
SHUTDOWN_DATE=2026-01-27
BRIDGE_EVENT=2026-03-06
NEW_WALLET=bc1q38ck9dvr4c6qrkqn9690rcefvgrw53hxxxln7j
NEW_WALLET_DAILY_BTC=0.01124447
SCALE_UP=8.4X_APPROX
LARGE_SCALE_PHASE=LIKELY_INFRAFLOW_CONTAINER
```
