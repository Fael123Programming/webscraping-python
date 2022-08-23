from ex13.booking import BookingBot
from datetime import date
from ex13.currency import Currency


if __name__ == '__main__':
    with BookingBot() as bot:
        bot.search_for('Madrid, Spain', date(2022, 9, 20), date(2022, 9, 23), Currency.US_DOLLAR, 1, 2)
        bot.add_child()

