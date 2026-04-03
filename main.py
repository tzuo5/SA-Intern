from create_db import create_database
from scraper import scrape_filtered_comments
from google_play_scraper import reviews, Sort


def main():
    create_database()
    scrape_filtered_comments(
        app_id="com.openai.chatgpt",
        lang="en",
        country="us",
        sort_mode=Sort.NEWEST,
        max_reviews=100,
        sleep_seconds=1.0
    )


if __name__ == "__main__":
    main()