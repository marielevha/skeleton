# import time
#
# from avito.avito_scraper import AvitoScraper
# from marocannonces.ma_scraper import MAScraper
# import dateparser
# from scraping.models import Announce
#
# try:
#     # with AvitoScraper() as bot:
#     #     bot.land_first_page()
#     #     bot.write_search_query(query='Iphone')
#     #     # bot.click_search()
#     #     bot.select_category(category='Téléphones')
#     #     # bot.filter_city('Agadir')
#     #     # bot.select_city(city='Casablanca')
#     #     # bot.select_city()
#     #     bot.click_search()
#     #     bot.get_total_pages()
#     #     # bot.navigate_to_next_page()
#     #     bot.report_data()
#     #     bot.show_ad()
#
#     date = '22 Aoû'
#     time = '14:54'
#     last_record = {'title': 'Apple iPhone 8 64Go Gold', 'price': '1 800 DH', 'date': '22 Aoû', 'time': '14:54'}
#     print(f"LR: {last_record}")
#     with MAScraper(last_record=last_record) as bot:
#         bot.land_first_page()
#         # bot.select_category()
#         bot.select_category(category='Téléphones Portables')
#         bot.select_city()
#         bot.write_search_query(query='iphone 8')
#         bot.click_search()
#         # time.sleep(20)
#         bot.get_next_page_url()
#         bot.report_results()
#         # bot.get_next_page_url()
#         print('####################################### FINAL DATA #######################################')
#         bot.show_ad()
# except Exception as e:
#     if 'in PATH' in str(e):
#         print(
#             'You are trying to run the bot from command line \n'
#             'Please add to PATH your Selenium Drivers \n'
#             'Windows: \n'
#             '    set PATH=%PATH%;C:path-to-your-folder \n \n'
#             'Linux: \n'
#             '    PATH=$PATH:/path/toyour/folder/ \n'
#         )
#     else:
#         raise
