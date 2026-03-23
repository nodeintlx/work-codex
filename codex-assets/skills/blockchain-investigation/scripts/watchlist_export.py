#!/usr/bin/env python3
import argparse
import csv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a watchlist CSV as Markdown.")
    parser.add_argument("--csv", required=True, help="Watchlist CSV file.")
    parser.add_argument("--title", default="Wallet Watchlist")
    parser.add_argument("--output", required=True, help="Markdown output path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with open(args.csv, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    lines = [
        f"# {args.title}",
        "",
        "| Label | Address | Role | Priority | Reason | First Seen | Last Seen |",
        "|---|---|---|---:|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {label} | {address} | {role} | {priority} | {reason} | {first_seen} | {last_seen} |".format(
                label=row.get("label", ""),
                address=row.get("address", ""),
                role=row.get("role", ""),
                priority=row.get("priority", ""),
                reason=row.get("reason", ""),
                first_seen=row.get("first_seen", ""),
                last_seen=row.get("last_seen", ""),
            )
        )

    with open(args.output, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
