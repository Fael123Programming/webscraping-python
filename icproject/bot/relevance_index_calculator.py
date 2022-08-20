from icproject.bot.post import Post
from datetime import datetime


class RelevanceIndexCalculator:

    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(RelevanceIndexCalculator, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def calculate_of(post: Post):
        if post.publication_timestamp is None or post.accesses is None or post.accesses == 0:
            post.relevance_index = None
        else:
            time_since_publication = datetime.now() - post.publication_timestamp
            hours_since_publication = time_since_publication.total_seconds() / 3600
            post.relevance_index = round(post.accesses / hours_since_publication, 2)
