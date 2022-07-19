from database_connection import DatabaseConnection
from icproject.bot.scraping_bot import ScrapingBot

# 2363 posts as of 2022-07-19

if __name__ == '__main__':
    # conn = DatabaseConnection()
    bot = ScrapingBot()
    bot.fetch_all_posts()
    # posts = list()
    # try:
    #     posts.append(bot.fetch_featured_post())
    #     posts.extend(bot.fetch_all_posts())
    # except Exception as e:
    #     print('Exception got thrown')
    #     print(e)
    #     bot.force_quit()
    # else:
    #     conn.connect()
    #     conn.insert_post_list(posts)
    #     conn.disconnect()
