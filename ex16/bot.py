from selenium import webdriver
from datetime import datetime

from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from time import sleep
from ex16 import constants


class Bot(webdriver.Chrome):

    def __init__(self):
        self._start_datetime = datetime.now()
        print('Bot started on', self._start_datetime)
        options = webdriver.ChromeOptions()
        prefs = {
            'profile.managed_default_content_settings.images': 2,
            'intl.accept_languages': 'en-GB'
        }
        options.add_experimental_option('prefs', prefs)
        super().__init__(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
                         options=options)
        self.implicitly_wait(5)

    def click_button_on_mais_brasil_platform_main_menu(self, text: str):
        """
        Accesses `https://voluntarias.plataformamaisbrasil.gov.br/voluntarias/Principal/Principal.do?Usr=guest&Pwd=guest`
        and clicks the button labeled as `text` inside the main menu
        """
        self.get(constants.PLATAFORMA_MAIS_BRASIL)
        main_menu = self.find_element(By.ID, 'menuPrincipal')
        for menu_options in main_menu.find_elements(By.TAG_NAME, 'div'):  # Go through all main menu options.
            if menu_options.text == text:  # Check whether the text of the menu option is equal to `text`.
                menu_options.click()
                sleep(5)
                return
        print(f'{text} wasn\'t found as a menu option')

    def click_submenu_option(self, text: str):
        """
        After a main menu button has been clicked, this method is responsible for clicking on a sub-option
        of the main menu option chosen. `Text` is the name of the sub-option to be clicked on.
        """
        content_menu = self.find_element(By.ID, 'contentMenu')
        for link in content_menu.find_elements(By.TAG_NAME, 'li'):  # Go through all sub-menu options.
            if link.text == text:  # Check whether the text of the sub-menu option is equal to `text`
                link.click()
                sleep(5)
                return
        print(f'{text} wasn\'t found as a link option')

    def consult_convenio(self, convenio_number: str):
        """
        Consults a convenio by its number.
        :param convenio_number:
        :return:
        """
        convenio_number_input = self.find_element(By.ID, 'consultarNumeroConvenio')
        convenio_number_input.send_keys(convenio_number)  # Entering convenio number to be searched for.
        convenio_number_input.send_keys(Keys.ENTER)
        convenio_table = self.find_element(By.ID, 'row')
        convenio_table_first_link = convenio_table.find_elements(By.TAG_NAME, 'a')[0]
        convenio_table_first_link.click()  # Click the first row of on the result table.
        sleep(5)

    def click_convenio_tab_and_subtab(self, tab_name: str, tab_option: str):
        """
        This method may be used to navigate between tabs and sub-tabs once you've
        reached a convenio page.
        :param: tab_name the tab to be clicked on.
        :param: tab_option the sub-tab to be clicked on
        """
        tab_group = self.find_element(By.ID, 'grupo_abas')
        links = tab_group.find_elements(By.TAG_NAME, 'a')
        links[0].find_element(By.TAG_NAME, 'div').click()  # Click to prevent misuse.
        for link in links:  # Search for the tab name that's equal to `tab_name` and click on it if it's found.
            if link.text == tab_name:
                link.find_element(By.TAG_NAME, 'div').click()
                sleep(5)
                break
        subgroup_tabs = self.find_element(By.ID, 'sub_grupo_abas')
        sublinks = subgroup_tabs.find_elements(By.TAG_NAME, 'a')
        for sublink in sublinks:
            # Search for the sub-tab name that's equal to `tab_option` and click on it if it's found.
            if sublink.text == tab_option:
                sublink.find_element(By.TAG_NAME, 'div').click()
                sleep(5)
                return

    def __exit__(self, exc_type, exc_val, exc_tb):
        now = datetime.now()
        print('Bot execution finished on', now)
        print('Time spent:', now - self._start_datetime)
        self.quit()
