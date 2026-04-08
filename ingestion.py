from scraper import scrape_filtered_comments
from google_play_scraper import Sort
from database_helper import add_comment, create_database

def run_ingestion(
    app_id: str,
    lang: str,
    country: str,
    sort_mode: Sort,
    tabel_name: str
):
    create_database(tabel_name)

    review = scrape_filtered_comments(
        app_id=app_id,
        lang=lang,
        country=country,
        sort_mode=sort_mode,
    )

    if not review:
        return

    review_id, content, score, date = review

    if review_id and content and score is not None and date:
        add_comment(review_id, content, score, date, tabel_name)



