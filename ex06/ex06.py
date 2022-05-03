from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec

PATH = "/usr/bin/chromedriver"
if __name__ == "__main__":
    driver = wd.Chrome(PATH)
    driver.get("https://jqueryui.com/resources/demos/progressbar/download.html")
    driver.implicitly_wait(5)
    download_button = driver.find_element(By.ID, "downloadButton")
    download_button.click()
    wdw(driver, 30).until(
        ec.text_to_be_present_in_element((By.CLASS_NAME, "progress-label"), "Complete!")
    )
    progress_element = driver.find_element(By.CLASS_NAME, "progress-label")
    if progress_element.text == "Complete!":
        print("Downloaded successfully")
    else:
        print("Something went wrong")
    driver.quit()
