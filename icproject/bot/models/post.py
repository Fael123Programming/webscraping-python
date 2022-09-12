from datetime import datetime
from icproject.bot.enums.enums import *


class Post:

    def __init__(self, category: PostCategory, weekday: Weekday, day_period: DayPeriod, title: str,
                 description: str | None, publication_timestamp: datetime | None, images_count: int,
                 accesses: int | None, relevance_index: float | None):
        self._category = category
        self._weekday = weekday
        self._day_period = day_period
        self._title = title
        self._description = description
        self._publication_timestamp = publication_timestamp
        self._images_count = images_count
        self._accesses = accesses
        self._relevance_index = relevance_index

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category: int):
        self._category = category

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title: str):
        self._title = title

    @property
    def publication_timestamp(self):
        return self._publication_timestamp

    @publication_timestamp.setter
    def publication_timestamp(self, publication_timestamp: datetime | None):
        self._publication_timestamp = publication_timestamp

    @property
    def accesses(self):
        return self._accesses

    @accesses.setter
    def accesses(self, accesses: int | None):
        self._accesses = accesses

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description: str | None):
        self._description = description

    @property
    def relevance_index(self):
        return self._relevance_index

    @relevance_index.setter
    def relevance_index(self, relevance_index: float | None):
        self._relevance_index = relevance_index

    def __str__(self):
        return {
            'category': self._category,
            'weekday': self._weekday,
            'day_period': self._day_period,
            'title': self._title,
            'description': self._description,
            'publication_timestamp': self._publication_timestamp.__str__(),
            'images_count': self._images_count,
            'accesses': self._accesses,
            'relevance_index': self._relevance_index
        }.__str__()

    def to_database_format(self) -> tuple:
        publication_timestamp = self._publication_timestamp
        publication_timestamp = publication_timestamp.__str__() if publication_timestamp is not None else None
        return self._category, self._weekday, self._day_period, self._title, self._description, publication_timestamp, \
            self._images_count, self._accesses, self._relevance_index,
