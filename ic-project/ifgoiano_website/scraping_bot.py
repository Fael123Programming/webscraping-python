from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.firefox import GeckoDriverManager
from post import Post
from date_converter import DateConverter
from post_category_setter import PostCategorySetter


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
        self._driver.implicitly_wait(0.5)
        featured_post_link = self._driver.find_element(By.CLASS_NAME, 'manchete-texto-lateral')
        featured_post_link.click()  # Click featured post.
        post = self._get_post()
        self._driver.quit()
        return post

    def fetch_all_posts(self) -> list:
        self._driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        self._driver.get(self._url)
        self._driver.implicitly_wait(5)
        post_list_btn = self._driver.find_element(By.CLASS_NAME, 'link')
        post_list_btn.click()
        post_list = WebDriverWait(self._driver, 20).until(ec.presence_of_element_located((By.CLASS_NAME, 'tile-list-1')))
        post_links = WebDriverWait(post_list, 20).until(ec.presence_of_all_elements_located((By.TAG_NAME, 'a')))
        links = list()
        for link in post_links:
            link_text = link.text
            if link_text.isspace() or len(link_text) == 0:
                continue
            links.append(link_text)
        posts = list()
        for i in range(len(links) - 1):  # The last post is rejected
            self._driver.find_element(By.LINK_TEXT, links[i]).click()
            posts.append(self._get_post())
            self._driver.back()
        self._driver.quit()
        return posts

    def _get_post(self) -> Post:
        post = Post()
        document_first_heading = self._driver.find_element(By.CLASS_NAME, 'documentFirstHeading')
        post_title = document_first_heading.text  # Get post title.
        document_publish_date = self._driver.find_element(By.CLASS_NAME, 'documentPublished')
        post_publish_date = document_publish_date.text  # Get post publish date text
        try:
            post_accesses = int(self._driver.find_element(By.CLASS_NAME, 'documentHits').text.split(' ')[1])
            # In some posts, there are no information about access measurement.
        except NoSuchElementException:
            post_accesses = 0
        post_description = self._driver.find_element(By.CLASS_NAME, 'description')
        post.title = post_title
        post.publication_date = DateConverter.convert(post_publish_date)
        post.accesses = post_accesses
        post.description = post_description.text.strip()
        PostCategorySetter.set(post)
        return post
