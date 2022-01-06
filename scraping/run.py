import datetime

from django.forms import model_to_dict

from avito.avito_scraper import AvitoScraper
from avito.avito_clean_data import AvitoCleanData
from marocannonces.ma_scraper import MAScraper
from marocannonces.ma_clean_data import MACleanData
from utils import constants as const
from .models import Announce
import threading
import schedule
import time


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
            avito.write_search_query(query='iphone 4')
            avito.select_category(category='Téléphones')
            avito.get_total_pages()
            avito.report_data()
            avito.show_ad()

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
            ma.select_category(category='Téléphones Portables')
            ma.select_city()
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
            ad = Announce.objects.filter(source=const.MA_SOURCE).latest('id')
            return ad
        except Announce.DoesNotExist:
            return None

    def get_last_avito_ad_from_db(self):
        try:
            # ad = Announce.objects.filter(source=const.AVITO_SOURCE).first()
            ad = Announce.objects.filter(source=const.AVITO_SOURCE).latest('id')
            return ad
        except Announce.DoesNotExist:
            return None

    def save_in_db(self, el, source):
        el_time = ''
        if source == const.MA_SOURCE:
            el_time = el['time']
        date = el['format_date']
        # date = datetime.date.today()

        Announce.objects.create(
            title=el['title'], city=el['city'], price=el['price'],
            type=el['type'], source=el['source'], date=date,
            original_date=el['date'], original_time=el_time
        ).save()

    def save_ma_data_to_db(self):
        # SAVE MA DATA
        # print(len(self.ma_final_data))
        for el in self.ma_final_data[::-1]:
            self.save_in_db(el, const.MA_SOURCE)
            print(f"MA ADD TO DB")

    def save_avito_data_to_db(self):
        # SAVE AVITO DATA
        # print(len(self.ma_final_data))
        for el in self.avito_final_data[::-1]:
            self.save_in_db(el, const.AVITO_SOURCE)
            print(f"AVITO ADD TO DB")


def launch_schedule():
    schedule.every(5).minutes.do(launch_scraping)

    while True:
        schedule.run_pending()
        # time.sleep(1)


def launch_scraping():
    runner = RunScraper()
    # MA THREAD
    ma_last_record = runner.get_last_ma_ad_from_db()
    if ma_last_record is not None:
        ma_last_record = model_to_dict(ma_last_record)
        print(f"MA LR: {ma_last_record}")
    ma_thread = threading.Thread(target=runner.scrape_ma, args=(ma_last_record,))

    # AVITO THREAD
    avito_last_record = runner.get_last_avito_ad_from_db()
    if avito_last_record is not None:
        avito_last_record = model_to_dict(avito_last_record)
        print(f"AVITO LR: {avito_last_record}")
    avito_thread = threading.Thread(target=runner.scrape_avito, args=(avito_last_record,))

    # ma_thread.start()
    avito_thread.start()

    """# db_ma_thread = threading.Thread(target=runner.save_ma_data_to_db)
    db_avito_thread = threading.Thread(target=runner.save_avito_data_to_db)

    # ma_thread.start()
    avito_thread.start()

    # ma_thread.join()

    avito_thread.join()
    db_avito_thread.start()"""


    # print(f"MA DATA CLEAN LENGTH: {len(runner.ma_final_data)}")
    # print(f"MA DATA CLEAN: {runner.ma_final_data}")

    """run = RunScraper()
    # TEST MA
    # lr = run.get_last_ma_ad_from_db()
    # print(type(lr))
    # if lr is not None:
    #     lr = model_to_dict(lr)
    #     print(f"MA LR: {lr}")
    # run.scrape_ma(last_record=lr)

    # TEST AVITO
    lr = run.get_last_avito_ad_from_db()
    print(type(lr))
    if lr is not None:
        lr = model_to_dict(lr)
        print(f"MA LR: {lr}")
    run.scrape_avito(last_record=lr)
    run.save_data_to_db()"""


# launch_scraping()


