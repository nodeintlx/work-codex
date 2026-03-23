---
name: blockchain-investigation
description: Investigate Bitcoin wallet activity, mining-pool payout patterns, fresh-wallet starts, hashrate footprints, watchlists, and downstream cash-out paths. Use when tracing pool-linked wallets, ranking candidates by startup date and payout cadence, reconciling CSV or telemetry exports with on-chain activity, or maintaining wallet-investigation case memory.
---

# Blockchain Investigation

## Overview

Use this skill for wallet attribution and pool-footprint analysis where the goal is to find the most likely operational wallet, not just any wallet that touched the same cluster.

Keep the workflow constraint-driven:
- trust the user's operational dates and capacity estimates
- separate evidence from inference
- prefer fresh-wallet timing and cadence over loose cluster overlap
- reject numerically plausible wallets if they violate the startup window

Open only the references you need.

## Workflow

1. Lock the constraints before scanning.
   - start date or date window
   - pool or sender cluster
   - expected payout cadence: daily, weekly, mixed
   - expected size band: BTC/day, BTC/week, or PH range
   - freshness rule: new wallet only, low-history wallet, or any wallet
2. Open [references/commands.md](references/commands.md) and choose the smallest command path that fits:
   - API-first scan
   - CSV reconciliation
   - telemetry plus chain reconciliation
3. Estimate the expected payout footprint with `scripts/hashrate_footprint.py` before ranking wallets.
4. Rank candidates with `scripts/rank_wallet_candidates.py` when you have a candidate table.
5. Load [references/case-memory-schema.md](references/case-memory-schema.md) and update the active case memory using [templates/wallet-case-memory.yaml](templates/wallet-case-memory.yaml).
6. Build a watchlist only after ranking:
   - primary
   - sibling
   - tertiary watch
   - discarded
7. If a candidate starts spending, trace the first outbound path before broadening the cluster.

## Default Scoring Priorities

Use this order unless the user says otherwise:
1. Startup timing
2. Freshness and low prior history
3. Payout cadence consistency
4. Size match to expected hashrate
5. Lack of non-pool contamination
6. Downstream behavior after first spend

## Investigation Rules

- Do not promote a wallet just because it shares Luxor batches with a known address if it predates the claimed startup date.
- A same-batch link is cohort evidence, not ownership proof.
- A large high-churn downstream address is usually service infrastructure, not the operating wallet you want to monitor.
- When daily receipts are stable and the wallet has no spends, treat it as a stronger payout-wallet candidate than a noisier address with a larger raw amount.
- Say explicitly when a conclusion is an inference from payout behavior rather than a direct on-chain link.

## Deliverables

For each investigation, produce:
- a short thesis
- ranked candidate list
- watchlist
- evidence vs inference split
- memory update

## Useful Files

- [references/commands.md](references/commands.md): repeatable command patterns
- [references/case-memory-schema.md](references/case-memory-schema.md): wallet-case fields and update rules
- [templates/wallet-case-memory.yaml](templates/wallet-case-memory.yaml): seed file for a new investigation
- `scripts/hashrate_footprint.py`: estimate PH from daily or weekly BTC
- `scripts/rank_wallet_candidates.py`: rank candidates from a CSV table
- `scripts/watchlist_export.py`: export watchlists to Markdown
