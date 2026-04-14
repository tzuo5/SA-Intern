# SA-Intern

## Overview

This repository contains the current Phase 1 monitoring and ingestion prototype for Google Play Store reviews.

The current target app is:

- `com.openai.chatgpt`

The goal of the current implementation is to repeatedly pull reviews, validate the incoming records, store them in a local SQLite database, track repeated review content, and print a readable monitoring summary from the database.

## What The Current Monitoring Layer Tracks

The current monitoring layer is console-based and database-backed. It currently tracks:

- ingestion progress across repeated runs
- duplicate review content encountered during repeated scraping
- basic validation of incoming review records
- the current deduplicated database state
- per-review repeat frequency through `appear_times`

There is no dashboard yet. Monitoring output is currently produced through logs, progress bars, and printed database summaries.

## Current Monitoring Logic

The current end-to-end flow is:

1. `main.py` starts repeated ingestion runs for a configured app, language, country, and sort mode.
2. `scraper.py` fetches reviews from Google Play one at a time using a continuation token so the scraper can move forward across calls.
3. `scraper.py` validates each fetched review before insertion.
4. `ingestion.py` ensures the target SQLite table exists and passes the review to the database layer.
5. `database_helper.py` stores new reviews or increments the repeat counter when the same trimmed review content already exists.
6. `monitoring.py` prints a summary of the stored database contents, sorted by repeat count from high to low.

## What Counts As A Duplicate Right Now

The current duplicate logic is content-based, not `review_id`-based.

- A new review is treated as a duplicate when `TRIM(content)` matches an existing row in the same table.
- When that happens, the existing row is kept and its `appear_times` value is incremented.
- If the content is new, a new row is inserted with `appear_times = 1`.

This means different users leaving exactly the same text will currently be collapsed into one stored row.

## Validation Currently Implemented

Before insertion, the current pipeline checks:

- `reviewId` must exist
- review `content` must be valid UTF-8
- `score` must not be `None`
- `date` must exist

If a record fails validation, it is skipped.

## Relevant Scripts

| Script | Role |
| --- | --- |
| [`main.py`](main.py) | Entry point for repeated ingestion, progress display, duplicate counting, and final database printout |
| [`scraper.py`](scraper.py) | Pulls one Google Play review at a time and applies basic validation |
| [`ingestion.py`](ingestion.py) | Connects the scraper and database layer |
| [`database_helper.py`](database_helper.py) | Creates/migrates the SQLite table and updates `appear_times` for duplicates |
| [`monitoring.py`](monitoring.py) | Renders the progress bar and prints a database summary sorted by repeat count |
| [`comments.db`](comments.db) | Local SQLite database storing collected reviews |

## Current Database Schema

The active SQLite schema used by the monitoring layer is:

```sql
CREATE TABLE IF NOT EXISTS comments (
    review_id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    score INTEGER,
    date TEXT,
    appear_times INTEGER DEFAULT 1
);
```

Stored fields:

- `review_id`: Google Play review ID
- `content`: review text
- `score`: review rating
- `date`: review timestamp
- `appear_times`: how many times the same trimmed content has been seen

## Current Run Configuration

The current default configuration in [`main.py`](main.py) is:

- `APP_ID = "com.openai.chatgpt"`
- `LANG = "en"`
- `COUNTRY = "us"`
- `SORT_MODE = Sort.NEWEST`
- `TABLE_NAME = "comments"`

## Example Monitoring Output

### Example Console Summary

The monitoring layer now includes a `print_database(app_id, table_name)` function that prints the full database contents in repeat-count order.

Example:

```text
================================================
Summary of the process:
App ID: com.openai.chatgpt, Reviews Count: 139
------------------------------------------------
review id: edbbded9-f247-4817-93b4-9ab4fefdc9f7
score: 4
date: 2026/04/09
content: 💗
appears time: 1035
--------------
review id: 3838ea68-8899-49e9-89ef-bf21686e2581
score: 3
date: 2026/04/07
content: nice
appears time: 12
--------------
```

### Current Local Snapshot

Snapshot below was taken from the local `comments` table on **April 14, 2026**.

| Metric | Value |
| --- | --- |
| Unique stored reviews | 139 |
| Rows with `appear_times > 1` | 10 |
| Highest observed repeat count | 1035 |

Top repeated entries:

| review_id | score | date | content preview | appear_times |
| --- | --- | --- | --- | --- |
| `edbbded9-f247-4817-93b4-9ab4fefdc9f7` | 4 | 2026-04-09 | `💗` | 1035 |
| `3838ea68-8899-49e9-89ef-bf21686e2581` | 3 | 2026-04-07 | `nice` | 12 |
| `f75d3fe3-6d62-44cd-926c-cf58b00b9057` | 5 | 2026-04-13 | `unic app` | 4 |
| `265b3ea3-7c33-474a-8f57-7900eff7b339` | 5 | 2026-04-13 | `likes` | 4 |
| `e3d1dc62-d533-485a-a0d0-4863d74cfca9` | 5 | 2026-04-13 | `constructor` | 4 |

## How To Run

Install dependencies first, then run:

```bash
python3 main.py
```

If you only want to print the current database summary:

```bash
python3 - <<'PY'
from monitoring import print_database
print_database("com.openai.chatgpt", "comments")
PY
```

## Current Limitations

This is the current prototype state, not the final monitoring design. Current limitations include:

- duplicate detection is based on review text, not unique user-review identity
- monitoring is local and console-only; there is no persistent dashboard or alerting layer yet
- the current pipeline stores a single representative row for repeated content rather than every raw review event
- the workflow is focused on one app configuration at a time

## Next Extension Areas

The next iteration could extend this into:

- clearer monitoring metrics across runs
- timestamped run logs
- better duplicate definitions
- simple plots or dashboards for repeat frequency, sentiment, and rating drift
- exportable summary reports for easier review on GitHub
