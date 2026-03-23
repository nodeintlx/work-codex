# Bitcoin Wallet Investigation Executive Summary

Prepared by: Aegis
Date: 2026-03-22
Matter context: TON-related operational investigation

## Purpose

Preserve the outcome of a Bitcoin wallet investigation that identified the most likely fresh Luxor-linked payout wallet for a mining operation believed to have started on March 6 or March 7, 2026.

## User Constraints

- Known pool: Luxor
- Known reference wallets:
  - TON known: `bc1qdcm607zgrgshnedv26nl70gkppm3zdpxtmkzsz`
  - Agnes: `1MdJhN26akTPbW1MTr11xiSLFiuEMmyaSB`
- Known fleet:
  - mainly `S19 90TH`
  - about `280-320` units
  - estimated footprint `25-31 PH`
- Exclude wallets that were already active before the March 6-7 startup window

## Investigative Method

The search was narrowed to:

- fresh Luxor recipients first seen on or after March 6, 2026
- low-history wallets
- repeated daily or weekly payout behavior
- payout size, variance, spends, and non-pool contamination

The analysis deliberately discarded older wallets that looked numerically plausible but violated the startup-date requirement.

## Primary Finding

The strongest target identified was:

- `bc1q38ck9dvr4c6qrkqn9690rcefvgrw53hxxxln7j`

Why it ranked first:

- first seen: `2026-03-07 05:05:27 UTC`
- `15` straight daily Luxor payouts from `2026-03-08` through `2026-03-22`
- average daily payout: `0.01124447 BTC/day`
- no spends
- almost no non-pool contamination

This was the cleanest fresh-start payout wallet in the March 6-22 window.

## Secondary Candidate

- `bc1qshnxdkkmup962764e7qhu09qakvtk7kwxvf46l`

Why it remains on the watchlist:

- first seen: `2026-03-10`
- `9` daily Luxor hits
- no spends
- average: `0.00924781 BTC/day`

This looks like a smaller same-pattern sibling, but not the primary operation wallet.

## Lower-Confidence Candidates

- `3FfYVe63gfE82MZbKZ9WWipbK8g1fUSMgi`
  - starts too late
  - already has a spend
  - noisier non-pool behavior
- `32fdnPfMtF2s7FtCReNTV8DeYrt4gBaH4b`
  - too much non-pool contamination

## Monitoring Stack

Primary:

- `bc1q38ck9dvr4c6qrkqn9690rcefvgrw53hxxxln7j`

Secondary:

- `bc1qshnxdkkmup962764e7qhu09qakvtk7kwxvf46l`

Context:

- TON known: `bc1qdcm607zgrgshnedv26nl70gkppm3zdpxtmkzsz`
- Agnes: `1MdJhN26akTPbW1MTr11xiSLFiuEMmyaSB`
- Luxor hubs:
  - `bc1qtzqyvfqqm4vc2xfcdjedt7d5k6t8h3vqhw2mpk`
  - `bc1ql4p0pcgvkjrld68uuvmj87vgactu0chm8zgx69`

## Recommended Next Step

Watch for the first spend from:

- `bc1q38ck9dvr4c6qrkqn9690rcefvgrw53hxxxln7j`
- `bc1qshnxdkkmup962764e7qhu09qakvtk7kwxvf46l`

That is the point where payout-edge analysis can become downstream cluster attribution.
