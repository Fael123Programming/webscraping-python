from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas


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
        self._search()
        data = self._get_data()
        df = pandas.DataFrame(data=data)
        df.to_excel("aprovados.xlsx")
        print('-'*100)
        print(f"{'linha':<10}{'numero convenio':<20}{'data fim execucao'}")
        row = 1
        for numero, data in zip(data['numeros_convenios'], data['datas_fim_execucao']):
            print(f"{row:<10}{numero:<20}{data}")
            row += 1
        print('-'*100)

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

    def _search(self):
        self.find_elements(By.ID, "form_submit")[4].click()

    def _get_data(self) -> dict:
        numeros_convenios = []
        datas_fim_execucao = []
        current_dataset = 1
        while True:
            numeros_convenios.extend(self._get_numeros_convenios())
            datas_fim_execucao.extend(self._get_datas_fim_execucao())
            if self._there_are_not_any_more_datasets(current_dataset):
                break
            self._click_next_dataset(current_dataset)
            current_dataset += 1
        return dict(numeros_convenios=numeros_convenios, datas_fim_execucao=datas_fim_execucao)

    def _get_numeros_convenios(self) -> list:
        return [web_element.text for web_element in self.find_elements(By.CLASS_NAME, "numeroConvenio")[1:]]

    def _get_datas_fim_execucao(self) -> list:
        return [web_element.text for web_element in self.find_elements(By.CLASS_NAME, "dataFimExecucao")[1:]]

    def _click_next_dataset(self, current_dataset: int):
        page_links_span = self.find_elements(By.CLASS_NAME, "pagelinks")[1]
        next_link = page_links_span.find_elements(By.TAG_NAME, "a")[current_dataset - 1]
        next_link.click()

    def _there_are_not_any_more_datasets(self, current_dataset: int) -> bool:
        page_links_span = self.find_elements(By.CLASS_NAME, "pagelinks")[1]
        dataset_links = page_links_span.find_elements(By.TAG_NAME, "a")
        number_last_link = int(dataset_links[len(dataset_links) - 1].text)
        return current_dataset == number_last_link + 1
