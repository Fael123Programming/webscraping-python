from datetime import date


class Post:
    def __init__(self, category: str, title: str, publication_date: date):
        self._category = category
        self._title = title
        self._publication_date = publication_date

    @property
    def category(self):
        return self._category

    @property
    def title(self):
        return self._title

    @property
    def publication_date(self):
        return self._publication_date

    def __str__(self):
        return str(self.__dict__)
