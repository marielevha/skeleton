import warnings
import dateparser
import utils.constants as const

# Ignore dateparser warnings regarding pytz
warnings.filterwarnings(
    "ignore",
    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
)


class AvitoCleanData:
    def __init__(self, input_data=const.AVITO_FAKE_DATA):
        self.input_data = input_data
        self.output_data = []

    def add_type_by_string_contains(self):
        for el in self.input_data.copy():
            for phone in const.PHONE_TYPES[::-1]:
                if phone.lower() in el["title"].lower():
                    el["type"] = phone.lower()
                    self.output_data.append(el)
                    break

    def format_date(self):
        for el in self.output_data.copy():
            dt = f'{el["date"]}'  # {el['time']}"
            el["date"] = dateparser.parse(dt)  # .date() | .time()

    def format_price(self):
        for el in self.output_data.copy():
            price = el['price'].replace('DH', '')
            el['price'] = float(price.replace(' ', ''))

    def clean_up_missing_data(self):
        self.add_type_by_string_contains()
        self.format_date()
        self.format_price()
        return self.output_data

    def show_output(self):
        print(self.output_data)


# cleaner = AvitoCleanData()
# cleaner.clean_up_missing_data()
# cleaner.show_output()
# print(f"LENGTH OUTPUT DATA: {len(cleaner.output_data)}")
#
# for ell in cleaner.output_data:
#     print(f"EL DATE: {ell}")
