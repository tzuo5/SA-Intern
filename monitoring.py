import sqlite3
import sys
from datetime import datetime

from database_helper import DB_PATH, get_user_tables


def render_progress(current: int, total: int, label: str, width: int = 30):
    filled = int(width * current / total)
    bar = "#" * filled + "-" * (width - filled)
    sys.stdout.write(f"\r{label} [{bar}] [{current}/{total}]")
    sys.stdout.flush()

def _format_review_date(raw_date) -> str:
    if not raw_date:
        return ""

    raw_text = str(raw_date)
    try:
        return datetime.fromisoformat(raw_text).strftime("%Y/%m/%d")
    except ValueError:
        normalized = raw_text.replace("-", "/")
        return normalized[:10] if len(normalized) >= 10 else normalized


def print_database(app_id: str, table_name: str):
    if not DB_PATH.exists():
        print(f"[INFO] Database file not found: {DB_PATH.resolve()}")
        return

    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        tables = get_user_tables(cursor)
        if table_name not in tables:
            print(f"[INFO] Table not found: {table_name}")
            return

        cursor.execute(
            f"""
            SELECT review_id, score, date, content, COALESCE(appear_times, 1)
            FROM {table_name}
            ORDER BY COALESCE(appear_times, 1) DESC, rowid ASC
            """
        )
        rows = cursor.fetchall()
    finally:
        conn.close()
    print("=" * 48)
    print("Summary of the process:")
    print(f"App ID: {app_id}, Reviews Count: {len(rows)}")
    print("-" * 48)

    for review_id, score, date, content, appear_times in rows:
        print(f"review id: {review_id}")
        print(f"score: {score}")
        print(f"date: {_format_review_date(date)}")
        print(f"content: {content}")
        print(f"appears time: {appear_times}")
        print("--------------")
