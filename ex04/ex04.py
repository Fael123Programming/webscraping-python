from selenium import webdriver as wd
from selenium.webdriver.common.by import By

PATH = "/usr/bin/chromedriver"

if __name__ == "__main__":
    driver = wd.Chrome(PATH)
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(input("Search on Google: "))
    search_box.submit()
    driver.quit()
