# Command Set

Use these patterns as the default operating toolkit.

## 1. Estimate hashrate footprint from payout size

```bash
python3 scripts/hashrate_footprint.py --daily-btc 0.01124 --network-eh-low 750 --network-eh-high 900
```

Use `--weekly-btc` instead when the wallet is paid weekly.

## 2. Rank candidate wallets from a CSV

Expected CSV columns:
- `address`
- `first_seen`
- `last_seen`
- `payout_days`
- `avg_daily_btc`
- `total_btc`
- `spends`
- `non_pool_inflows`
- `shared_batch_refs`
- `notes`

Example:

```bash
python3 scripts/rank_wallet_candidates.py \
  --csv /path/to/candidates.csv \
  --start-date 2026-03-06 \
  --expected-ph-low 25 \
  --expected-ph-high 31 \
  --network-eh-low 750 \
  --network-eh-high 900
```

## 3. Export a watchlist to Markdown

```bash
python3 scripts/watchlist_export.py \
  --csv /path/to/watchlist.csv \
  --title "TON Luxor Watchlist" \
  --output /path/to/watchlist.md
```

Expected watchlist CSV columns:
- `label`
- `address`
- `role`
- `priority`
- `reason`
- `first_seen`
- `last_seen`

## 4. Minimal Blockstream and mempool usage

Use API endpoints only when the question depends on live chain data.

Examples:

```bash
curl -s https://blockstream.info/api/address/<address>
curl -s https://blockstream.info/api/address/<address>/txs
curl -s https://blockstream.info/api/tx/<txid>
curl -s https://mempool.space/api/address/<address>
curl -s https://mempool.space/api/address/<address>/txs
```

## 5. SQLite telemetry checks

```bash
sqlite3 nrg_bloom.db "select pool_name, timestamp, active_miners, btc_earned from mining_summary_history order by timestamp desc limit 20;"
sqlite3 nrg_bloom.db "select distinct worker_name from worker_history where pool_name='TON-NRG' order by worker_name;"
```

## 6. Investigation order

1. Estimate the payout target.
2. Scan fresh wallets after the claimed startup date.
3. Rank by timing, cadence, size fit, and cleanliness.
4. Build the watchlist.
5. Trace the first spend.
