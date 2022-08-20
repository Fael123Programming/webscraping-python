import psycopg2
from icproject.database.config import config
from icproject.bot.post import Post


class DatabaseConnection:

    def __init__(self):
        self._conn = None

    def connect(self):
        try:
            params = config()
            print('-' * 150)
            print('Connecting to PostgreSQL database...')
            self._conn = psycopg2.connect(**params)
            cursor = self._conn.cursor()
            cursor.execute('SELECT version();')
            print(f'PostgreSQL database version: {cursor.fetchone()[0]}')
            print('-' * 150)
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print('#' * 150)
            print('The following error has been thrown while trying to set connection with the database:')
            print(error)
            print('#' * 150)
            if self._conn is not None:
                self._conn.close()

    def get_post_categories(self) -> list:
        cursor = self._conn.cursor()
        cursor.execute('SELECT * FROM post_category;')
        post_categories = list()
        for category in cursor.fetchall():
            post_categories.append(category)
        cursor.close()
        return post_categories

    def insert_post(self, post: Post):
        cursor = self._conn.cursor()
        statement = """
            INSERT INTO website_post (fk_post_category, post_title, post_description, 
            post_publication_timestamp, post_accesses, relevance_index) VALUES 
            (%s, %s, %s, %s, %s, %s);
        """
        cursor.execute(statement, post.to_database_format())
        self._conn.commit()
        cursor.close()

    def insert_posts(self, post_list: list):
        cursor = self._conn.cursor()
        statement = """
                    INSERT INTO website_post (fk_post_category, post_title, post_description, 
                    post_publication_timestamp, post_accesses, relevance_index) VALUES 
                    (%s, %s, %s, %s, %s, %s);
                """
        post_list_database_format = list()
        for post in post_list:
            post_list_database_format.append(post.to_database_format())
        cursor.executemany(statement, post_list_database_format)
        self._conn.commit()
        cursor.close()

    def disconnect(self):
        if self._conn is not None:
            self._conn.close()
            print('----- Connection with PostgreSQL database ended.')
