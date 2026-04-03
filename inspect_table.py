#!/usr/bin/env python3
"""Inspect a SQLAlchemy table structure and print it in a table-like format."""

import argparse
from sqlalchemy import inspect
from main import app, db


def format_table(data, headers):
    # compute maximum widths for columns
    widths = [len(h) for h in headers]
    for row in data:
        for i, value in enumerate(row):
            widths[i] = max(widths[i], len(str(value)))

    # header
    header_line = " | ".join(f"{h:<{widths[i]}}" for i, h in enumerate(headers))
    separator = "-+-".join("-" * widths[i] for i in range(len(headers)))

    print(header_line)
    print(separator)

    for row in data:
        print(" | ".join(f"{str(v):<{widths[i]}}" for i, v in enumerate(row)))


def main():
    parser = argparse.ArgumentParser(description='Inspect SQLAlchemy table columns.')
    parser.add_argument('table', help='Table name to inspect')
    args = parser.parse_args()

    # 👇 FIX STARTS HERE
    with app.app_context():
        inspector = inspect(db.engine)

        if args.table not in inspector.get_table_names():
            raise SystemExit(
                f"Table '{args.table}' not found. Available tables: {', '.join(inspector.get_table_names())}"
            )

        cols = inspector.get_columns(args.table)

        rows = []
        for c in cols:
            rows.append([
                c['name'],
                str(c['type']),
                c.get('nullable', ''),
                'Yes' if c.get('primary_key') else 'No',
                str(c.get('default', ''))
            ])

        format_table(rows, ['name', 'type', 'nullable', 'pk', 'default'])

if __name__ == '__main__':
    main()


# python3 inspect_table.py user
# python3 inspect_table.py post
# python3 inspect_table.py comment
# python3 inspect_table.py category