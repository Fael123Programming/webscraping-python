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
        self._consult_convenio()

    def _click_convenios_button(self):
        div_col1 = self.find_element(By.CLASS_NAME, "col1")
        div_convenios = div_col1.find_elements(By.TAG_NAME, "div")[3]
        div_convenios.click()
        li_to_click = self.find_element(By.TAG_NAME, "li")
        li_to_click.click()

    def _consult_convenio(self):
        convenios_number_list = []
        convenios_cnpj_list = []
        data_frame = pd.read_excel('solicitacoes.xlsx', index_col=0)
        convenios_to_search_for = data_frame.index.values
        for convenio_number in convenios_to_search_for:
            # convenio_number = input("Número do convênio (-1 para encerrar): ")
            # if convenio_number == "-1":
            #     break
            if self._convenio_number_not_found(str(convenio_number)):
                print(f"Convênio ({convenio_number}) não encontrado...")
            else:
                convenios_number_list.append(convenio_number)
                convenios_cnpj_list.append(self._get_cnpj())
                print(f"Convênio encontrado!")
            self._click_convenios_button()
        data = {'numero_convenio': convenios_number_list, 'cnpnj_proponente_convenio': convenios_cnpj_list}
        df = pd.DataFrame(data=data)
        df.to_excel("cnpj.xlsx", index=False)

    def _convenio_number_not_found(self, convenio_number) -> bool:
        if convenio_number.isspace():
            return True
        search_box = self.find_element(By.ID, "consultarNumeroConvenio")
        search_box.send_keys(convenio_number)
        consult_button = self.find_element(By.ID, "form_submit")
        consult_button.click()
        result_list = self.find_element(By.ID, "listaResultado")
        return result_list.text == "Nenhum registro foi encontrado."

    def _get_cnpj(self):
        result_list = self.find_element(By.ID, "listaResultado")
        result_list.find_elements(By.TAG_NAME, "a")[0].click()
        tr_proponent = self.find_element(By.CLASS_NAME, "proponente")
        return tr_proponent.find_elements(By.TAG_NAME, "td")[1].text.split(" ")[1]
