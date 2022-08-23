from datetime import date


class InvalidDateException(Exception):

    def __init__(self, dt: date):
        super().__init__(f'Invalid date: {dt}')


class InvalidCheckinDateException(InvalidDateException):

    def __init__(self, dt: date):
        super().__init__(dt)


class InvalidCheckoutDateException(InvalidDateException):

    def __init__(self, dt: date):
        super().__init__(dt)


class InvalidQuantity(Exception):

    def __init__(self, quantity: int, traveller_type: str):
        super().__init__(f'Invalid quantity {quantity} of {traveller_type}.')


class InvalidAdultQuantity(InvalidQuantity):

    def __init__(self, quantity: int):
        super().__init__(quantity, 'adults')


class InvalidChildrenQuantity(InvalidQuantity):

    def __init__(self, quantity: int):
        super().__init__(quantity, 'children')


class InvalidRoomQuantity(InvalidQuantity):

    def __init__(self, quantity: int):
        super().__init__(quantity, 'rooms')


class InvalidPlaceException(Exception):

    def __init__(self):
        super().__init__('The place you are entering is not a valid place.')


class InvalidChildrenAges(Exception):

    def __init__(self):
        super().__init__(
            'Invalid children ages: it must be a `list` containing each child\'s age from 0 to 17 (integer values).')
