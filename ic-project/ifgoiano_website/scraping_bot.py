from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from post import Post
from datetime import date


def transform_to_date(date_string: str):  # yyyy-mm-dd
    return date_string


class ScrapingBot:
    ROOT_URL = 'https://www.ifgoiano.edu.br/home/index.php'
    PATH_CHROME_DRIVER = '/usr/bin/chromedriver'
    PATH_FIREFOX_DRIVER = '/usr/bin/geckodriver'

    def __init__(self):
        self._driver = wd.Firefox(ScrapingBot.PATH_FIREFOX_DRIVER)  # Not working yet. Fix it!
        self._driver.get(ScrapingBot.ROOT_URL)  # Initializing at the root of the website.
        self._driver.implicitly_wait(5)

    def fetch_featured_post(self):
        featured_post_link = self._driver.find_element(By.CLASS_NAME, 'manchete-texto-lateral')
        featured_post_link.click()
        div_content = self._driver.find_element(By.ID, 'content')
        section_content_section = div_content.find_element(By.ID, 'content-section')
        row_fluid_div = section_content_section.find_element(By.CLASS_NAME, 'row-fluid')
        div_item_page = row_fluid_div.find_element(By.CLASS_NAME, 'item-page')
        span_document_category = div_item_page.find_element(By.CLASS_NAME, 'documentCategory')
        h1_document_first_heading = div_item_page.find_element(By.CLASS_NAME, 'documentFirstHeading')
        anchor_h1_document_first_heading = h1_document_first_heading.find_element(By.TAG_NAME, 'a')
        div_content_header_options_1_row_fluid = div_item_page.find_element(By.CSS_SELECTOR, 'content-header-options-1 row-fluid')
        div_document_by_line_span7 = div_content_header_options_1_row_fluid.find_element(By.CLASS_NAME, 'documentByLine span7')
        span_document_published = div_document_by_line_span7.find_element(By.CLASS_NAME, 'documentPublished')
        category = span_document_category.text
        title = anchor_h1_document_first_heading.text
        publication_date = span_document_published.text
        # post = Post(category, title, transform_to_date(publication_date))
        # self._driver.close()
        # return post
        print(transform_to_date(publication_date))
