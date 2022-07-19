from datetime import datetime


class Post:

    def __init__(self, category=1, title='', publication_timestamp=datetime.now(), accesses=0, description='',
                 relevance_index=0):
        self._category = category
        self._title = title
        self._publication_timestamp = publication_timestamp
        self._accesses = accesses
        self._description = description
        self._relevance_index = relevance_index

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category: int):
        if category < 1:
            return
        self._category = category

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title: str):
        if title is None or title.isspace() or len(title) == 0:
            return
        self._title = title

    @property
    def publication_timestamp(self):
        return self._publication_timestamp

    @publication_timestamp.setter
    def publication_timestamp(self, publication_timestamp: datetime):
        if publication_timestamp is None:
            return
        self._publication_timestamp = publication_timestamp

    @property
    def accesses(self):
        return self._accesses

    @accesses.setter
    def accesses(self, accesses: int):
        if accesses < 0:
            return
        self._accesses = accesses

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description: str):
        if description is None or description.isspace() or len(description) == 0:
            return
        self._description = description

    @property
    def relevance_index(self):
        return self._relevance_index

    @relevance_index.setter
    def relevance_index(self, relevance_index: int):
        if relevance_index < 0:
            return
        self._relevance_index = relevance_index

    def __str__(self):
        return {
                'category': self._category,
                'title': self._title,
                'publication_timestamp': self._publication_timestamp.__str__(),
                'accesses': self._accesses,
                'description': self._description,
                'relevance_index': self._relevance_index
        }.__str__()

    def to_database_format(self) -> tuple:
        return self._category, self._title, self._description, self._publication_timestamp.__str__(), self._accesses, \
               self._relevance_index,
