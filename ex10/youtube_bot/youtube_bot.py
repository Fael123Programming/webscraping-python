from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from os import system, name
from prettytable import PrettyTable

BASE_URL = 'https://www.youtube.com/'


def clear_prompt():
    system('cls' if name == 'nt' else 'clear')


class YoutubeBot(webdriver.Firefox):

    def __init__(self):
        super().__init__(service=FirefoxService(GeckoDriverManager().install()))
        self.implicitly_wait(5)
        clear_prompt()
        self._channels_list = list()
        self._channels_data = list()

    def ask_channels(self):
        print('-' * 100)
        channels = input('Comma-separated list of channels: ')
        if len(channels) == 0 or len(channels.strip()) == 0:
            print('-' * 100)
            print('# Invalid input. Try entering valid channel names instead! #')
            exit(0)
        if ',' in channels:
            for channel in channels.split(','):
                self._channels_list.append(channel.strip())
        else:
            self._channels_list.append(channels.strip())
        clear_prompt()

    def get_channels_data(self):
        for channel in self._channels_list:
            channel_info = self._get_channel_info(channel)
            self._channels_data.append(channel_info)

    def display_channels_data(self):
        table = PrettyTable(['channel', 'subscribers', 'video count', 'date of join', 'total views'])
        table.add_rows(self._channels_data)
        print(table)

    def _get_channel_info(self, channel: str) -> list:
        channel_info = list()
        self.get(BASE_URL + f'results?search_query={channel}')
        filter_pane = self.find_element(By.CSS_SELECTOR, 'a[class="yt-simple-endpoint style-scope ytd-toggle-butto'
                                                         'n-renderer"]')
        filter_pane.click()
        filter_type_groups = self.find_element(By.ID, 'collapse-content')
        type_group = filter_type_groups.find_elements(By.CSS_SELECTOR, 'ytd-search-filter-group-renderer')[1]
        channel_mark = type_group.find_elements(By.TAG_NAME, 'a')[1]
        channel_mark.click()
        channel_boxes = self.find_elements(By.TAG_NAME, 'ytd-channel-renderer')
        first_channel_box = channel_boxes[0]
        channel_subscribers = first_channel_box.find_element(By.ID, 'subscribers').text.split(' ')[0].strip()
        channel_video_count = first_channel_box.find_element(By.ID, 'video-count').text.split(' ')[0].strip()
        channel_title = first_channel_box.find_element(By.ID, 'text-container')
        channel_info.append(channel_title.text)
        channel_info.append(channel_subscribers)
        channel_info.append(channel_video_count)
        channel_title.click()
        tabs = self.find_element(By.ID, 'tabsContent')
        about_tab = None
        for tab in tabs.find_elements(By.TAG_NAME, 'tp-yt-paper-tab'):
            if tab.text == 'ABOUT':
                about_tab = tab
        about_btn = about_tab.find_element(By.TAG_NAME, 'div')
        self.execute_script('arguments[0].click();', about_btn)
        stats_column = self.find_element(By.ID, 'right-column')
        stats = stats_column.find_elements(By.TAG_NAME, 'yt-formatted-string')
        date_of_join = stats[1].text.replace('Joined ', '')
        channel_info.append(date_of_join)
        total_views = stats[2].text.replace(' views', '')
        channel_info.append(total_views)
        return channel_info

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
