import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


if __name__ == '__main__':
    os.environ['PATH'] += r'/usr/bin/chromedriver'  # 'r' is used to treat it as a raw string.
    driver = webdriver.Chrome()
    driver.get('https://www.seleniumeasy.com/test/jquery-download-progress-bar-demo.html')
    driver.implicitly_wait(5)  # Timeout of 5 secs.
    driver.find_element(By.ID, 'downloadButton').click()
    print('Waiting progress bar...')
    WebDriverWait(driver, 30).until(
        ec.text_to_be_present_in_element(
            (By.CLASS_NAME, 'progress-label'),
            'Complete!'
        )
    )
    print('Finished!')
    driver.close()
