from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.firefox import GeckoDriverManager
from post import Post
from date_converter import DateConverter
from post_category_setter import PostCategorySetter
from relevance_index_calculator import RelevanceIndexCalculator


class ScrapingBot:
    PATH_FIREFOX_DRIVER = '/usr/bin/geckodriver'

    def __init__(self):
        self._url = 'https://www.ifgoiano.edu.br/home/index.php'
        self._driver = None

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str):
        if url is None or url.isspace() or len(url) == 0:
            return
        self._url = url

    def fetch_featured_post(self) -> Post:
        self._driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        self._driver.get(self._url)
        self._driver.implicitly_wait(5)
        WebDriverWait(self._driver, 5).until(
            ec.presence_of_element_located((By.CLASS_NAME, 'manchete-texto-lateral'))
        ).click()
        post = self._get_post()
        print('Featured post:', post)
        self._driver.quit()
        return post

    def fetch_all_posts(self) -> list:
        self._driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        self._driver.execute_script(f"location.href='{self._url}'")
        # self._driver.get(self._url)
        self._driver.implicitly_wait(5)
        wait = WebDriverWait(self._driver, 5)
        wait.until(ec.element_to_be_clickable((By.CLASS_NAME, 'link'))).click()
        post_list = wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'tile-list-1')))
        post_links = WebDriverWait(post_list, 5).until(ec.presence_of_all_elements_located((By.TAG_NAME, 'a')))
        links = list()
        for link in post_links:
            link_text = link.text
            if link_text.isspace() or len(link_text) == 0:
                continue
            links.append(link_text)
        posts = list()
        for i in range(len(links) - 1):  # The last post is rejected
            if i == 5:
                break
            wait.until(ec.element_to_be_clickable((By.LINK_TEXT, links[i]))).click()
            post = self._get_post()
            print(f"({i + 1})", post)
            posts.append(post)
            self._driver.back()
        self._driver.quit()
        return posts

    def fetch_post(self, post_title: str):
        if post_title.isspace() or len(post_title) == 0:
            return
        self._driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        self._driver.execute_script(f"location.href='{self._url}'")
        # self._driver.get(self._url)
        self._driver.implicitly_wait(5)
        self._driver.find_element(By.CLASS_NAME, 'link').click()
        self._driver.find_element(By.LINK_TEXT, post_title).click()
        post = self._get_post()
        self._driver.quit()
        return post

    def _get_post(self) -> Post:
        post = Post()
        date_converter = DateConverter()
        post_category_setter = PostCategorySetter()
        relevance_index_calculator = RelevanceIndexCalculator()
        post_title = self._driver.find_element(By.CLASS_NAME, 'documentFirstHeading').text  # Get post title.
        try:
            post_publish_date = self._driver.find_element(By.CLASS_NAME, 'documentPublished').text
        except NoSuchElementException:
            post_publish_date = None
        try:
            document_hits = self._driver.find_element(By.CLASS_NAME, 'documentHits')
            post_accesses = int(document_hits.text.split(' ')[1])
        except NoSuchElementException:
            post_accesses = 0
        post_description = self._driver.find_element(By.CLASS_NAME, 'description').text.strip()
        post.title = post_title
        post.publication_date = None if post_publish_date is None else date_converter.convert(post_publish_date)
        post.accesses = post_accesses
        post.description = post_description
        post_category_setter.set_of(post)  # Setting post category.
        relevance_index_calculator.calculate_of(post)  # Calculate post relevance index.
        return post
