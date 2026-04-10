from scraper import scrape_filtered_comments
from google_play_scraper import Sort
from database_helper import add_comment, create_database

def run_ingestion(
    app_id: str,
    lang: str,
    country: str,
    sort_mode: Sort,
    table_name: str
):
    create_database(table_name)

    review = scrape_filtered_comments(
        app_id=app_id,
        lang=lang,
        country=country,
        sort_mode=sort_mode,
    )

    print(review)

    # if not review:
    #     return

    review_id, content, score, date = review
    duplicates = 0

    if review_id and content and score is not None and date:
        duplicates += add_comment(review_id, content, score, date, table_name)

    return duplicates

