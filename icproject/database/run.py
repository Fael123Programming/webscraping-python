from database_connection import DatabaseConnection
from icproject.bot.post import Post
from datetime import datetime

if __name__ == '__main__':
    conn = DatabaseConnection()
    conn.connect()
    conn.insert_post(
        Post(
            'unknown',
            'My test post',
            datetime(2022, 7, 14, 11, 15),
            100,
            'This is a test description for a test post',
            7
        )
    )
    conn.disconnect()
