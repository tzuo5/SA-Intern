import time
from ingestion import run_ingestion
from google_play_scraper import reviews, Sort

APP_ID = "com.openai.chatgpt"
LANG = "en"
COUNTRY = "us"
SORT_MODE = Sort.NEWEST
TABLE_NAME = "comments"
ITERATE_TIMES = 100 #in K
SLEEP_TIME = 1  # 1 hour in seconds

if __name__ == "__main__":
    for i in range(ITERATE_TIMES):
        for j in range(1000):
            run_ingestion(
                app_id=APP_ID,
                lang=LANG,
                country=COUNTRY,
                sort_mode=SORT_MODE,
                table_name=TABLE_NAME
            )
            print(f"[INFO]     {j+1}/1000 comments added in iteration {i+1}.")
        print(f"[INFO] {i+1}/{ITERATE_TIMES} K comments added.")
        time.sleep(SLEEP_TIME)