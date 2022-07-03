from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from post import Post
from date_converter import DateConverter
from post_category_setter import PostCategorySetter


class ScrapingBot:
    PATH_FIREFOX_DRIVER = '/usr/bin/geckodriver'

    def __init__(self):
        self._url = 'https://www.ifgoiano.edu.br/home/index.php'

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str):
        if url is None or url.isspace() or len(url) == 0:
            return
        self._url = url

    def fetch_featured_post(self) -> Post:
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        driver.get(self._url)
        driver.implicitly_wait(0.5)
        post = Post()
        featured_post_link = driver.find_element(By.CLASS_NAME, 'manchete-texto-lateral')
        featured_post_link.click()  # Click featured post.
        document_first_heading = driver.find_element(By.CLASS_NAME, 'documentFirstHeading')
        post_title = document_first_heading.text  # Get post title.
        document_publish_date = driver.find_element(By.CLASS_NAME, 'documentPublished')
        post_publish_date = document_publish_date.text  # Get post publish date text
        post_accesses = driver.find_element(By.CLASS_NAME, 'documentHits')
        post_accesses = int(post_accesses.text.split(' ')[1])
        post_description = driver.find_element(By.CLASS_NAME, 'description')
        post.title = post_title
        post.publication_date = DateConverter.convert(post_publish_date)
        post.accesses = post_accesses
        post.description = post_description.text.strip()
        PostCategorySetter.set(post)
        driver.quit()
        return post

    def fetch_all_posts(self) -> list:
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        driver.get(self._url)
        driver.implicitly_wait(0.5)
        post_list_btn = driver.find_element(By.CLASS_NAME, 'link')
        post_list_btn.click()
        driver.implicitly_wait(5)
        admin_form = driver.find_element(By.ID, 'adminForm')
        post_list = admin_form.find_element(By.CLASS_NAME, 'tile-list-1')
        post_links = post_list.find_elements(By.TAG_NAME, 'a')
        posts = list()
        for i in range(len(post_links) - 1):  # The last post is rejected
            post_links[i].click()
            driver.implicitly_wait(5)
            # get post info
            # create post object
            # posts.append(post)
            driver.back()
            driver.implicitly_wait(5)
            admin_form = driver.find_element(By.ID, 'adminForm')
            post_list = admin_form.find_element(By.CLASS_NAME, 'tile-list-1')
            post_links = post_list.find_elements(By.TAG_NAME, 'a')
        return posts
