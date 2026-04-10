from pathlib import Path
import sqlite3

DB_PATH = Path("comments.db")


def _create_table(
        cursor,
        table_name
    ):
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            review_id TEXT PRIMARY KEY,
            content TEXT NOT NULL,
            score INTEGER,
            date TEXT,
            appear_times INTEGER DEFAULT 1
        )
        """
    )

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


def _column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    return any(row[1] == column_name for row in columns)


def _needs_migration(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()

    if not columns:
        return False

    schema = {row[1]: row[2].upper() for row in columns}
    return schema.get("review_id") != "TEXT"


def _migrate_table(cursor, table_name):
    temp_table = f"{table_name}_old"

    cursor.execute(f"ALTER TABLE {table_name} RENAME TO {temp_table}")
    has_appear_times = _column_exists(cursor, temp_table, "appear_times")
    _create_table(cursor, table_name)
    if has_appear_times:
        cursor.execute(
            f"""
            INSERT OR IGNORE INTO {table_name}
            (review_id, content, score, date, appear_times)
            SELECT CAST(review_id AS TEXT), content, score, date, COALESCE(appear_times, 1)
            FROM {temp_table}
            """
        )
    else:
        cursor.execute(
            f"""
            INSERT OR IGNORE INTO {table_name}
            (review_id, content, score, date, appear_times)
            SELECT CAST(review_id AS TEXT), content, score, date, 1
            FROM {temp_table}
            """
        )
    cursor.execute(f"DROP TABLE {temp_table}")


def create_database(table_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    _create_table(cursor, table_name)
    if _needs_migration(cursor, table_name):
        _migrate_table(cursor, table_name)
    if not _column_exists(cursor, table_name, "appear_times"):
        cursor.execute(
            f"""
            ALTER TABLE {table_name}
            ADD COLUMN appear_times INTEGER DEFAULT 1
            """
        )

    conn.commit()
    conn.close()


def add_comment(review_id, content, score, date, table_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    normalized_content = content.strip()

    cursor.execute(
        f"""
        SELECT review_id
        FROM {table_name}
        WHERE TRIM(content) = ?
        ORDER BY rowid
        LIMIT 1
        """,
        (normalized_content,),
    )
    existing_row = cursor.fetchone()
    flag = 0

    if existing_row:
        existing_review_id = existing_row[0]
        cursor.execute(
            f"""
            UPDATE {table_name}
            SET appear_times = COALESCE(appear_times, 0) + 1
            WHERE review_id = ?
            """,
            (existing_review_id,),
        )
        flag = 1
    else:
        cursor.execute(
            f"""
            INSERT OR REPLACE INTO {table_name}
            (review_id, content, score, date, appear_times)
            VALUES (?, ?, ?, ?, 1)
            """,
            (str(review_id), normalized_content, score, str(date)),
        )

    conn.commit()
    conn.close()
    return flag


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
