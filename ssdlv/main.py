import time
from utils import constants as const
from avito.avito_scraper import AvitoScraper
from marocannonces.ma_scraper import MAScraper
import dateparser
# from scraping.models import Announce

"""try:
    with AvitoScraper(last_record=None) as bot:
        bot.land_first_page()
        bot.write_search_query(query='Iphone')
        # bot.click_search()
        bot.select_category(category='Téléphones')
        # bot.filter_city('Agadir')
        # bot.select_city(city='Casablanca')
        # bot.select_city()
        bot.click_search()
        bot.get_total_pages()
        # bot.navigate_to_next_page()
        bot.report_data()
        bot.show_ad()

    # date = '22 Aoû'
    # time = '14:54'
    # last_record = {'title': 'Apple iPhone 8 64Go Gold', 'price': '1 800 DH', 'date': '22 Aoû', 'time': '14:54'}
    # print(f"LR: {last_record}")
    # with MAScraper(last_record=last_record) as bot:
    #     bot.land_first_page()
    #     # bot.select_category()
    #     bot.select_category(category='Téléphones Portables')
    #     bot.select_city()
    #     bot.write_search_query(query='iphone 8')
    #     bot.click_search()
    #     # time.sleep(20)
    #     bot.get_next_page_url()
    #     bot.report_results()
    #     # bot.get_next_page_url()
    #     print('####################################### FINAL DATA #######################################')
    #     bot.show_ad()
except Exception as e:
    if 'in PATH' in str(e):
        print(
            'You are trying to run the bot from command line \n'
            'Please add to PATH your Selenium Drivers \n'
            'Windows: \n'
            '    set PATH=%PATH%;C:path-to-your-folder \n \n'
            'Linux: \n'
            '    PATH=$PATH:/path/toyour/folder/ \n'
        )
    else:
        raise
"""


# for el in const.AVITO_FAKE_DATA:
#     dd = re.search(r'(\d{2})[\s/.,-](\w+)[\s/.,-](\d{4})$', el['date'])
#     print(dd)
import re
import csv
with open('../utils/sfs.csv', 'r') as read_obj:
    csv_reader = csv.reader(read_obj)
    i = 0
    j = 0
    t = []
    for row in csv_reader:
        value = row[1]
        i += 1
        for tp in const.PHONE_TYPES_INFO[::-1]:
            if tp['regex'] != '':
                word = re.search(tp['regex'], value.lower())
                if word is not None:
                    t.append(word)
                    print(f"TITLE: {value.lower()}, ID: {row[0]}, TYPE: {tp['model']}")
                    break
    print(f"FIND: {len(t)} | MISSING: {j} | ALL: {i}")