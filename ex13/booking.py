from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager, ChromeType
from datetime import datetime
from ex13.constants import *
from ex13.exceptions import *
from ex13.currency import Currency


def switch_blanks_by_plus(string: str) -> str:
    return string.replace(' ', '+')


class BookingBot(webdriver.Chrome):

    def __init__(self):
        self._execution_start = datetime.now()
        print('Bot started at', self._execution_start)
        options = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images': 2, 'intl.accept_languages': 'en-GB'}
        options.add_experimental_option('prefs', prefs)
        super().__init__(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
        self.maximize_window()
        self.implicitly_wait(15)
        self.get(BASE_URL)

    def search_for(self, place: str, checkin_date: date, checkout_date: date, currency: Currency, adults: int,
                   rooms: int):
        now = datetime.now().date()
        if checkin_date <= now:
            raise InvalidCheckinDateException(checkin_date)
        if checkout_date <= checkin_date:
            raise InvalidCheckoutDateException(checkout_date)
        if adults <= 0:
            raise InvalidAdultQuantity(adults)
        if rooms <= 0:
            raise InvalidRoomQuantity(rooms)
        self._set_currency(currency)
        self._enter_place(place)
        self._enter_checkin_date(checkin_date)
        self._enter_checkout_date(checkout_date)
        self._set_adults(adults)
        self._set_rooms(rooms)

    def add_child(self, age: int):
        pass

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

    def _set_currency(self, currency: Currency):
        currencies_button = self.find_element(By.CSS_SELECTOR, 'button[data-modal-aria-label="Select your currency"]')
        currencies_button.click()
        currency_element = self.find_element(By.CSS_SELECTOR, 'a[data-modal-header-async-url-param='
                                                              f'"changed_currency=1&selected_currency={currency.value}"')
        currency_element.click()

    def _enter_place(self, place: str):
        if place.isspace() or len(place) == 0 or not place.replace(' ', '').isalpha():
            raise InvalidPlaceException()
        search_box = self.find_element(By.ID, 'ss')
        search_box.send_keys(place)
        # Click on the first suggestion.
        suggestion_box = self.find_element(By.CSS_SELECTOR, 'ul[role="listbox"]')
        suggestion_box.find_elements(By.TAG_NAME, 'li')[0].click()

    def _enter_checkin_date(self, checkin_date: date):
        checkin_date_input = self.find_element(By.CSS_SELECTOR, f'td[data-date="{checkin_date.__str__()}"]')
        checkin_date_input.click()

    def _enter_checkout_date(self, checkout_date: date):
        checkout_date_input = self.find_element(By.CSS_SELECTOR, f'td[data-date="{checkout_date.__str__()}"]')
        checkout_date_input.click()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()
        print('Bot execution finished with', datetime.now() - self._execution_start)
