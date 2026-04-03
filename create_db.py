import sqlite3

DB_PATH = "comments.db"
TABLE_NAME = "ChatGPT_comments"


def _create_table(cursor):
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            review_id TEXT PRIMARY KEY,
            content TEXT NOT NULL,
            score INTEGER,
            date TEXT
        )
        """
    )


def _needs_migration(cursor):
    cursor.execute(f"PRAGMA table_info({TABLE_NAME})")
    columns = cursor.fetchall()

    if not columns:
        return False

    schema = {row[1]: row[2].upper() for row in columns}
    return schema.get("review_id") != "TEXT"


def _migrate_table(cursor):
    temp_table = f"{TABLE_NAME}_old"

    cursor.execute(f"ALTER TABLE {TABLE_NAME} RENAME TO {temp_table}")
    _create_table(cursor)
    cursor.execute(
        f"""
        INSERT OR IGNORE INTO {TABLE_NAME} (review_id, content, score, date)
        SELECT CAST(review_id AS TEXT), content, score, date
        FROM {temp_table}
        """
    )
    cursor.execute(f"DROP TABLE {temp_table}")


def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    _create_table(cursor)
    if _needs_migration(cursor):
        _migrate_table(cursor)

    conn.commit()
    conn.close()


def add_comment(review_id, content, score, date):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        f"""
        INSERT OR REPLACE INTO {TABLE_NAME} (review_id, content, score, date)
        VALUES (?, ?, ?, ?)
        """,
        (str(review_id), content, score, str(date)),
    )

    conn.commit()
    conn.close()
