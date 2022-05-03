from selenium import webdriver as wd
from selenium.webdriver.common.by import By

PATH = "/usr/bin/chromedriver"

if __name__ == "__main__":
    driver = wd.Chrome(PATH)
    driver.maximize_window()
    driver.get("https://academico.ifgoiano.edu.br/qacademico/alunos")
    user_login = driver.find_element(By.ID, "txtLogin")
    user_password = driver.find_element(By.ID, "txtSenha")
    button = driver.find_element(By.ID, "btnOk")
    user_login.send_keys("")
    user_password.send_keys("")
    button.click()
    driver.quit()

