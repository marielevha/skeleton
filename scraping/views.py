import datetime

from django.shortcuts import render
from .models import City
from .models import Announce
from scraping import models
from utils import constants as const
from django.http import HttpResponse
from avito.avito_scraper import AvitoScraper
from avito.avito_clean_data import AvitoCleanData
from marocannonces.ma_scraper import MAScraper
from marocannonces.ma_clean_data import MACleanData
from utils import constants as const
import threading
import schedule
import time
from django.forms.models import model_to_dict
from .run import launch_scraping


"""class RunScraper:
    def __init__(self):
        self.state = False
        self.ma_final_data = []
        self.avito_final_data = []

    def scrape_avito(self):
        with AvitoScraper() as avito:
            # Scrap Data From Avito
            avito.land_first_page()
            avito.write_search_query(query=const.SCRAP_MARKET)
            avito.select_category(category='Téléphones')
            avito.get_total_pages()
            avito.report_data()
            avito.show_ad()

            # Clear & Affect data
            avito_cleaner = AvitoCleanData(avito.get_final_data())
            self.avito_final_data = avito_cleaner.clean_up_missing_data()

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

    # DB ACTIONS
    def get_last_ma_ad_from_db(self):
        try:
            ad = Announce.objects.filter(source=const.MA_SOURCE).first()
            # ad = Announce.objects.filter(source=const.MA_SOURCE).latest('id')
            return ad
        except Announce.DoesNotExist:
            return None

    def get_last_avito_ad_from_db(self):
        print(self)

    def save_data_to_db(self):
        print(len(self.ma_final_data))
        for el in self.ma_final_data:
            ad = Announce.objects.create(
                title=el['title'], city=el['city'], price=el['price'],
                type=el['type'], source=el['source'], date=datetime.date.today(),
                original_date=el['date'], original_time=el['time']
            ).save()
            print(ad)"""


def index(request):
    """run = RunScraper()
    lr = run.get_last_ma_ad_from_db()
    if lr is not None:
        lr = model_to_dict(lr)
    run.scrape_ma(last_record=lr)
    run.save_data_to_db()"""
    launch_scraping()
    cities = City.objects.all()
    announces = Announce.objects.all()
    return render(request, 'index.html', {
        "cities": cities,
        "announces": announces,
    })
