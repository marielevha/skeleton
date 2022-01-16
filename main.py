# from scraping.models import Announce
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from scraping.utils import constants as const

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
import csv
# with open('scraping/utils/sfs.csv', 'r') as read_obj:
#     csv_reader = csv.reader(read_obj)
#     i = 0
#     j = 0
#     t = []
# t = ['iphone 8 plus 256 gb', 'iphone 8 plus neuf sous emballage']
# for row in t:
#     print(row)
#     for tp in const.PHONE_MODELS[::-1]:
#         if tp['regex'] != '':
#             word = re.search(tp['regex'], row)
#             if word is not None:
#                 print(f"TITLE: {row.lower()}, TYPE: {tp['model']}")
#                 break
# #         if 'afficheur' in row[1].lower():
# #             print(f"TITLE: {row[1]}, PRICE: {row[2]}")
# #     print(f"FIND: {len(t)} | MISSING: {j} | ALL: {i}")
#
# import smtplib
# s = smtplib.SMTP(host='smtp.gmail.com', port=25)
# s.starttls()
# s.login('suptech.3annee@gmail.com', 'Suptech19/20')
#
# msg = MIMEMultipart()
# msg['From'] = 'suptech.3annee@gmail.com'
# msg['To'] = 'mspeedy733@gmail.com'
# msg['Subject'] = "Produits maroc annonces"
# message = 'Hello'
# msg.attach(MIMEText(message, 'plain'))
# s.send_message(msg)

import dateparser
import datetime
with open('scraping/utils/announces.csv', 'r') as read_obj:
    csv_reader = csv.reader(read_obj)
    final_data = []
    missing_data = []
    for row in csv_reader:
        title = row[1]
        price = row[2]
        missing_data.append(row)
        for tp in const.PHONE_MODELS[::-1]:
            if tp['regex'] != '':
                word = re.search(tp['regex'], title.lower())
                if (word is not None) and ('afficheur' not in title.lower() or 'samsung' not in title.lower()) and (float(price) > const.MIN_PRICE_ANNOUNCE or float(price) < const.MAX_PRICE_ANNOUNCE):
                    #print(f"TITLE: {title.lower()}, PRICE: {price}, TYPE: {tp['model']}")
                    #final_data.append(row)
                    #print(row[4])
                    d = datetime.datetime.fromisoformat(row[4])
                    # dd = d.strftime('%Y-%m-%d %H:%M:%S')
                    dd = d.strftime('%d %b %Y %H:%M')
                    print(dateparser.parse(dd))
                    #print(dateparser.parse('12:30'))
                    #print(d.day, d.month, d.year, d.hour, d.minute, d.second)
                    #d = row[4]
                    #print(dateparser.parse())
                    break
                    #print(row[1], row[2], row[3], row[4])

                    # Announce.objects.create(
                    #     title=row[1], city=row[3], price=row[2],
                    #     type=tp['model'], source=row['source'], date=dateparser.parse(row[4]),
                    #     original_date=row[7], original_time='', link=link
                    # )
                    break
            # if 'afficheur' in title.lower() or 'samsung' in title.lower():
            #     print(f"TITLE: {title}, PRICE: {price}")
            #     break
            # if float(price) < const.MIN_PRICE_ANNOUNCE or float(price) > const.MAX_PRICE_ANNOUNCE:
            #     print(f"TITLE: {title}, PRICE: {price}")
            #     break
    print(f"FIND: {len(final_data)} | MISSING: {len(missing_data)} | ALL: {len(missing_data) - len(final_data)}")

print(dateparser.parse('12:30'))
