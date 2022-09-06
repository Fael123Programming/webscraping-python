from icproject.bot.bot import Bot
from datetime import datetime
from icproject.database.database_connection import DatabaseConnection


if __name__ == "__main__":
    # bot_urls = Bot()
    # bot_urls.export_post_urls_to_csv()
    # start_timestamp = datetime.now()
    # bot_data = Bot()
    # posts = bot_data.get_posts_data()
    # end_timestamp = datetime.now()
    # print('-' * 150)
    # print(f'Total of {len(posts)} posts fetched')
    # print(f'Timestamp start: {start_timestamp}')
    # print(f'Timestamp end: {end_timestamp}')
    # print(f'It took {end_timestamp - start_timestamp}.')
    conn = DatabaseConnection()
    conn.connect()
    # conn.insert_posts(posts)
    most_relevant_posts = conn.get_most_relevant_posts_in_website(quantity=10)
    print('-' * 170)
    print(f'{"Post Title":<100}{"Publication Timestamp":<50}{"Relevance Index"}')
    print('-' * 170)
    for post in most_relevant_posts:
        print(f'{post[0]:<100}{post[1].__str__():<50}{float(post[2])}')
    print('-' * 170)
    conn.disconnect()
