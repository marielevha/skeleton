from django.forms import model_to_dict

from scraping.avito.avito_scraper import AvitoScraper
from scraping.avito.avito_clean_data import AvitoCleanData
from scraping.marocannonces.ma_scraper import MAScraper
from scraping.marocannonces.ma_clean_data import MACleanData
from scraping.utils import constants as const
from .models import Announce
import threading
import schedule
import pytz
utc = pytz.UTC


class RunScraper:
    def __init__(self):
        print("###################### START SCRAPING ######################")
        self.state = False
        self.ma_final_data = []
        self.avito_final_data = []
        # self.db = Announce()

    def scrape_avito(self, last_record=None):
        with AvitoScraper(last_record=last_record) as avito:
            # Scrap Data From Avito
            avito.land_first_page()
            # avito.write_search_query(query=const.SCRAP_MARKET)
            # avito.write_search_query(query='iphone 4')
            # avito.select_category(category='Téléphones')
            avito.get_total_pages()
            avito.report_data()

            # Clear & Affect data
            avito_cleaner = AvitoCleanData(avito.get_final_data())
            self.avito_final_data = avito_cleaner.clean_up_missing_data()

            #Saving to db
            db_avito_thread = threading.Thread(target=self.save_avito_data_to_db)
            db_avito_thread.start()

    def scrape_ma(self, last_record=None):
        # Scrap Data From Maroc Annonces
        with MAScraper(last_record=last_record) as ma:
            ma.land_first_page()
            # ma.select_category(category='Téléphones Portables')
            # ma.select_city()
            ma.write_search_query(query=const.SCRAP_MARKET)
            ma.click_search()
            ma.get_next_page_url()
            ma.report_results()

            # Clear & Affect data
            ma_cleaner = MACleanData(ma.get_final_data())
            self.ma_final_data = ma_cleaner.clean_up_missing_data()

            # Saving to db
            db_ma_thread = threading.Thread(target=self.save_ma_data_to_db)
            db_ma_thread.start()

    # DB ACTIONS
    def get_last_ma_ad_from_db(self):
        try:
            # ad = Announce.objects.filter(source=const.MA_SOURCE).first()
            ad = Announce.objects.filter(source=const.MA_SOURCE).latest('date')
            return ad
        except Announce.DoesNotExist:
            return None

    def get_last_avito_ad_from_db(self):
        try:
            # ad = Announce.objects.filter(source=const.AVITO_SOURCE).first()
            ad = Announce.objects.filter(source=const.AVITO_SOURCE).latest('date')
            return ad
        except Announce.DoesNotExist:
            return None

    def save_in_db(self, el, source):
        el_time = ''
        if source == const.MA_SOURCE:
            el_time = el['time']
        date = el['format_date'].replace(tzinfo=utc)

        Announce.objects.create(
            title=el['title'], city=el['city'].lower(), price=el['price'],
            type=el['type'], source=el['source'], date=date,
            original_date=el['date'], original_time=el_time, link=el['link']
        ).save()

    def save_ma_data_to_db(self):
        # SAVE MA DATA
        for el in self.ma_final_data[::-1]:
            self.save_in_db(el, const.MA_SOURCE)

    def save_avito_data_to_db(self):
        # SAVE AVITO DATA
        for el in self.avito_final_data[::-1]:
            self.save_in_db(el, const.AVITO_SOURCE)


def launch_schedule():
    schedule.every(5).minutes.do(launch_scraping)
    while True:
        schedule.run_pending()


def launch_scraping():
    runner = RunScraper()
    # MA THREAD
    ma_last_record = runner.get_last_ma_ad_from_db()
    if ma_last_record is not None:
        ma_last_record = model_to_dict(ma_last_record)
    ma_thread = threading.Thread(target=runner.scrape_ma, args=(ma_last_record,))

    # AVITO THREAD
    avito_last_record = runner.get_last_avito_ad_from_db()
    if avito_last_record is not None:
        avito_last_record = model_to_dict(avito_last_record)
    avito_thread = threading.Thread(target=runner.scrape_avito, args=(avito_last_record,))

    ma_thread.start()
    avito_thread.start()



