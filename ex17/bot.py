from selenium import webdriver
from datetime import datetime

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep


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

    def access_video_repeatedly(self, video_url: str):
        self.get(video_url)
        while True:
            left_controls_box = self.find_element(By.CLASS_NAME, 'ytp-left-controls')
            try:
                btn_play = WebDriverWait(left_controls_box, 30).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, 'button[title="Play (k)"]'))
                )
            except TimeoutException:
                pass
            else:
                btn_play.click()
                sleep(10)
            self.get(video_url)
