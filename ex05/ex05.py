from selenium import webdriver as wd
from selenium.webdriver.common.by import By

PATH = "/usr/bin/chromedriver"

if __name__ == "__main__":
    driver = wd.Chrome(PATH)
    driver.get("https://academico.ifgoiano.edu.br/qacademico/alunos")
    print("----- Q-Academico IF Goiano -----")
    login = input("Login: ")
    password = input("Password: ")
    login_element = driver.find_element(By.ID, "txtLogin")
    password_element = driver.find_element(By.ID, "txtSenha")
    btn_submit = driver.find_element(By.ID, "btnOk")
    login_element.send_keys(login)
    password_element.send_keys(password)
    btn_submit.click()
