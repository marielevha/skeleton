import re
import warnings
import dateparser
from datetime import datetime
from scraping.utils import constants as const

# Ignore dateparser warnings regarding pytz
warnings.filterwarnings(
    "ignore",
    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
)


class MACleanData:
    def __init__(self, input_data=const.MA_FAKE_DATA):
        self.input_data = input_data
        self.output_data = []

    def add_type_by_string_contains(self):
        for el in self.input_data.copy():
            for phone in const.PHONE_TYPES[::-1]:
                if phone.lower() in el['title'].lower():
                    el['type'] = phone.lower()
                    self.output_data.append(el)
                    break

    def format_type_announce(self):
        for el in self.input_data.copy():
            original_title = el['title']
            for model in const.PHONE_MODELS[::-1]:
                if model['regex'] != '':
                    search_result = re.search(model['regex'], original_title.lower())
                    if search_result is not None:
                        el['type'] = model['model']
                        self.output_data.append(el)
                        break

    def format_date(self):
        """for el in self.output_data.copy():
            dt = f"{el['date']} {el['time']}"
            el['datetime'] = dateparser.parse(dt)  # .date() | .time()"""
        for el in self.output_data.copy():
            # Format: "20 Déc 2021"
            dd = re.search(r'(\d{2})[\s/.,-](\w{3})[\s/.,-](\d{4})$', el['date'])
            if dd is not None:
                dt = f"{el['date']} {el['time']}"
                el['format_date'] = dateparser.parse(dt)
            else:
                # Format: "20 Déc"
                dd1 = re.search(r'(\d{2})[\s/.,-](\w{3})$', el['date'])
                if dd1 is not None:
                    current_date = datetime.now()
                    date = dateparser.parse(el['date'])
                    ad_date = date
                    if ad_date > current_date:
                        year = (date.date().year - 1)
                        new_date = dateparser.parse(f"{el['date']} {year} {el['time']}")
                        el['format_date'] = new_date
                    else:
                        new_date = dateparser.parse(f"{el['date']} {el['time']}")
                        el['format_date'] = new_date
                else:
                    new_date = dateparser.parse(f"{el['date']} {el['time']}")
                    el['format_date'] = new_date

    def format_price(self):
        for el in self.output_data.copy():
            price = el['price'].replace('DH', '')
            price = float(price.replace(' ', ''))
            if price < const.MIN_PRICE_ANNOUNCE or price > const.MAX_PRICE_ANNOUNCE:
                self.output_data.remove(el)
                continue
            el['price'] = price
            # if el['price'] >= float(50000):
            #     self.output_data.remove(el)

    def remove_nan(self):
        for el in self.output_data.copy():
            if 'afficheur' in el['title'].lower():
                self.output_data.remove(el)
            elif 'samsung' in el['title'].lower():
                self.output_data.remove(el)

    def clean_up_missing_data(self):
        # self.add_type_by_string_contains()
        self.format_type_announce()
        self.format_date()
        self.format_price()
        self.remove_nan()
        return self.output_data


# cleaner = MACleanData()
# cleaner.clean_up_missing_data()
# # cleaner.show_output()
# print(f"LENGTH OUTPUT DATA: {len(cleaner.output_data)}")
#
# for ell in cleaner.output_data:
#     print(f"EL DATE: {ell}")
"""
import re
from datetime import datetime
import time
import locale
# locales = ['fr', 'zh', 'tr']
# locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')


clean_up_data = []
phones_types = [
    'iPhone 3G',
    'iPhone 3GS',
    'iPhone 4',
    'iPhone 4S',
    'iPhone 5',
    'iPhone 5c',
    'iPhone 5s',
    'iPhone 6',
    'iPhone 6 Plus',
    'iPhone 6s',
    'iPhone 6s Plus',
    'iPhone SE',
    'iPhone 7',
    'iPhone 7 Plus',
    'iPhone 8',
    'iPhone 8 Plus',
    'iPhone X',
    'iPhone XS',
    'iPhone XS Max',
    'iPhone XR',
    'iPhone 11',
    'iPhone 11 Pro',
    'iPhone 11 Pro Max',
    'iPhone SE',
    'iPhone 12',
    'iPhone 12 mini',
    'iPhone 12 Pro',
    'iPhone 12 Pro Max',
    'iPhone 13',
    'iPhone 13 mini',
    'iPhone 13 Pro',
    'iPhone 13 Pro Max'
]


def format_date():
    for el in clean_up_data.copy():
        # dt = f"{el['date']} {el['time']}"
        # el['date'] = dateparser.parse(dt).date()

        # for el in self.output_data.copy():
        #     dt = f"{el['date']} {el['time']}"
        #     el['datetime'] = dateparser.parse(dt)  # .date() | .time()
        # Format: "20 Déc 2021"
        dd = re.search(r'(\d{2})[\s/.,-](\w{3})[\s/.,-](\d{4})$', el['date'])
        if dd is not None:
            # print(f'Format: 20 Déc 2021 -> {dd}')
            dt = f"{el['date']} {el['time']}"
            el['date'] = dateparser.parse(dt)
            # print(f"DATA: {el['date']}")
        # Format: "20 Déc"
        else:
            dd1 = re.search(r'(\d{2})[\s/.,-](\w{3})$', el['date'])
            # print(f'Format: 20 Déc -> {dd1}')
            if dd1 is not None:
                # current_month = datetime.now().month
                current_date = datetime.now()

                date = dateparser.parse(el['date'])
                # ad_month = date.date().month
                ad_date = date

                if ad_date > current_date:
                    year = (date.date().year - 1)
                    new_date = dateparser.parse(f"{el['date']} {year} {el['time']}")
                    el['date'] = new_date
                    print(f"AD Month {el['date']}")
                else:
                    print("ad_month <<< current_month")
                    new_date = dateparser.parse(f"{el['date']} {el['time']}")
                    print(f"AD Date {new_date}")
            else:
                dd2 = re.search(r'(\w)$', el['date'])
                # print(f'Format: Hier/Aujourd\'hui -> {dd2}')
                new_date = dateparser.parse(f"{el['date']} {el['time']}")
                el['date'] = new_date
                # print(f"AD Month {el['date']}")


def format_price():
    for el in clean_up_data.copy():
        price = el['price'].replace('DH', '')
        el['price'] = float(price.replace(' ', ''))


def add_type_by_string_contains():
    for el in const.MA_FAKE_DATA.copy():
        for phone in const.PHONE_TYPES[::-1]:
            if phone.lower() in el['title'].lower():
                el['type'] = phone.lower()
                #print(el)
                clean_up_data.append(el)
                break
    return clean_up_data


def add_type_by_regex():
    print()


def clean_up_missing_data():
    add_type_by_string_contains()
    format_date()
    format_price()

    # for el in clean_up_data:
    #     print(el)


clean_up_missing_data()
# print(f"LENGTH SOURCES DATA {len(data['data'])}")
# print(f"LENGTH SOURCES DATA {len(clean_up_data)}")
# print(f"CONVERT STRING TO DATE {datetime.strptime('Jan 25, 2021', '%b %d, %Y').strftime('%Y-%m-%d')}")
# print(f"CONVERT STRING TO DATE {datetime.strptime('20 Dec 2021', '%d %b %Y').strftime('%Y-%m-%d')}")
#
# for date_string in [u"Aujourd'hui", "3 juillet", u"4 Août", u"Hier", "20 Déc 2021 12:30:43"]:
#     print(dateparser.parse(date_string).date())
#     print(dateparser.parse(date_string).time())"""

