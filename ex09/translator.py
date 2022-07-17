from os import environ
from selenium import webdriver
from selenium.webdriver.common.by import By
from language import Language


class Translator:

    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(Translator, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def translate(src_lang: Language, target_lan: Language, text: str) -> str:
        url = f'https://translate.google.com/?sl={src_lang.value}&tl={target_lan.value}&text={text}&op=translate'
        environ['PATH'] += r'/usr/bin/geckodriver'
        driver = webdriver.Firefox()
        driver.get(url)
        driver.implicitly_wait(5)
        result = driver.find_element(By.CLASS_NAME, 'J0lOec').text
        driver.close()
        return result
