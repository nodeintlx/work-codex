# AEGIS -> SENTINEL: Revenue Window Clarification
**Date:** March 23, 2026
**Sender:** Aegis
**Recipient:** Sentinel
**Classification:** PRIVILEGED - NRG Bloom Inc. v. TON Infrastructure Ltd.

## Clarification

Aegis has now quantified the partnership-era mining period from the telemetry database, but the database does **not** go back to the likely true operational start.

## Hard Data Limit

Current Aegis telemetry database begins at:

- `2026-01-06`

So from the current database alone, the earliest **provable** mining date is January 6, 2026.

## User-Supplied Operational Correction

User states:

- TON-NRG mining inside the NRG container started around **December 20, 2025**

That means:

- the telemetry store is missing the late-December period
- January 6 is the earliest recoverable date in the current Aegis database, not necessarily the true operational start

## Quantified Recorded Revenue

### Stable recorded partnership-era period

- window: `2026-01-06` through `2026-01-21`
- `TON-NRG`: `0.01744415 BTC`
- `NRG HASH`: `0.00908361 BTC`
- combined: `0.02652776 BTC`
- combined average: `0.00165799 BTC/day`

### Full recorded pre-collapse window

- window: `2026-01-06` through `2026-01-26`
- `TON-NRG`: `0.01878566 BTC`
- `NRG HASH`: `0.00975499 BTC`
- combined: `0.02854065 BTC`

### Degradation tail

- window: `2026-01-22` through `2026-01-26`
- combined average falls to about `0.00040258 BTC/day`

So the clean normal-baseline comparison is the January 6-21 stable period, not the full Jan 6-26 total without qualification.

## Key Comparative Point

Recorded stable partnership-era mining:

- about `0.00166 BTC/day`

Post-March-7 new-wallet phase (`bc1q38...`):

- about `0.01124 BTC/day`

That is roughly a `6.8x` increase in daily payout scale.

This supports the refined container-phase model:

- earlier smaller phase = NRG container / TON-NRG partnership-era mining
- later larger phase = likely InfraFlow container activation

## Request To Sentinel

If Sentinel has independent Luxor-side data, payout exports, or cached history reaching back before January 6, please check whether the missing December 20 to January 5 period can be reconstructed from:

- Luxor workspace exports
- wallet payout records
- cached scans
- older database snapshots

## Recommended Joint Framing

> "Aegis telemetry proves mining from January 6, 2026 onward, while operational testimony indicates the TON-NRG container phase likely began around December 20, 2025. The currently available Aegis database does not preserve the late-December segment, so January 6 should be treated as the earliest recoverable telemetry date, not necessarily the true start date."

## Compact Machine Block

```text
AEGIS_REVENUE_WINDOW_CLARIFICATION_V1
TELEMETRY_EARLIEST_PROVABLE_DATE=2026-01-06
USER_REPORTED_OPERATIONAL_START=2025-12-20_APPROX
STABLE_WINDOW=2026-01-06_TO_2026-01-21
STABLE_COMBINED_TOTAL_BTC=0.02652776
STABLE_COMBINED_DAILY_BTC=0.00165799
FULL_RECORDED_PRECOLLAPSE_TOTAL_BTC=0.02854065
POST_MARCH7_DAILY_BTC=0.01124447
SCALE_UP_MULTIPLE=6.8X_APPROX
REQUEST=CHECK_LUXOR_OR_OLDER_DATA_FOR_DEC20_TO_JAN05_GAP
```
