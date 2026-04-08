from google_play_scraper import reviews, Sort

# Function to check if a string is valid UTF-8
def is_valid_utf8(s):
    if not isinstance(s, str):
        return False
    try:
        s.encode("utf-8")
        return True
    except UnicodeEncodeError:
        return False


def scrape_filtered_comments(
    app_id: str,
    lang: str,
    country: str,
    sort_mode: Sort,
):
    
    result, _ = reviews(
        app_id,
        lang=lang,
        country=country,
        sort=sort_mode,
        count=1,
        continuation_token=None,
    )

    if not result:
        print("[INFO] No more reviews found.")
        return None

    review = result[0]
    review_id = review.get("reviewId", "")
    content = review.get("content", "")
    score = review.get("score")
    date = review.get("at", "")

    if not review_id:
        print("[INFO] Skipping review with missing reviewId.")
        return None

    if not is_valid_utf8(content):
        print("[INFO] Skipping review with invalid UTF-8 content.")
        return None

    return review_id, content, score, date
