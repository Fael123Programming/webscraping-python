class DatabaseSectionNotFoundException(Exception):

    def __init__(self, section: str, filename: str):
        super().__init__(f'Section {section} not found in file {filename}')


class InvalidArgumentException(Exception):

    def __init__(self, value):
        super().__init__(f'Invalid argument: {value}')
