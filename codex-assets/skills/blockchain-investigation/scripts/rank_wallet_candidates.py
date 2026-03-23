#!/usr/bin/env python3
import argparse
import csv
import datetime as dt
from math import fabs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rank Bitcoin wallet candidates.")
    parser.add_argument("--csv", required=True, help="Candidate CSV file.")
    parser.add_argument("--start-date", required=True, help="Target startup date, YYYY-MM-DD.")
    parser.add_argument("--expected-ph-low", type=float, required=True)
    parser.add_argument("--expected-ph-high", type=float, required=True)
    parser.add_argument("--network-btc-per-day", type=float, default=450.0)
    parser.add_argument("--network-eh-low", type=float, default=750.0)
    parser.add_argument("--network-eh-high", type=float, default=900.0)
    return parser.parse_args()


def implied_ph_mid(avg_daily_btc: float, network_btc_per_day: float, network_eh_low: float, network_eh_high: float) -> float:
    share = avg_daily_btc / network_btc_per_day
    low_ph = share * network_eh_low * 1_000
    high_ph = share * network_eh_high * 1_000
    return (low_ph + high_ph) / 2.0


def to_int(value: str) -> int:
    return int(value.strip() or "0")


def to_float(value: str) -> float:
    return float(value.strip() or "0")


def days_from_start(first_seen: str, start_date: dt.date) -> int:
    return abs((dt.date.fromisoformat(first_seen) - start_date).days)


def score_row(row: dict, args: argparse.Namespace, start_date: dt.date) -> tuple[float, float]:
    avg_daily_btc = to_float(row["avg_daily_btc"])
    payout_days = to_int(row["payout_days"])
    spends = to_int(row["spends"])
    non_pool_inflows = to_int(row["non_pool_inflows"])
    shared_batch_refs = to_int(row.get("shared_batch_refs", "0"))

    implied_mid = implied_ph_mid(
        avg_daily_btc,
        args.network_btc_per_day,
        args.network_eh_low,
        args.network_eh_high,
    )
    target_mid = (args.expected_ph_low + args.expected_ph_high) / 2.0

    timing_penalty = min(days_from_start(row["first_seen"], start_date) * 7.5, 30.0)
    size_penalty = min(fabs(implied_mid - target_mid) * 2.0, 30.0)
    cadence_bonus = min(payout_days * 2.5, 25.0)
    cleanliness_bonus = 15.0 if spends == 0 else max(0.0, 15.0 - spends * 5.0)
    contamination_penalty = min(non_pool_inflows * 10.0, 25.0)
    cohort_bonus = min(shared_batch_refs * 1.5, 10.0)

    score = 100.0 - timing_penalty - size_penalty - contamination_penalty + cadence_bonus + cleanliness_bonus + cohort_bonus
    return round(score, 2), round(implied_mid, 2)


def main() -> None:
    args = parse_args()
    start_date = dt.date.fromisoformat(args.start_date)

    with open(args.csv, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    ranked = []
    for row in rows:
        score, implied_mid = score_row(row, args, start_date)
        ranked.append(
            {
                "score": score,
                "implied_ph_mid": implied_mid,
                "address": row["address"],
                "first_seen": row["first_seen"],
                "avg_daily_btc": row["avg_daily_btc"],
                "payout_days": row["payout_days"],
                "spends": row["spends"],
                "non_pool_inflows": row["non_pool_inflows"],
                "notes": row.get("notes", ""),
            }
        )

    ranked.sort(key=lambda item: item["score"], reverse=True)

    writer = csv.DictWriter(
        __import__("sys").stdout,
        fieldnames=[
            "score",
            "implied_ph_mid",
            "address",
            "first_seen",
            "avg_daily_btc",
            "payout_days",
            "spends",
            "non_pool_inflows",
            "notes",
        ],
    )
    writer.writeheader()
    writer.writerows(ranked)


if __name__ == "__main__":
    main()
