from datetime import datetime


class Post:
    def __init__(self, category='', title='', publication_date=datetime.now(), accesses=0, description=''):
        self._category = category
        self._title = title
        self._publication_date = publication_date
        self._accesses = accesses
        self._description = description

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category: str):
        if category is None or category.isspace() or len(category) == 0:
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
    def publication_date(self):
        return self._publication_date.__str__()

    @publication_date.setter
    def publication_date(self, publication_date: datetime):
        if publication_date is None:
            return
        self._publication_date = publication_date

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

    def __str__(self):
        return {'category': self._category, 'title': self._title, 'publication_date': self._publication_date.__str__(),
                'accesses': self._accesses, 'description': self._description}.__str__()
