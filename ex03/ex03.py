from selenium import webdriver as wd
from selenium.webdriver.common.by import By

PATH = "/usr/bin/chromedriver"

if __name__ == "__main__":
    driver = wd.Chrome(PATH)
    driver.maximize_window()
    driver.get("https://www.google.com")
    driver.implicitly_wait(5)
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(input("Enter something to search on Google: "))
    search_button = driver.find_element(By.NAME, "btnK")
    search_button.click()
    driver.quit()

