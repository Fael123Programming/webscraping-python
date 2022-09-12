from enum import Enum


class Weekday(Enum):
    SUNDAY = 1
    MONDAY = 2
    TUESDAY = 3
    WEDNESDAY = 4
    THURSDAY = 5
    FRIDAY = 6
    SATURDAY = 7


class PostCategory(Enum):
    UNKNOWN = 1
    # Add here the other types when inserted to database.


class DayPeriod(Enum):
    MORNING = 1
    AFTERNOON = 2
    NIGHT = 3
