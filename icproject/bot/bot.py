from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager, ChromeType
from icproject.bot.date_converter import DateConverter
from icproject.bot.post import Post
from icproject.bot.post_category_setter import PostCategorySetter
from icproject.bot.relevance_index_calculator import RelevanceIndexCalculator
import pandas as pd
from time import sleep


def change_spaces_by_plus_sign(url: str) -> str:
    return url.replace(' ', '+')


class Bot(webdriver.Chrome):

    def __init__(self):
        options = webdriver.ChromeOptions()
        prefs = {
            'profile.managed_default_content_settings.images': 2,  # Disable images for being loaded.
            'intl.accept_languages': 'en-GB'  # Set browser default language to English.
        }
        options.add_experimental_option('prefs', prefs)
        # Avoid bot detection by servers.
        # options.add_argument('--disable-blink-features=AutomationControlled')
        # options = Options()
        # options.set_preference('intl.accept_languages', 'en-GB')
        # options.set_preference('profile.managed_default_content_settings.images', 2)
        super().__init__(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
                         options=options)

    def print_title_and_description_maximum_sizes(self):
        titles = list()
        descriptions = list()
        self.get('https://ifgoiano.edu.br/home/index.php')
        featured_post = self.find_element(By.CLASS_NAME, 'manchete-texto-lateral')
        titles.append(len(featured_post.find_element(By.TAG_NAME, 'h1').text.strip()))
        descriptions.append(len(featured_post.find_element(By.CLASS_NAME, 'description').text.strip()))
        print(titles)
        print(descriptions)
        self.quit()

    def export_post_urls_to_csv(self):
        """
            Accesses `www.ifgoiano.edu.br`, fetches all post urls and place them into a .csv file.
        """
        urls = list()
        self.get('https://ifgoiano.edu.br/home/index.php')
        featured_post_box = self.find_element(By.CLASS_NAME, 'manchete-texto-lateral')
        urls.append([featured_post_box.find_element(By.TAG_NAME, 'a').get_attribute('href')])  # Featured post url.
        three_secondary_posts_box = self.find_element(By.CLASS_NAME, 'chamadas-secundarias')
        three_secondary_posts_urls = three_secondary_posts_box.find_elements(By.TAG_NAME, 'a')
        for i in range(0, len(three_secondary_posts_urls), 2):
            urls.append([three_secondary_posts_urls[i].get_attribute('href')])
        self.get('https://www.ifgoiano.edu.br/home/index.php/component/content/category/160-noticias-anteriores.html')
        post_boxes = self.find_elements(By.CLASS_NAME, 'tileItem')
        for post_box in post_boxes:
            post_title = post_box.find_element(By.CLASS_NAME, 'tileHeadline')
            post_url = post_title.find_element(By.TAG_NAME, 'a').get_attribute('href')
            urls.append([post_url])
        data_frame = pd.DataFrame(urls, columns=['post_url'])
        data_frame.to_csv('post_urls.csv', index=False)
        print(f'----- Post urls exported to file \'post_urls.csv\'')
        self.quit()

    def get_posts_data(self) -> list:
        """
            Accesses each post url of `www.ifgoiano.edu.br` based on the file created by
            the method `export_post_urls_to_csv()`, cast each post's data
            into a `Post` object grouping them in a list.
        :return: A list containing all post objects.
        """
        posts = list()
        urls = self._load_urls()
        i = 1
        for url in urls:
            self.get(url)
            sleep(1)
            post = self._get_post_data()
            print(f'{i} - {post}')
            posts.append(post)
            i += 1
        return posts

    @staticmethod
    def _load_urls() -> list:
        data_frame = pd.read_csv('post_urls.csv')
        urls = list()
        for row in data_frame.values:
            urls.append(row[0])
        return urls[0:len(urls) - 1]  # The last url isn't of a valuable post.

    def _get_post_data(self) -> Post:
        post = Post(1, '', None, None, None, None)
        seconds = 15  # Seconds to the WebDriverWait hold on.
        date_converter = DateConverter()
        post_category_setter = PostCategorySetter()
        relevance_index_calculator = RelevanceIndexCalculator()
        content_panel = self.find_element(By.ID, 'content')
        post_title = WebDriverWait(content_panel, seconds).until(
            ec.presence_of_element_located((By.TAG_NAME, 'h1'))).text. \
            strip()
        post.title = post_title
        try:
            post_publication_timestamp = date_converter.convert(WebDriverWait(content_panel, seconds).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'documentPublished'))
            ).text.strip())
        except (NoSuchElementException, TimeoutException):
            post_publication_timestamp = None
        post.publication_timestamp = post_publication_timestamp
        try:
            post_accesses = int(WebDriverWait(content_panel, seconds).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'documentHits'))
            ).text.strip().split(' ')[1])
        except (NoSuchElementException, TimeoutException):
            post_accesses = None  # Post does not have access count.
        post.accesses = post_accesses
        try:
            post_description = WebDriverWait(self, seconds).until(ec.presence_of_element_located(
                (By.CLASS_NAME, 'description'))
            ).text.strip()
        except (NoSuchElementException, TimeoutException):
            try:
                post_description = WebDriverWait(self, seconds).until(ec.presence_of_element_located(
                    (By.CLASS_NAME, 'subtitle'))).text.strip()
            except (NoSuchElementException, TimeoutException):
                post_description = None  # Post does not have description.
        post.description = post_description
        post_category_setter.set_of(post)  # Setting post category.
        relevance_index_calculator.calculate_of(post)  # Calculate post relevance index.
        return post
