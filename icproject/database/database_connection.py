import psycopg2
from icproject.database.config import config
from icproject.bot.post import Post


class DatabaseConnection:

    def __init__(self):
        self._conn = None

    def connect(self):
        try:
            params = config()
            print('-' * 100)
            print('Connecting to the PostgreSQL database...')
            self._conn = psycopg2.connect(**params)
            cursor = self._conn.cursor()
            cursor.execute('SELECT version();')
            print(f'PostgreSQL database version: {cursor.fetchone()[0]}')
            print('-' * 100)
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print('#' * 100)
            print('The following error has been thrown while trying to set connection with the database:')
            print(error)
            print('#' * 100)
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
        fk_post_category = self.get_fk_post_category_of(post)
        statement = f"INSERT INTO website_post (fk_post_category, post_title, post_description, " \
                    f"post_publication_timestamp, post_accesses, relevance_index) VALUES ({fk_post_category}, " \
                    f"'{post.title}', '{post.description}', '{post.publication_timestamp.__str__()}', {post.accesses}, " \
                    f"{post.relevance_index});"
        cursor.execute(statement)
        cursor.close()

    def get_fk_post_category_of(self, post: Post) -> int:
        post_categories = self.get_post_categories()
        for category in post_categories:
            if category[1] == post.category:
                return category[0]

    def disconnect(self):
        if self._conn is not None:
            self._conn.close()
            print('Connection with the PostgreSQL database ended.')


