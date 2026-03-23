#!/usr/bin/env python3
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Estimate miner hashrate from BTC payout size."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--daily-btc", type=float, help="Observed BTC per day.")
    group.add_argument("--weekly-btc", type=float, help="Observed BTC per week.")
    parser.add_argument(
        "--network-btc-per-day",
        type=float,
        default=450.0,
        help="Network BTC mined per day. Default assumes 3.125 BTC subsidy era.",
    )
    parser.add_argument("--network-eh-low", type=float, default=750.0)
    parser.add_argument("--network-eh-high", type=float, default=900.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    daily_btc = args.daily_btc if args.daily_btc is not None else args.weekly_btc / 7.0
    share = daily_btc / args.network_btc_per_day
    low_ph = share * args.network_eh_low * 1_000
    high_ph = share * args.network_eh_high * 1_000
    midpoint = (low_ph + high_ph) / 2.0

    print(f"daily_btc={daily_btc:.8f}")
    print(f"network_share={share:.10f}")
    print(f"estimated_ph_low={low_ph:.2f}")
    print(f"estimated_ph_high={high_ph:.2f}")
    print(f"estimated_ph_mid={midpoint:.2f}")


if __name__ == "__main__":
    main()
