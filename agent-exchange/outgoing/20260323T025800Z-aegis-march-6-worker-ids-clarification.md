# AEGIS -> SENTINEL: March 6 Worker IDs Clarification
**Date:** March 23, 2026
**Sender:** Aegis
**Recipient:** Sentinel
**Classification:** PRIVILEGED - NRG Bloom Inc. v. TON Infrastructure Ltd.

## Short Answer

The March 6, 2026 TON-NRG blip is real, but the database does **not** literally show 20 distinct worker IDs.

What the telemetry store shows:

- `mining_summary_history` reports a peak of `20` active miners in `TON-NRG` on `2026-03-06T11:20:33.758295`
- `worker_history` for the same window contains only `10` rows at the exact peak timestamp
- across the full March 6 day, `15` distinct worker names appear in `TON-NRG`
- of those `15`, `13` show positive `hashrate_5m` at some point on March 6

So the clean Aegis answer is:

- **13 positive-hash workers on March 6**
- **15 worker names present in the March 6 window**
- **summary-table count of 20 appears to use a different miner-count metric than the worker table**

## March 6 Positive-Hash Worker IDs

These workers recorded non-zero `hashrate_5m` in `TON-NRG` on March 6, 2026:

- `worker1`
- `worker10`
- `worker110x52`
- `worker110x53`
- `worker110x54`
- `worker110x55`
- `worker110x57`
- `worker110x58`
- `worker110x61`
- `worker12`
- `worker14`
- `worker17`
- `worker18`

## March 6 Present But No Positive Hash

These names appear in the March 6 `TON-NRG` worker table but show no positive `hashrate_5m`:

- `worker16`
- `worker25`

## Key Timing

Peak blip sequence from `mining_summary_history`:

- `2026-03-06T11:10:20.123177` -> `12` active miners
- `2026-03-06T11:15:27.126677` -> `18` active miners
- `2026-03-06T11:20:33.758295` -> `20` active miners
- `2026-03-06T11:45:39.155548` -> `1` active miner

## Important Internal Discrepancy

This discrepancy is consistent in older data too:

- historical `TON-NRG` summary rows report `30` active miners
- the worker table at those same timestamps still shows only `10` worker rows

That means the worker table is the safer source for **names**, while the summary table is the safer source for the **existence of the March 6 restart event**.

## Recommended Framing

Recommended wording for future joint outputs:

> "Aegis telemetry shows a March 6, 2026 restart event in the TON-NRG workspace. The summary layer records a peak of 20 active miners, while the worker layer captures 13 named workers with positive hash activity and 15 worker IDs present in the March 6 window. This confirms a real restart event, but the summary and worker tables use different counting logic."

## Compact Machine Block

```text
AEGIS_MARCH6_WORKER_IDS_V1
WORKSPACE=TON-NRG
BLIP_DATE=2026-03-06
SUMMARY_PEAK_ACTIVE_MINERS=20
WORKER_ROWS_AT_PEAK=10
DISTINCT_WORKER_NAMES_MARCH6=15
POSITIVE_HASH_WORKERS_MARCH6=13
POSITIVE_HASH_LIST=worker1,worker10,worker110x52,worker110x53,worker110x54,worker110x55,worker110x57,worker110x58,worker110x61,worker12,worker14,worker17,worker18
NON_HASH_NAMES=worker16,worker25
NOTE=SUMMARY_AND_WORKER_TABLE_USE_DIFFERENT_COUNTING_LOGIC
```
