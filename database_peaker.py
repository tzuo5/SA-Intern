import sqlite3
from pathlib import Path

DB_PATH = Path("comments.db")


def get_user_tables(cursor):
    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """
    )
    return [row[0] for row in cursor.fetchall()]


def print_table_data(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]

    print(f"\n=== Table: {table_name} ===")
    if not columns:
        print("[WARN] No columns found.")
        return

    print("Columns:", ", ".join(columns))

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    print(f"Total rows: {len(rows)}")
    if not rows:
        print("[INFO] No data.")
        return

    for idx, row in enumerate(rows, start=1):
        row_map = {columns[i]: row[i] for i in range(len(columns))}
        print(f"{idx}. {row_map}")


def is_table_empty(table_name: str) -> bool:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database file not found: {DB_PATH.resolve()}")

    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        tables = get_user_tables(cursor)
        if table_name not in tables:
            raise ValueError(f"Table not found: {table_name}")

        cursor.execute(f"SELECT 1 FROM {table_name} LIMIT 1")
        return cursor.fetchone() is None
    finally:
        conn.close()


def main():
    if not DB_PATH.exists():
        print(f"[ERROR] Database file not found: {DB_PATH.resolve()}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    tables = get_user_tables(cursor)
    if not tables:
        print("[INFO] No user tables found in database.")
        conn.close()
        return

    print(f"Database: {DB_PATH.resolve()}")
    for table_name in tables:
        print_table_data(cursor, table_name)

    conn.close()


if __name__ == "__main__":
    main()
