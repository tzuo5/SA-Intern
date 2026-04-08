from ingestion import run_ingestion
from google_play_scraper import reviews, Sort

APP_ID = "com.openai.chatgpt"
LANG = "en"
COUNTRY = "us"
SORT_MODE = Sort.NEWEST
SLEEP_SECONDS = 1.0
TABLE_NAME = "comments"
ITERATE_TIMES = 100000

if __name__ == "__main__":
    for i in range(ITERATE_TIMES):
        run_ingestion(
            app_id=APP_ID,
            lang=LANG,
            country=COUNTRY,
            sort_mode=SORT_MODE,
            tabel_name=TABLE_NAME
        )
        print(f"[INFO] {i+1}/{ITERATE_TIMES} comments added.")
