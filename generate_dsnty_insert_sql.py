#!/usr/bin/env python3
import argparse
import csv
from datetime import datetime, date, timedelta
from pathlib import Path


TABLE_NAME = "CRWD_DNSTY.DNSTY.DNSTY"
TODAY = date.today()
COLUMN_ORDER = [
    "intervaltime",
    "intervaltime_epoch",
    "building_code",
    "building_type",
    "floor",
    "total_users",
    "density",
    "loadg_dtm",
]
STRING_COLUMNS = {"building_code", "building_type", "floor"}
NUMERIC_COLUMNS = {"intervaltime_epoch", "total_users", "density"}


def escape_sql_string(value: str) -> str:
    return value.replace("'", "''")


def intervaltime_for_date(original: str, target_date: date) -> str:
    dt = datetime.strptime(original.strip(), "%Y-%m-%d %H:%M:%S.%f")
    dt = dt.replace(year=target_date.year, month=target_date.month, day=target_date.day)
    ms = dt.microsecond // 1000
    return dt.strftime("%Y-%m-%d %H:%M:%S.") + f"{ms:03d}"


def sql_literal(column_name: str, value: str, target_date: date, row: dict[str, str] = None) -> str:
    if column_name == "intervaltime":
        return f"'{intervaltime_for_date(row['intervaltime'], target_date)}'"

    if column_name == "loadg_dtm":
        return "CURRENT_TIMESTAMP"

    if value is None:
        return "NULL"

    trimmed = value.strip()
    if trimmed == "":
        return "NULL"

    if column_name in NUMERIC_COLUMNS:
        return trimmed

    if column_name in STRING_COLUMNS:
        return f"'{escape_sql_string(trimmed)}'"

    return f"'{escape_sql_string(trimmed)}'"


def build_insert_statement(row: dict[str, str], target_date: date) -> str:
    values = [sql_literal(column_name, row.get(column_name), target_date, row) for column_name in COLUMN_ORDER]
    columns = ", ".join(COLUMN_ORDER)
    rendered_values = ", ".join(values)
    return f"INSERT INTO {TABLE_NAME} ({columns}) VALUES ({rendered_values});"


TIME_START = (8, 0, 0)
TIME_END = (20, 0, 0)


def in_time_range(intervaltime: str) -> bool:
    dt = datetime.strptime(intervaltime.strip(), "%Y-%m-%d %H:%M:%S.%f")
    t = (dt.hour, dt.minute, dt.second)
    return TIME_START <= t <= TIME_END


def iterate_dates(start_date: date, end_date: date):
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)


def generate_sql(csv_path: Path, output_path: Path, start_date: date, end_date: date) -> int:
    with csv_path.open("r", newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = [row for row in reader if in_time_range(row["intervaltime"])]

    statements = []
    for target_date in iterate_dates(start_date, end_date):
        statements.extend(build_insert_statement(row, target_date) for row in rows)

    with output_path.open("w", encoding="utf-8") as output_file:
        output_file.write(f"-- Generated from {csv_path.name}\n")
        output_file.write(f"-- Target table: {TABLE_NAME}\n")
        if start_date == end_date:
            output_file.write(f"-- intervaltime: requested date ({start_date}) with original time portion\n")
        else:
            output_file.write(f"-- Date range: {start_date} to {end_date}\n")
        output_file.write("-- loadg_dtm: CURRENT_TIMESTAMP\n\n")
        output_file.write("\n".join(statements))
        output_file.write("\n")

    return len(statements)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate INSERT SQL for DNSTY CSV data.")
    parser.add_argument("csv_path", help="Path to the input CSV file.")
    parser.add_argument(
        "--start-date",
        help="Start date for intervaltime substitution in YYYY-MM-DD format. Defaults to today.",
    )
    parser.add_argument(
        "--end-date",
        help="End date for intervaltime substitution in YYYY-MM-DD format. Defaults to start-date.",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory for the generated INSERT_DNSTY_<timestamp>.sql file.",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv_path).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    start_date = datetime.strptime(args.start_date, "%Y-%m-%d").date() if args.start_date else TODAY
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d").date() if args.end_date else start_date
    if end_date < start_date:
        raise ValueError("end-date must be on or after start-date")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_path = output_dir / f"INSERT_DNSTY_{timestamp}.sql"

    output_dir.mkdir(parents=True, exist_ok=True)
    row_count = generate_sql(csv_path, output_path, start_date, end_date)
    print(f"Generated {row_count} INSERT statements")
    print(output_path)


if __name__ == "__main__":
    main()