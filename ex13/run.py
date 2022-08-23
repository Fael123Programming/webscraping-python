from ex13.booking import BookingBot
from datetime import date
from ex13.currency import Currency


if __name__ == '__main__':
    with BookingBot() as bot:
        bot.search_for(
            place='Rio de Janeiro',
            checkin_date=date(2022, 9, 20),
            checkout_date=date(2022, 9, 23),
            currency=Currency.US_DOLLAR,
            adults=2,
            rooms=2,
            children=3,
            children_ages=[10, 12, 8]
        )
        bot.export_to_csv()
        bot.print_data()

