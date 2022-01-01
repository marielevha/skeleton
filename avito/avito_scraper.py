import json
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


# def get_options():
#     options = Options()
#     options.add_argument("--window-size=1920,1080")
#     options.add_argument("--start-maximized")
#     options.add_argument("--headless")
#     return options


class AvitoScraper(webdriver.Chrome):
    def __init__(self, driver_path=const.SELENIUM_DRIVERS_PATH, teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        # options = webdriver.ChromeOptions()
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # options.add_argument('headless')
        options = const.CHROME_OPTIONS()
        super(AvitoScraper, self).__init__(options=options)
        self.implicitly_wait(10)
        self.maximize_window()

        self.data = dict()
        self.data["status"] = 0
        self.data["data"] = []
        self.data["page"] = 1
        self.path = None
        self.totalPages = 1
        self.currentPages = 1
        self.next = False
        # self.data['current_url'] = self.current_url

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.AVITO_BASE_URL)

    def write_search_query(self, query):
        query_element = self.find_element(By.NAME, 'q')
        query_element.clear()
        query_element.send_keys(query)

    def select_category(self, category='Toutes les catégories'):
        category_element = Select(self.find_element(
            By.ID,
            'catgroup'
        ))
        category_element.select_by_visible_text(category)

    def filter_city(self, city=None):
        # filter_element = self.find_element(
        #     By.CSS_SELECTOR,
        #     'input[id="filter-list-input"]'
        # )
        open_filter_element = WebDriverWait(self, 5).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'svg[aria-labelledby="MapPinLineTitleID"]'
            ))
        )
        open_filter_element.click()

        filter_element = WebDriverWait(self, 5).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'input[id="filter-list-input"]'
            ))
        )
        filter_element.clear()
        filter_element.send_keys(city)
        time.sleep(3)

    def select_city(self, city=None):
        if city is not None:
            self.filter_city(city)
        # city_element = Select(self.find_element(
        #     By.ID,
        #     'searcharea_expanded'
        # ))
        # city_element.select_by_visible_text(city)

        city_container_el = self.find_element(
            By.CSS_SELECTOR,
            'div[data-testid="cities"]'
        )

        city_elements = city_container_el.find_elements(
            By.CSS_SELECTOR,
            'button[class="h1t2kn-0 bNbXEC"]'
        )
        # city_elements[1].click()
        isChooseCity = False
        for el in city_elements:
            if not isChooseCity:
                isChooseCity = True
                el.click()
                break

    def click_search(self):
        search_button = self.find_element(
            By.CSS_SELECTOR,
            'button[type="submit"]'
        )
        search_button.click()

    def report_data(self):
        data_container = WebDriverWait(self, 5).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'div[class="sc-1nre5ec-0 gpXkJn listing"]'
            ))
        )

        boxes = data_container.find_elements(
            By.CSS_SELECTOR,
            'div[class="oan6tk-0 hEwuhz"]'
        )

        print(len(boxes))
        for box in boxes:
            ad = dict()
            ad["title"] = " ".join(self.get_ad_title(box).split())
            ad["price"] = self.get_ad_price(box)
            ad["city"] = " ".join(self.get_ad_city(box).split())
            ad["date"] = " ".join(self.get_ad_date(box).split())
            ad['source'] = "avito"
            self.data["data"].append(ad)

        print(self.data)
        # Pass to next page if exist
        self.navigate_to_next_page()

    def navigate_to_next_page1(self):
        self.scroll_down()
        self.implicitly_wait(10)

        self.find_element(
            By.XPATH,
            ''
        ).click()
        # div = self.find_element(
        #     By.CSS_SELECTOR,
        #     'div[class="sc-2y0ggl-0 jXwFwm"]'
        # )
        #
        # print(div.find_elements(By.TAG_NAME, 'a')[-1].get_attribute('innerHTML'))
        # print(div.find_elements(By.TAG_NAME, 'a')[-1].get_attribute('outerHTML'))
        # div.find_elements(By.TAG_NAME, 'a')[-1].click()
        # next_page_element = div.find_element(
        #     By.CSS_SELECTOR,
        #     'svg[aria-labelledby="ChevronRightTitleID"]'
        # )
        #
        # next_page_element.click()
        # print(next_page_element.get_attribute('outerHTML'))
        # next_page_element.click()
        # try:
        #     paginate_container_el = WebDriverWait(self, 5).until(
        #         EC.presence_of_element_located((
        #             By.CSS_SELECTOR,
        #             'div[class="sc-2y0ggl-0 jXwFwm"]'
        #         ))
        #     )
        #
        #     isLastPage = False
        #     while not isLastPage:
        #         print('Hello')
        #         try:
        #             next_page_element = paginate_container_el.find_element(
        #                 By.CSS_SELECTOR,
        #                 'svg[aria-labelledby="ChevronRightTitleID"]'
        #             )
        #
        #             next_page_element.click()
        #         except Exception as e:
        #             print(e)
        #             print("IS LAST PAGE")
        #             isLastPage = True
        # except Exception as e:
        #     print(e)
        #     print('NOT PAGINATE')

    def get_ad_title(self, box: WebElement):
        title_container = box.find_element(
            By.CSS_SELECTOR,
            'span[data-testid="adSubject"]'
        )
        title = title_container.find_element(
            By.TAG_NAME,
            'span'
        ).get_attribute('innerHTML')
        return title

    def get_ad_price(self, box: WebElement):
        try:
            price_container = box.find_element(
                By.CSS_SELECTOR,
                'span[data-testid="adPrice"]'
            )
            price = price_container.find_elements(
                By.TAG_NAME,
                'span'
            )[0].get_attribute('innerHTML')
            return price
        except Exception as e:
            print(e)
            print("PRICE UNDEFINED")
            return None

    def get_ad_city(self, box: WebElement):
        # svg1_container = WebDriverWait(self, 5).until(
        #     EC.presence_of_element_located((
        #         By.CSS_SELECTOR,
        #         'svg[aria-labelledby="TimeFillTitleID"]'
        #     ))
        # )

        # svg2_container = WebDriverWait(self, 5).until(
        #     EC.presence_of_element_located((
        #         By.CSS_SELECTOR,
        #         'svg[aria-labelledby="MapPinFillTitleID"]'
        #     ))
        # )
        container = box.find_elements(
            By.CSS_SELECTOR,
            'span[class="sc-1x0vz2r-0 kIeipZ"]'
        )
        if len(container) == 2:
            city = container[1].get_attribute('innerHTML')
            return city

    def get_ad_date(self, box: WebElement):
        container = box.find_elements(
            By.CSS_SELECTOR,
            'span[class="sc-1x0vz2r-0 kIeipZ"]'
        )
        if len(container) == 2:
            date = container[0].get_attribute('innerHTML')
            return date

    def scroll_up(self):
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_down(self):
        self.execute_script("window.scrollTo(0, 7080);")

    def show_ad(self):
        # print(json.dumps(self.data))
        print(self.data)

    def navigate_to_next_page(self):
        if self.path is not None and self.totalPages > self.currentPages and self.next:
            self.currentPages += 1
            script = "window.location.href='" + self.path + "'"
            print('PATH: ' + self.path)
            self.execute_script(f"window.location.href='{self.path}'")
            self.get_total_pages()
            self.report_data()
        else:
            self.next = False

    def get_total_pages(self):
        try:
            paginate_container_el = WebDriverWait(self, 5).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    'div[class="sc-2y0ggl-0 jXwFwm"]'
                ))
            )

            page = paginate_container_el.find_elements(
                By.TAG_NAME, 'a'
            )[-2].get_attribute('innerHTML')
            self.totalPages = int(page)
            print(self.totalPages)

            self.get_next_page_url()
        except Exception as e:
            self.totalPages = 1
            print(e)
            print('NOT EXIST PAGINATION')

    def get_next_page_url(self):
        try:
            paginate_container_el = WebDriverWait(self, 5).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    'div[class="sc-2y0ggl-0 jXwFwm"]'
                ))
            )

            self.path = paginate_container_el.find_elements(
                By.TAG_NAME, 'a'
            )[-1].get_attribute('href')
            print(self.path)
            self.next = True
        except Exception as e:
            self.path = None
            print(e)
            print('NOT EXIST PAGINATION')
