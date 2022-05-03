from selenium import webdriver as wd

PATH = "/usr/bin/chromedriver"  # The driver for the specific browser we are going to use

if __name__ == "__main__":
    driver = wd.Chrome(PATH)
    driver.maximize_window()
    driver.get("https://www.nasa.gov")
    print("Title of the web application:", driver.title)
    print("URL:", driver.current_url)
