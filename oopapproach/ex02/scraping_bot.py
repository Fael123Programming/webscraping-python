from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


class ScrapingBot(wd.Chrome):
    def __init__(self):
        options = wd.ChromeOptions().add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service(ChromeDriverManager().install())
        super(ScrapingBot, self).__init__(options=options, service=service)
        self.get(
            "https://voluntarias.plataformamaisbrasil.gov.br/voluntarias/Principal/Principal.do?Usr=guest&Pwd=guest")
        self.implicitly_wait(5)

    def go(self):
        self._click_convenios_button()
        self._enter_search_information()
        self.search()

    def _click_convenios_button(self):
        div_col1 = self.find_element(By.CLASS_NAME, "col1")
        div_convenios = div_col1.find_elements(By.TAG_NAME, "div")[3]
        div_convenios.click()
        li_to_click = self.find_element(By.TAG_NAME, "li")
        li_to_click.click()

    def _enter_search_information(self):
        select_estado = self.find_element(By.ID, "consultarUf")
        select_estado.click()
        option_go = select_estado.find_elements(By.TAG_NAME, "option")[9]
        option_go.click()
        select_municipio = self.find_element(By.ID, "consultarMunicipioProponente")
        select_municipio.click()
        option_morrinhos = select_municipio.find_elements(By.TAG_NAME, "option")[151]
        option_morrinhos.click()
        tr_convenio = self.find_element(By.ID, "tr-consultarSituacaoConvenio")
        radio_aprovado_plano_de_trabalho = tr_convenio.find_elements(By.TAG_NAME, "input")[0]
        radio_aprovado_plano_de_trabalho.click()

    def search(self):
        from time import sleep
        self.find_elements(By.ID, "form_submit")[0].click()
        sleep(5)