from scraping_bot import ScrapingBot


if __name__ == "__main__":
    sb = ScrapingBot()
    sb.fetch_featured_post()
    sb.fetch_all_posts()
