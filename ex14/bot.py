from selenium import webdriver
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager, ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from datetime import datetime


class Bot(webdriver.Chrome):

    def __init__(self):
        print('Bot started at', datetime.now())
        options = webdriver.ChromeOptions()
        prefs = {
            'profile.managed_default_content_settings.images': 2,  # Disable images for being loaded.
            'intl.accept_languages': 'en-GB'  # Set browser default language to English.
        }
        options.add_experimental_option('prefs', prefs)
        super().__init__(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
                         options=options)
        self.implicitly_wait(5)

    def open_multiple_tabs(self):
        self.maximize_window()
        self.get('https://www.google.com')
        self.execute_script('window.open();')
        self.switch_to.window(self.window_handles[1])
        self.get("https://www.youtube.com")
        self.execute_script('window.open("https://www.refactoring.guru", "new tab");')
        self.switch_to.window(self.window_handles[2])
        sleep(3)
        self.switch_to.window(self.window_handles[1])
        sleep(3)
        self.switch_to.window(self.window_handles[0])
        sleep(3)

    def access_frame(self):
        username = 'Guido van Rossum'
        email = 'guido.rossum@python.org'
        password = 'IcreaTedPython91'
        self.get("https://jqueryui.com/dialog/#modal-form")
        content = self.find_element(By.ID, 'content')
        iframe = content.find_element(By.TAG_NAME, 'iframe')
        self.switch_to.frame(iframe)
        create_account_btn = self.find_element(By.ID, 'create-user')
        create_account_btn.click()
        name_input = self.find_element(By.ID, 'name')
        name_input.clear()
        name_input.send_keys(username)
        email_input = self.find_element(By.ID, 'email')
        email_input.clear()
        email_input.send_keys(email)
        password_input = self.find_element(By.ID, 'password')
        password_input.clear()
        password_input.send_keys(password)
        button_div = self.find_element(By.CSS_SELECTOR, 'div[class="ui-dialog-buttonset"]')
        create_btn = button_div.find_element(By.TAG_NAME, 'button')
        create_btn.click()
        self.execute_script(f"alert('Account created, {username}!')")
        sleep(5)

    def use_javascript(self):
        self.get('https://www.google.com')
        self.execute_script('alert("Switch to YouTube...")')
        WebDriverWait(self, 5).until(
            ec.alert_is_present()
        )
        self.switch_to.alert.accept()
        self.get('https://www.youtube.com')
        sleep(3)

    def roll_page(self):
        self.get('https://en.wikipedia.org')
        self.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(3)

    def drag_and_drop(self):
        self.get('https://jqueryui.com/droppable/')
        self.maximize_window()
        content = self.find_element(By.ID, 'content')
        iframe = content.find_element(By.TAG_NAME, 'iframe')
        self.switch_to.frame(iframe)
        draggable = self.find_element(By.ID, 'draggable')
        droppable = self.find_element(By.ID, 'droppable')
        action = ActionChains(self)
        # action.drag_and_drop(draggable, droppable).perform()
        # action.click_and_hold(draggable).pause(3).move_to_element(droppable).release(droppable).perform()
        action.drag_and_drop_by_offset(draggable, 160, 30).perform()
        sleep(3)

    def upload_file(self):
        file_path = '/home/leafar/time_consuming.c'
        self.get('https://the-internet.herokuapp.com/upload')
        file_input = self.find_element(By.ID, 'file-upload')
        file_input.send_keys(file_path)
        file_submit_btn = self.find_element(By.ID, 'file-submit')
        file_submit_btn.click()
        sleep(3)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()
        print('Bot finished at', datetime.now())
