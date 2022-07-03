from scraping_bot import ScrapingBot


if __name__ == "__main__":
    sb = ScrapingBot()
    posts = sb.fetch_all_posts()
    print('Total of posts:', len(posts))
    print('-'*100)
    for post in posts:
        print(post)
    print('-'*100)
