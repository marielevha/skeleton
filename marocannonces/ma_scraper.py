import time
import os
import utils.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
import dateparser
import warnings

# Ignore dateparser warnings regarding pytz
warnings.filterwarnings(
    "ignore",
    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
)


class MAScraper(webdriver.Chrome):
    def __init__(self, driver_path=const.SELENIUM_DRIVERS_PATH, teardown=False, last_record=None):
        print(f"LAST R TYPE: {type(last_record)}")
        # if last_record is None:
        #     last_record = {'title': 'Apple iPhone 8 64Go Gold', 'price': '1 800 DH', 'date': '22 Aoû', 'time': '14:54'}
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(MAScraper, self).__init__(options=options)
        self.implicitly_wait(10)
        self.maximize_window()
        self.last_record = last_record

        self.data = dict()
        self.data["status"] = 0
        self.data["data"] = []
        self.data["page"] = 1
        self.path = None
        self.pathPage = 1
        self.totalPages = 1
        self.lastPage = 1
        self.currentPages = 1
        self.next = False
        self.page = 1
        # self.data['current_url'] = self.current_url

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.MAROC_ANNOUNCE_BASE_URL)

    def select_category(self, category=None):
        if category is None:
            category_element = self.find_element(
                By.CSS_SELECTOR,
                'li[class="category_title cathptelephone"]'
            )
            category_element.click()
        else:
            category_element = Select(self.find_element(
                By.ID,
                'select-cat'
            ))
            category_element.select_by_visible_text(category)

    def select_city(self, city='Toutes les villes'):
        city_element = Select(self.find_element(
            By.ID,
            'select-ville'
        ))
        city_element.select_by_visible_text(city)

    def write_search_query(self, query):
        query_element = self.find_element(
            By.CSS_SELECTOR,
            'input[class="kw"]'
        )
        query_element.clear()
        query_element.send_keys(query)

    def click_search(self):
        search_button = self.find_element(
            By.CSS_SELECTOR,
            'input[value="Rechercher"]'
        )
        search_button.click()

    def get_next_page_url(self):
        print('####################################### GET NEXT PAGE URL #######################################')
        try:
            div_content = WebDriverWait(self, 5).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    'div [class="used-cars"]'
                ))
            )
            is_paginate = len(
                div_content.find_elements(
                    By.CSS_SELECTOR,
                    'div[class="contentpaging"]'
                )
            ) > 0

            if is_paginate:
                # Report data
                # self.report_results()

                pagination_ul = WebDriverWait(self, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[class="paging"]'))
                )

                # print(pagination_ul.get_attribute('innerHTML'))

                # Get next page url
                next_li = pagination_ul.find_element(
                    By.CSS_SELECTOR,
                    'li[class="next"]'
                )
                self.path = next_li.find_element(
                    By.TAG_NAME,
                    'a'
                ).get_attribute('href')
                self.pathPage = int(self.path.split('=')[-1])
                print(f"NEXT PAGE URL: {self.path}")
                print(f"NEXT PAGE NUMBER: {self.pathPage}")
                self.next = True
                self.get_last_page(pagination_ul)
        except Exception as e:
            self.path = None
            self.next = False
            print(e)

    def report_results(self):
        # result_list = self.find_element(
        #     By.CSS_SELECTOR,
        #     'ul[class="cars-list"]'
        # )
        result_list = WebDriverWait(self, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[class="cars-list"]'))
        )
        # print(result_list.get_attribute('outerHTML'))

        boxes = result_list.find_elements(
            By.TAG_NAME,
            'li'
        )
        # boxes = WebDriverWait(self, 10).until(
        #     EC.presence_of_all_elements_located((By.TAG_NAME, "li"))
        # )
        # print(boxes)
        # collections = []
        # print(len(boxes))
        for box in boxes:
            try:
                '''title = box.find_element(
                    By.TAG_NAME,
                    'h3'
                ).get_attribute('innerHTML')

                price = box.find_element(
                    By.TAG_NAME,
                    'strong[class="price"]'
                ).get_attribute('innerHTML')

                city = box.find_element(
                    By.CSS_SELECTOR,
                    'span[class="location"]'
                ).get_attribute('innerHTML')

                date_elements = box.find_elements(
                    By.CSS_SELECTOR,
                    'em[class="date"]'
                )

                el = date_elements[1].get_attribute('innerHTML')
                date = el.split('<br>')[0]
                time = date_elements[1].find_element(
                    By.TAG_NAME,
                    'span'
                ).get_attribute('innerHTML')'''

                ad = dict()
                ad['title'] = " ".join(self.get_ad_title(box).split())
                ad['price'] = " ".join(self.get_ad_price(box).split())
                ad['city'] = " ".join(self.get_ad_city(box).split())
                ad['date'] = " ".join(self.get_ad_date(box)[0].split())
                ad['time'] = " ".join(self.get_ad_date(box)[1].split())
                ad['source'] = const.MA_SOURCE

                current_record = {
                    'title': ad['title'],
                    'date': dateparser.parse(f"{ad['date']} {ad['time']}")
                }
                # print(f"CURRENT RECORD: {ad}")
                # print(f"LAST RECORD: {self.last_record}")
                # and (self.last_record['date'] < current_record['date'])
                if (self.last_record is not None) and (self.last_record['original_date'] == ad['date']) and (
                        self.last_record['original_time'] == ad['time']):
                    price = (ad['price'].replace('DH', '')).replace(' ', '')
                    if (self.last_record['title'] == ad['title']) and (self.last_record['price'] == float(price)):
                        self.next = False
                        print('##################################### EXACT #####################################')
                        print(f"CURRENT RECORD: {ad}")
                        print('##################################### EXACT #####################################')
                        # print(f"LAST RECORD: {self.last_record}")
                        self.quit()
                        break
                self.data['data'].append(ad)
            except Exception as e:
                print(e)
                continue
                # if const.NOT_FOUND_ELEMENT in e:
                #     print(e)
                #     continue
        print(self.data)
        self.navigate_to_next_page()

        # print(boxes)

    def get_ad_title(self, box: WebElement):
        title = box.find_element(
            By.TAG_NAME,
            'h3'
        ).get_attribute('innerHTML')
        return title

    def get_ad_price(self, box: WebElement):
        price = box.find_element(
            By.TAG_NAME,
            'strong[class="price"]'
        ).get_attribute('innerHTML')
        return price

    def get_ad_city(self, box: WebElement):
        city = box.find_element(
            By.CSS_SELECTOR,
            'span[class="location"]'
        ).get_attribute('innerHTML')
        return city

    def get_ad_date(self, box: WebElement):
        date_elements = box.find_elements(
            By.CSS_SELECTOR,
            'em[class="date"]'
        )

        el = date_elements[1].get_attribute('innerHTML')
        date = el.split('<br>')[0]
        time = date_elements[1].find_element(
            By.TAG_NAME,
            'span'
        ).get_attribute('innerHTML')
        return [date, time]

    def show_ad(self):
        print(self.data)

    def navigate_to_next_page(self):
        if self.path is not None and self.next:
            if self.pathPage < self.lastPage:
                self.execute_script(f"window.location.href='{self.path}'")
                self.get_next_page_url()
                self.report_results()
            elif self.pathPage == self.lastPage:
                self.execute_script(f"window.location.href='{self.path}'")
                self.get_next_page_url()
                self.report_results()
                self.next = False
        else:
            self.next = False

    def get_last_page(self, ul: WebElement):
        # Get last page number
        li_elements = ul.find_elements(
            By.CSS_SELECTOR,
            'li[class="item"]'
        )
        self.lastPage = int(li_elements[-1].find_element(
            By.TAG_NAME,
            'a'
        ).get_attribute('text'))
        print(f"LAST PAGE: {self.lastPage}")

    def get_final_data(self):
        return self.data['data']

    def check_an_exist_ad(self):
        print(self.last_record)
