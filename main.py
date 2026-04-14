import time
from ingestion import run_ingestion
from monitoring import render_progress, print_database
from google_play_scraper import Sort

APP_ID = "com.openai.chatgpt"
LANG = "en"
COUNTRY = "us"
SORT_MODE = Sort.NEWEST
TABLE_NAME = "comments"
ITERATE_TIMES = 1 #in K
SLEEP_TIME = 1  # 1 hour in seconds


if __name__ == "__main__":
    duplicates = 0
    print("[INFO] Starting data ingestion...")
    print(f"[INFO] Total iterations: {ITERATE_TIMES}")
    for i in range(ITERATE_TIMES):
        for j in range(10):
            duplicates += run_ingestion(
                app_id=APP_ID,
                lang=LANG,
                country=COUNTRY,
                sort_mode=SORT_MODE,
                table_name=TABLE_NAME
            )
            render_progress(j + 1, 1000, f"[INFO] Iteration {i + 1}")
        render_progress(i + 1, ITERATE_TIMES, "[INFO] Total progress")
        print()
        print(f"[INFO] Duplicates found: {duplicates}")
        time.sleep(SLEEP_TIME)
    print_database(APP_ID, TABLE_NAME)
