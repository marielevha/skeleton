import time

from avito.avito_scraper import AvitoScraper
from marocannonces.ma_scraper import MAScraper

try:
    # with AvitoScraper() as bot:
    #     bot.land_first_page()
    #     bot.write_search_query(query='xiaomi')
    #     # bot.click_search()
    #     bot.select_category(category='Téléphones')
    #     # bot.filter_city('Agadir')
    #     bot.select_city(city='Agadir')
    #     bot.click_search()
    #     bot.get_total_pages()
    #     # bot.navigate_to_next_page()
    #     bot.report_data()
    #     bot.show_ad()

    with MAScraper() as bot:
        bot.land_first_page()
        # bot.select_category()
        bot.select_category(category='Téléphones Portables')
        bot.select_city()
        bot.write_search_query(query='iphone 8')
        bot.click_search()
        # time.sleep(20)
        bot.get_next_page_url()
        bot.report_results()
        # bot.get_next_page_url()
        print('####################################### FINAL DATA #######################################')
        bot.show_ad()
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
