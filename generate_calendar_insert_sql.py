#!/usr/bin/env python3
import argparse
import csv
from datetime import datetime
from pathlib import Path


TABLE_NAME = "CRWD_DNSTY.[REF].CALENDAR"
COLUMN_ORDER = [
    "CAL_D",
    "DAY_TP",
    "PH_F",
    "TERM_F",
    "LOADG_DTM",
]

def escape_sql_string(value: str) -> str:
    return value.replace("'", "''")


def sql_literal(column_name: str, value: str) -> str:
    if column_name == "LOADG_DTM":
        return "CURRENT_TIMESTAMP"

    if value is None:
        return "NULL"

    trimmed = value.strip()
    if trimmed == "":
        return "NULL"

    return f"'{escape_sql_string(trimmed)}'"


def build_insert_statement(row: dict[str, str]) -> str:
    values = [sql_literal(col, row.get(col)) for col in COLUMN_ORDER]
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
        output_file.write(f"-- Target table: {TABLE_NAME}\n\n")
        output_file.write("\n".join(statements))
        output_file.write("\n")

    return len(statements)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate INSERT SQL for CALENDAR CSV data.")
    parser.add_argument("csv_path", help="Path to the input CSV file.")
    parser.add_argument(
        "--output-dir",
        default="sql",
        help="Directory for the generated INSERT_CALENDAR_<timestamp>.sql file. Defaults to 'sql'.",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv_path).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_path = output_dir / f"INSERT_CALENDAR_{timestamp}.sql"

    output_dir.mkdir(parents=True, exist_ok=True)
    row_count = generate_sql(csv_path, output_path)
    print(f"Generated {row_count} INSERT statements")
    print(output_path)


if __name__ == "__main__":
    main()
