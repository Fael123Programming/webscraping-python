from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager, ChromeType
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from ex13.constants import *
from ex13.exceptions import *
from ex13.currency import Currency
from time import sleep
from pandas import DataFrame
from prettytable import PrettyTable


class BookingBot(webdriver.Chrome):

    def __init__(self):
        self._execution_start = datetime.now()
        print('Bot started at', self._execution_start)
        options = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images': 2, 'intl.accept_languages': 'en-GB'}
        options.add_experimental_option('prefs', prefs)
        super().__init__(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
        self._fetched_data = list()
        self._columns = ['Title', 'Rating', 'Address', 'Period (nights)', 'Price', 'Taxes and Charges']
        self.maximize_window()
        self.implicitly_wait(15)
        self.get(BASE_URL)

    def search_for(self, *, place: str, checkin_date: date, checkout_date: date, currency: Currency, adults: int,
                   rooms: int, children=0, children_ages=None):
        now = datetime.now().date()
        if checkin_date <= now:
            raise InvalidCheckinDateException(checkin_date)
        if checkout_date <= checkin_date:
            raise InvalidCheckoutDateException(checkout_date)
        if adults <= 0:
            raise InvalidAdultQuantity(adults)
        if rooms <= 0:
            raise InvalidRoomQuantity(rooms)
        if children < 0:
            raise InvalidChildrenQuantity(children)
        if children > 0:
            # Do some checking.
            if not isinstance(children_ages, list) or len(children_ages) < children:
                raise InvalidChildrenAges()
            for child_age in children_ages:
                if not isinstance(child_age, int) or child_age < 0 or child_age > 17:
                    raise InvalidChildrenAges()
        self._set_currency(currency)
        self._enter_place(place)
        self._enter_checkin_date(checkin_date)
        self._enter_checkout_date(checkout_date)
        self._set_adults(adults)
        if children > 0:
            self._set_children(children, children_ages)
        self._set_rooms(rooms)
        self._search()
        self._fetched_data = self._fetch_results()
        print('----- Data fetched')

    def export_to_csv(self, filename='booking_data.csv'):
        if len(self._fetched_data) == 0:
            print('-- There is no data fetched. Try using search_for() method.')
        data_frame = DataFrame(self._fetched_data, columns=self._columns)
        data_frame.to_csv(filename, index=False)
        print(f"----- Exported to '{filename}'")

    def print_data(self):
        table = PrettyTable(self._columns)
        table.add_rows(self._fetched_data)
        print(table)

    def _search(self):
        self.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    def _fetch_results(self) -> list:
        # Fetches the title, rating, address, period (nights), price, taxes and charges.
        result_cards = self.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')
        processed_result_cards = list()
        for result_card in result_cards:
            processed_result_cards.append(self._extract_data_from_result_card(result_card))
        return processed_result_cards

    @staticmethod
    def _extract_data_from_result_card(result_card: WebElement) -> list:
        # title, rating, address, period(nights), price, taxes and charges.
        extracted_data = list()
        # Title.
        extracted_data.append(result_card.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').text.strip())
        # Review score.
        try:
            review_score = result_card.find_element(By.CSS_SELECTOR,
                                                    'div[data-testid="review-score"]').text.strip().replace('\n', ' - ')
        except NoSuchElementException:
            review_score = 'unknown'
        extracted_data.append(review_score)
        # Address.
        extracted_data.append(result_card.find_element(By.CSS_SELECTOR, 'span[data-testid="address"]').text.strip())
        # Period (nights).
        extracted_data.append(result_card.find_element(By.CSS_SELECTOR, 'div[data-testid="price-for-x-nights"]').text
                              .strip().split(' ')[0])
        # Price
        price_box = result_card.find_element(By.CSS_SELECTOR, 'div[data-testid="price-and-discounted-price"]')
        price_box_spans = price_box.find_elements(By.TAG_NAME, 'span')
        # The pricing may come having the former price and the new one (with some discount).
        # As we want only the actual price, we should get the price given by the last span inside price_box.
        price = price_box_spans[len(price_box_spans) - 1]  # Get the last span.
        extracted_data.append(price.text.strip())
        # Taxes and charges.
        extracted_data.append(result_card.find_element(By.CSS_SELECTOR, 'div[data-testid="taxes-and-charges"]')
                              .text.strip())
        return extracted_data

    def _click_dropdown_element(self):
        self.find_element(By.CSS_SELECTOR, 'div[data-component="search/group/group-with-modal"]').click()

    def _click_body(self):
        self.find_element(By.ID, 'b2indexPage').click()

    def _set_adults(self, quantity: int):
        if quantity <= 0:
            raise InvalidAdultQuantity(quantity)

        def get_adult_quantity() -> int:
            return int(self.find_elements(By.CSS_SELECTOR, 'span.bui-stepper__display')[0].text)

        self._click_dropdown_element()
        decrease_button = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Decrease number of Adults"]')
        increase_button = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Increase number of Adults"]')
        while get_adult_quantity() < quantity:
            increase_button.click()
        else:
            while get_adult_quantity() > quantity:
                decrease_button.click()
        self._click_body()

    def _set_rooms(self, rooms: int):
        if rooms <= 0:
            raise InvalidRoomQuantity(rooms)

        def get_room_quantity() -> int:
            return int(self.find_elements(By.CSS_SELECTOR, 'span.bui-stepper__display')[2].text)

        self._click_dropdown_element()
        decrease_button = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Decrease number of Rooms"]')
        increase_button = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Increase number of Rooms"]')
        while get_room_quantity() < rooms:
            increase_button.click()
        else:
            while get_room_quantity() > rooms:
                decrease_button.click()
        self._click_body()

    def _set_children(self, children: int, children_ages: list):
        def get_children_quantity() -> int:
            number = self.find_elements(By.CSS_SELECTOR, 'span.bui-stepper__display')[1].text
            return 0 if number == '' else int(number)

        self._click_dropdown_element()
        decrease_button = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Decrease number of Children"]')
        increase_button = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Increase number of Children"]')
        while get_children_quantity() < children:
            increase_button.click()
        else:
            while get_children_quantity() > children:
                decrease_button.click()
        children_age_select_elements = self.find_elements(By.NAME, 'age')
        i = 0
        for select_element in children_age_select_elements:
            select_element.click()
            select_element.find_element(By.CSS_SELECTOR, f'option[value="{children_ages[i]}"]').click()
            i += 1
        self._click_body()

    def _set_currency(self, currency: Currency):
        currencies_button = self.find_element(By.CSS_SELECTOR, 'button[data-modal-aria-label="Select your currency"]')
        currencies_button.click()
        currency_element = self.find_element(By.CSS_SELECTOR, 'a[data-modal-header-async-url-param='
                                                              f'"changed_currency=1&selected_currency={currency.value}"')
        currency_element.click()

    def _enter_place(self, place: str):
        if place.isspace() or len(place) == 0:
            raise InvalidPlaceException()
        search_box = self.find_element(By.ID, 'ss')
        search_box.send_keys(place)
        # Click on the first suggestion.
        sleep(1)
        suggestion_box = self.find_element(By.CSS_SELECTOR, 'ul[role="listbox"]')
        suggestion_box.find_elements(By.TAG_NAME, 'li')[0].click()

    def _enter_checkin_date(self, checkin_date: date):
        checkin_date_input = self.find_element(By.CSS_SELECTOR, f'td[data-date="{checkin_date.__str__()}"]')
        checkin_date_input.click()

    def _enter_checkout_date(self, checkout_date: date):
        checkout_date_input = self.find_element(By.CSS_SELECTOR, f'td[data-date="{checkout_date.__str__()}"]')
        checkout_date_input.click()

    @property
    def fetched_data(self) -> list:
        return self._fetched_data

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()
        print('Bot execution finished with', datetime.now() - self._execution_start)
