import json
import os

from google_play_scraper import reviews, Sort
import time

APP_ID = "com.openai.chatgpt"
LANG = "en"
COUNTRY = "us"
SORT_MODE = Sort.NEWEST
MAX_REVIEWS = 10000
SLEEP_SECONDS = 1.0
OUTPUT_PATH = "/Users/zuotianhao/Desktop/sa intern/Phase 1/review.JSON"

# Function to count the number of words in a given text
def word_count(text: str) -> int:
    if not text:
        return 0
    return len(text.split())

# Function to check if a string is valid UTF-8
def is_valid_utf8(s):
    if not isinstance(s, str):
        return False
    try:
        s.encode("utf-8")
        return True
    except UnicodeEncodeError:
        return False


def print_filtered_comments(
    app_id: str,
    lang: str = "en",
    country: str = "us",
    sort_mode=Sort.NEWEST,
    max_reviews: int = 20,
    sleep_seconds: float = 1.0
):

    total_printed = 0
    continuation_token = None

    while total_printed < max_reviews:
        result, continuation_token = reviews(
            app_id,
            lang=lang,
            country=country,
            sort=sort_mode,
            count = 100,
            continuation_token=continuation_token,
        )

        if not result:
            print("[INFO] No more reviews found.")
            break

        for r in result:
            review_id = r.get("reviewId")
            content = r.get("content", "")
            score = r.get("score", "N/A")
            date = str(r.get("at", "N/A"))


            # if word_count(content) <= 7:
            #     continue
            
            if not is_valid_utf8(content):
                continue
            
            data = {
                "review_id": review_id,
                "date": date,
                "score": score,
                "content": content
            }

            if not os.path.exists(OUTPUT_PATH) or os.path.getsize(OUTPUT_PATH) == 0:
                all_reviews = []

            else:
                with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
                    all_reviews = json.load(f)

            all_reviews.append(data)

            with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
                json.dump(all_reviews, f, ensure_ascii=False, indent=4)

            # print("=" * 80)
            # print(f"Review Number: {total_printed}")
            # print(f"User: {user_name}")
            # print(f"Rating: {score}")
            # print(f"Date: {review_time}")
            # print("Comment:")
            # print(content)
            # print("=" * 80)
            # print()

            total_printed += 1

            if total_printed >= max_reviews:
                break

        if total_printed >= max_reviews:
            break

        print(f"[INFO] Now printed: {total_printed}.")

        time.sleep(sleep_seconds)

    print(f"[INFO] Total printed: {total_printed}.")

if __name__ == "__main__":
    print_filtered_comments(
        app_id=APP_ID,
        lang=LANG,
        country=COUNTRY,
        sort_mode=SORT_MODE,
        max_reviews=MAX_REVIEWS,
        sleep_seconds=SLEEP_SECONDS,
    )