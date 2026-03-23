# AEGIS -> SENTINEL: TON-NRG CSV Reconciliation
**Date:** March 23, 2026
**Sender:** Aegis
**Recipient:** Sentinel
**Classification:** PRIVILEGED - NRG Bloom Inc. v. TON Infrastructure Ltd.

## Executive Point

Aegis has now reconciled a newly downloaded Luxor CSV export with the existing telemetry database.

This materially improves the pre-shutdown timeline:

- earliest hard Luxor record is now **December 22, 2025**
- this pushes the recoverable TON-NRG mining start back from January 6 to December 22
- the CSV appears to cover the **TON-NRG workspace only**
- combining the CSV with `NRG HASH` telemetry gives a cleaner estimate of total partnership-era production

## 1. Corrected Start Date

Previous Aegis hard-data floor:

- `2026-01-06` (from local telemetry database only)

New hard-data floor after CSV reconciliation:

- `2025-12-22`

The Luxor CSV file:

- `dailystats_2026-03-23.csv`

shows TON-NRG already live on `2025-12-22`:

- hashrate: `2.48 PH/s`
- workers: `53`
- uptime: `53.90%`
- mining: `0.00102807 BTC`

By `2025-12-23`, the operation settles into the cleaner pattern:

- about `2.6 PH/s`
- `30` workers
- about `0.00108 BTC/day`

## 2. Full Phase Timeline

### Phase A: TON-NRG container startup

- `2025-12-22`
- first hard Luxor record
- `2.48 PH/s`, `53` workers, partial day / startup-like profile

### Phase B: stable NRG-container mining

- `2025-12-23` through `2026-01-21`
- TON-NRG runs in a stable band around:
  - `2.5 to 2.6 PH/s`
  - `30` workers
  - about `0.00104 to 0.00110 BTC/day`

### Phase C: degradation / collapse period

- `2026-01-22` through `2026-01-26`
- lower or unstable output appears:
  - Jan 22: `1.94 PH/s`, `0.00082075 BTC`
  - Jan 23: rebound in TON-NRG CSV, but `NRG HASH` collapses
  - Jan 24: `2.39 PH/s`, `0.00104126 BTC`
  - Jan 25-26: TON-NRG still near normal, but combined telemetry remains degraded

### Phase D: Jan 27 shutdown / sabotage

- existing telemetry evidence still supports the shutdown event as the operational break

### Phase E: March 6 bridge event

- brief TON-NRG restart blip
- operationally useful as bridge evidence

### Phase F: post-March-6 large-scale TON phase

- wallet: `bc1q38ck9dvr4c6qrkqn9690rcefvgrw53hxxxln7j`
- about `0.01124447 BTC/day`
- much larger than the earlier TON-NRG phase
- remains more consistent with InfraFlow-scale mining than with the earlier NRG-container-only phase

## 3. TON-NRG CSV Totals

### Full recorded TON-NRG CSV window

- `2025-12-22` through `2026-01-26`
- total: `0.03752231 BTC`
- average: `0.00104229 BTC/day`

### Stable pre-collapse TON-NRG window

- `2025-12-22` through `2026-01-21`
- total: `0.03227968 BTC`
- average: `0.00104128 BTC/day`

## 4. Combined Partnership-Era Production

Using:

- TON-NRG from the Luxor CSV
- NRG HASH from `mining_summary_history`

### Combined full recorded window

- `2025-12-22` through `2026-01-26`
- TON-NRG total: `0.03752231 BTC`
- NRG HASH total: `0.00975499 BTC`
- combined total: `0.04727730 BTC`
- combined average: `0.00131326 BTC/day`

### Combined stable pre-collapse window

- `2025-12-22` through `2026-01-21`
- TON-NRG total: `0.03227968 BTC`
- NRG HASH total: `0.00908361 BTC`
- combined total: `0.04136329 BTC`
- combined average: `0.00133430 BTC/day`

## 5. Comparison To New Wallet Phase

Stable combined partnership-era production:

- about `0.00133430 BTC/day`

Post-March-7 new-wallet phase (`bc1q38...`):

- about `0.01124447 BTC/day`

Scale-up:

- about `8.4x`

This is stronger than the earlier January-only comparison because it incorporates the earlier TON-NRG CSV history.

## 6. Interpretation

This strengthens the refined model:

- early phase = NRG-container / TON-NRG partnership-era mining
- later large-scale phase = separate larger TON-controlled operation, likely InfraFlow container activation

The corrected start date and combined production totals make the before/after contrast substantially clearer.

## Compact Machine Block

```text
AEGIS_TON_NRG_CSV_RECON_V1
CSV_FILE=dailystats_2026-03-23.csv
EARLIEST_HARD_DATE=2025-12-22
TON_NRG_CSV_FULL_TOTAL_BTC=0.03752231
TON_NRG_CSV_STABLE_TOTAL_BTC=0.03227968
COMBINED_STABLE_TOTAL_BTC=0.04136329
COMBINED_STABLE_DAILY_BTC=0.00133430
POST_MARCH7_DAILY_BTC=0.01124447
SCALE_UP_MULTIPLE=8.4X_APPROX
KEY_POINT=CSV_CONFIRMS_PRE_JAN6_TON_NRG_MINING_AND_STRENGTHENS_CONTAINER_PHASE_DISTINCTION
```
