from selenium import webdriver as wd
from selenium.webdriver.common.by import By

PATH = "/usr/bin/chromedriver"

if __name__ == "__main__":
    driver = wd.Chrome(PATH)
    driver.get("https://academico.ifgoiano.edu.br/")
    driver.implicitly_wait(5)
    aluno_button = driver.find_elements(By.CLASS_NAME, "item_login_pagina_inicial")[1]
    aluno_button.click()
    login = driver.find_element(By.ID, "txtLogin")
    password = driver.find_element(By.ID, "txtSenha")
    btn_ok = driver.find_element(By.ID, "btnOk")
    login.send_keys(input("Login: "))
    password.send_keys(input("Password: "))
    btn_ok.click()
    calendario_academico_button = driver.find_elements(By.CLASS_NAME, "conteudoLink")[3]
    calendario_academico_button.click()
    if driver.save_screenshot("/home/leafar/documents/prg/code/py/webscraping/calendar.png"):
        print("Screenshot taken and saved")
    else:
        print("Could not take screenshot")
    driver.quit()
