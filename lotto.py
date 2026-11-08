"""Report the seven most frequent NY Lotto numbers using only Python's standard library."""

import argparse
import csv
from collections import Counter
from pathlib import Path


DEFAULT_CSV = "Lottery_NY_Lotto_Winning_Numbers__Beginning_2001_20261108.csv"


def count_numbers(path, include_bonus=False):
    """Count winning numbers; optionally count the separate bonus number too."""
    counts = Counter()
    draws = 0
    with Path(path).open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        required = {"Winning Numbers"}
        if include_bonus:
            required.add("Bonus #")
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("CSV must contain columns: " + ", ".join(sorted(required)))
        for row in reader:
            if not any(row.values()):
                continue
            try:
                numbers = [int(value) for value in row["Winning Numbers"].split()]
                if len(numbers) != 6 or len(set(numbers)) != 6:
                    raise ValueError("expected six distinct winning numbers")
                if include_bonus:
                    bonus = int(row["Bonus #"])
                    if bonus in numbers:
                        raise ValueError("bonus duplicates a winning number")
                    numbers.append(bonus)
                if any(number < 1 or number > 59 for number in numbers):
                    raise ValueError("numbers must be between 1 and 59")
            except (ValueError, AttributeError, TypeError) as error:
                raise ValueError(f"Invalid draw at CSV line {reader.line_num}: {error}") from error
            counts.update(numbers)
            draws += 1
    if not draws:
        raise ValueError("CSV contains no draws")
    return counts, draws


def top_seven(counts):
    """Break frequency ties by choosing the smaller number first."""
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:7]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", nargs="?", type=Path,
                        default=Path(__file__).resolve().parent / DEFAULT_CSV,
                        help="CSV to analyze (default: the bundled CSV)")
    parser.add_argument("--include-bonus", action="store_true",
                        help="count Bonus # as well as Winning Numbers")
    args = parser.parse_args()
    try:
        counts, draws = count_numbers(args.csv_file, args.include_bonus)
    except (OSError, UnicodeError, ValueError, csv.Error) as error:
        parser.exit(1, f"Error: {error}\n")
    mode = "winning and bonus numbers" if args.include_bonus else "winning numbers only"
    print(f"Top 7 numbers across {draws:,} draws ({mode})")
    print(f"{'Number':>6}  {'Occurrences':>11}")
    for number, frequency in top_seven(counts):
        print(f"{number:02d}      {frequency:>11,}")
    print("Ties are resolved by smaller number first. Extra # is excluded.")


if __name__ == "__main__":
    main()
