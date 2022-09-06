from time import sleep
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager, ChromeType
from datetime import datetime


class Bot(webdriver.Chrome):

    def __init__(self):
        print('Bot started as of', datetime.now())
        options = webdriver.ChromeOptions()
        prefs = {
            'profile.managed_default_content_settings.images': 2,
            'intl.accept_languages': 'en-GB'
        }
        options.add_experimental_option('prefs', prefs)
        super().__init__(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
                         options=options)
        self.implicitly_wait(5)

    def go(self):
        self._access_site()
        self._search_process('92.000114/2020-20')
        self._upload_file('/home/leafar/Anexo-rafael.pdf')

    def _access_site(self):
        self.get('https://sipseiteste.fiocruz.br/login.php?sigla_orgao_sistema=FIOCRUZ&sigla_sistema=SEI')
        self.maximize_window()
        user_login = self.find_element(By.ID, 'txtUsuario')
        user_login.clear()
        user_login.send_keys('teste')
        password = self.find_element(By.ID, 'pwdSenha')
        password.clear()
        password.send_keys('teste')
        login_btn = self.find_element(By.ID, 'sbmLogin')
        login_btn.click()
        sleep(3)

    def _search_process(self, process_code: str):
        search_box = self.find_element(By.ID, 'txtPesquisaRapida')
        search_box.clear()
        search_box.send_keys(process_code)
        search_box.send_keys(Keys.ENTER)
        sleep(3)

    def _upload_file(self, file_path: str):
        iframe = self.find_element(By.ID, 'ifrVisualizacao')
        self.switch_to.frame(iframe)
        action_menu = self.find_element(By.ID, 'divArvoreAcoes')
        include_document_anchor = action_menu.find_elements(By.TAG_NAME, 'a')[0]
        include_document_anchor.click()
        document_source = self.find_element(By.LINK_TEXT, 'Externo')
        document_source.click()
        document_type = self.find_element(By.ID, 'selSerie')
        document_type.send_keys('Anexo')
        creation_date = self.find_element(By.ID, 'txtDataElaboracao')
        creation_date.send_keys('26/05/2022')
        nato_digital_radio = self.find_element(By.ID, 'optNato')
        nato_digital_radio.click()
        public_access_radio = self.find_element(By.ID, 'optPublico')
        public_access_radio.click()
        file_input = self.find_element(By.ID, 'filArquivo')
        file_input.send_keys(file_path)
        save_btn = self.find_element(By.ID, 'btnSalvar')
        save_btn.submit()
        sleep(5)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Bot ended as of', datetime.now())
        self.quit()

