from configparser import RawConfigParser
from icproject.exceptions.exceptions import DatabaseSectionNotFoundException


def config(filename='database.ini', section='postgresql') -> dict:
    parser = RawConfigParser()
    parser.read(filename)
    db_section = dict()
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_section[param[0]] = param[1]
    else:
        raise DatabaseSectionNotFoundException(section, filename)
    return db_section
