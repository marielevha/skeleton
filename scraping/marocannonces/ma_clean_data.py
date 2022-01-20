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
