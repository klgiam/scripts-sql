#!/usr/bin/env python3
import argparse
import csv
from datetime import datetime
from pathlib import Path


TABLE_NAME = "CRWD_DNSTY.DNSTY.DNSTY"
FIXED_INTERVALTIME = "2026-03-23 17:00:00.000"
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


def sql_literal(column_name: str, value: str) -> str:
    if column_name == "intervaltime":
        return f"'{FIXED_INTERVALTIME}'"

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


def build_insert_statement(row: dict[str, str]) -> str:
    values = [sql_literal(column_name, row.get(column_name)) for column_name in COLUMN_ORDER]
    columns = ", ".join(COLUMN_ORDER)
    rendered_values = ", ".join(values)
    return f"INSERT INTO {TABLE_NAME} ({columns}) VALUES ({rendered_values});"


def generate_sql(csv_path: Path, output_path: Path) -> int:
    with csv_path.open("r", newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

    statements = [build_insert_statement(row) for row in rows]

    with output_path.open("w", encoding="utf-8") as output_file:
        output_file.write(f"-- Generated from {csv_path.name}\n")
        output_file.write(f"-- Target table: {TABLE_NAME}\n")
        output_file.write(f"-- Fixed intervaltime: {FIXED_INTERVALTIME}\n")
        output_file.write("-- loadg_dtm: CURRENT_TIMESTAMP\n\n")
        output_file.write("\n".join(statements))
        output_file.write("\n")

    return len(statements)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate INSERT SQL for DNSTY CSV data.")
    parser.add_argument("csv_path", help="Path to the input CSV file.")
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory for the generated INSERT_DNSTY_<timestamp>.sql file.",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv_path).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_path = output_dir / f"INSERT_DNSTY_{timestamp}.sql"

    output_dir.mkdir(parents=True, exist_ok=True)
    row_count = generate_sql(csv_path, output_path)
    print(f"Generated {row_count} INSERT statements")
    print(output_path)


if __name__ == "__main__":
    main()