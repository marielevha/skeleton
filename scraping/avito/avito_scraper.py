import time
import os
from scraping.utils import constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
import dateparser
import pytz
utc = pytz.UTC


class AvitoScraper(webdriver.Chrome):
    def __init__(self, driver_path=const.SELENIUM_DRIVERS_PATH, teardown=False, last_record=None):
        print(f"LAST RECORD: {last_record}")
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
        self.last_record = last_record

        self.data = dict()
        self.data["status"] = 0
        self.data["data"] = []
        self.data["page"] = 1
        self.path = None
        self.totalPages = 1
        self.currentPages = 1
        self.next = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.AVITO_BASE_URL2)

    def write_search_query(self, query):
        global query_element
        try:
            query_element = self.find_element(By.NAME, 'q')
        except:
            query_element = self.find_element(By.CSS_SELECTOR, 'input[placeholder="Que recherchez-vous?"]')
        finally:
            query_element.clear()
            query_element.send_keys(query)

    def select_category(self, category='Toutes les catégories'):
        category_element = Select(self.find_element(
            By.ID,
            'catgroup'
        ))
        category_element.select_by_visible_text(category)

    def filter_city(self, city=None):
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

    def select_city(self, city=None):
        if city is not None:
            self.filter_city(city)
        city_container_el = self.find_element(
            By.CSS_SELECTOR,
            'div[data-testid="cities"]'
        )

        city_elements = city_container_el.find_elements(
            By.CSS_SELECTOR,
            'button[class="h1t2kn-0 bNbXEC"]'
        )
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
        for box in boxes:
            try:
                ad = dict()
                ad["title"] = " ".join(self.get_ad_title(box).split())
                ad["price"] = self.get_ad_price(box)
                ad["city"] = " ".join(self.get_ad_city(box).split())
                ad["date"] = " ".join(self.get_ad_date(box).split())
                ad['link'] = self.get_ad_link(box)
                ad['source'] = const.AVITO_SOURCE

                if self.last_record is not None:
                    if dateparser.parse(ad['date']).replace(tzinfo=utc) > self.last_record['date'].replace(tzinfo=utc):
                        self.data["data"].append(ad)
                    else:
                        self.next = False
                        self.quit()
                        break
            except Exception as e:
                print(e)
                continue

        # Pass to next page if exist
        self.navigate_to_next_page()

    def get_ad_title(self, box: WebElement):
        title_container = box.find_element(
            By.CSS_SELECTOR,
            'span[data-testid="adSubject"]'
        )
        title = title_container.find_element(
            By.TAG_NAME,
            'span'
        ).get_attribute('innerHTML')
        return title.lower()

    def get_ad_price(self, box: WebElement):
        price_container = box.find_element(
            By.CSS_SELECTOR,
            'span[data-testid="adPrice"]'
        )
        price = price_container.find_elements(
            By.TAG_NAME,
            'span'
        )[0].get_attribute('innerHTML')
        return price

    def get_ad_city(self, box: WebElement):
        container = box.find_elements(
            By.CSS_SELECTOR,
            'span[class="sc-1x0vz2r-0 kIeipZ"]'
        )
        if len(container) == 2:
            city = container[1].get_attribute('innerHTML')
            return city.lower()

    def get_ad_date(self, box: WebElement):
        container = box.find_elements(
            By.CSS_SELECTOR,
            'span[class="sc-1x0vz2r-0 kIeipZ"]'
        )
        if len(container) == 2:
            date = container[0].get_attribute('innerHTML')
            return date

    def get_ad_link(self, box: WebElement):
        link = ''
        try:
            link = box.find_element(By.TAG_NAME, 'a').get_attribute('href').strip()
        finally:
            return link

    def get_final_data(self):
        return self.data['data']

    def navigate_to_next_page(self):
        if self.path is not None and self.totalPages > self.currentPages and self.next:
            self.currentPages += 1
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

            self.get_next_page_url()
        except Exception as e:
            self.totalPages = 1

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
            self.next = True
        except Exception as e:
            self.path = None
