from selenium.webdriver.chrome.options import Options

# SCRAPING
BASE_URL = "https://www.booking.com"
AVITO_BASE_URL = 'https://www.avito.ma'
AVITO_BASE_URL2 = 'https://www.avito.ma/fr/maroc/téléphones/iphone--à_vendre'
MAROC_ANNOUNCE_BASE_URL = 'https://www.marocannonces.com/categorie/306/Multim%C3%A9dia.html?bloc=1'
MAROC_ANNOUNCE_BASE_URL2 = 'https://www.marocannonces.com/maroc/telephones-portables--b359.html?kw=Iphone'
SCRAP_MARKET = 'Iphone'
AVITO_SOURCE = 'avito'
MA_SOURCE = 'marocannonces'
SELENIUM_DRIVERS_PATH = r'/zdrivers/'
NOT_FOUND_ELEMENT = 'no such element: Unable to locate element'
MAX_PRICE_ANNOUNCE = 50000
MIN_PRICE_ANNOUNCE = 300
PHONE_TYPES = [
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
PHONE_MODELS = [
    {
        'model': 'iPhone 3G',
        'max-price': '',
        'regex': r'(\b(iphone)(|\s)3g(|\s)\b)'
    },
    {
        'model': 'iPhone 3GS',
        'max-price': '',
        'regex': r'(\b(iphone)(|\s)3gs(|\s)\b)'
    },
    {
        'model': 'iPhone 4',
        'max-price': '',
        'regex': r'(\b(iphone)(|\s)4(|\s)\b)'
    },
    {
        'model': 'iPhone 4S',
        'max-price': '',
        'regex': r'(\b(iphone)(|\s)4s(|\s)\b)'
    },
    {
        'model': 'iPhone 5',
        'max-price': '',
        'regex': r'(\b(iphone)(|\s)5(|\s)\b)'
    },
    {
        'model': 'iPhone 5c',
        'max-price': '',
        'regex': r'(\b(iphone)(|\s)5(|\s)c(|\s)\b)'
    },
    {
        'model': 'iPhone 5s',
        'max-price': '',
        'regex': r'(\b(iphone)(|\s)5(|\s)s(|\s)\b)'
    },
    {
        'model': 'iPhone 6',
        'max-price': '',
        'regex': r'(\b(iphone)(|\s)6(|\s)\b)'
    },
    {
        'model': 'iPhone 6 Plus',
        'max-price': '',
        'regex': r'(\b(\w+|\s)6(|\s)(plus|pls)(|\s)\b)'
    },
    {
        'model': 'iPhone 6s',
        'max-price': '',
        'regex': r'(\b(iphone)(|\s)6(|\s)s(|\s)\b)'
    },
    {
        'model': 'iPhone 6s Plus',
        'max-price': '',
        'regex': r'(\b(\w+|\s)6(|\s)s(|\s)(plus|pls)(|\s)\b)'
    },
    {
        'model': 'iPhone SE',
        'max-price': '',
        'regex': r'(\b(iphone)(|\s)se(|\s)\b)'
    },
    {
        'model': 'iPhone 7',
        'max-price': '',
        'regex': r'(\b(iphone)(|\s)7(|\s)\b)'
    },
    {
        'model': 'iPhone 7 Plus',
        'max-price': '',
        'regex': r'(\b(\w+|\s)7(|\s)(plus|pls)(|\s)\b)'
    },
    {
        'model': 'iPhone 8',
        'max-price': '',
        'regex': r'(\b(iphone)(|\s)8(|\s)\b)'
    },
    {
        'model': 'iPhone 8 Plus',
        'max-price': '',
        'regex': r'(\b(\w+|\s)8(|\s)(plus|pls)(|\s)\b)'
    },
    {
        'model': 'iPhone X',
        'max-price': '',
        'regex': r'(\b(iphone)(|\s)x(|\s)\b)'
    },
    {
        'model': 'iPhone XS',
        'max-price': '',
        'regex': r'(\b(\w+|\s)xs(|\s)\b)'
    },
    {
        'model': 'iPhone XS Max',
        'max-price': '',
        'regex': r'(\b(\w+|\s)xs(|\s)(max|mx)\b)'
    },
    {
        'model': 'iPhone XR',
        'max-price': '',
        'regex': r'(\b(\w+|\s)xr(|\s|\w+)\b)'
    },
    {
        'model': 'iPhone 11',
        'max-price': '',
        'regex': r'(\b(\w+|\s)11(|\s)\b)',
        # 'regex': r'(\b(\w+|\s)11(\s||\w+)\b)'
    },
    {
        'model': 'iPhone 11 Pro',
        'max-price': '',
        'regex': r'(\b(\w+|\s)11(\s|)pro(\s|)\b)',
    },
    {
        'model': 'iPhone 11 Pro Max',
        'max-price': '',
        'regex': r'(\b(\w+|\s)11(\s|)pro(\s|)(max|mx)\b)',
        # 'regex': r'(\b 11 pro max\b)|([\s]|)(\b 11pro (max|mx)\b)'
        # |(\b 11 pro max\b)
        # (\b 11 pro (max|mx)\b)|(\b 11pro (max|mx)\b)|(\b\w+11pro\b)
        # |(\b\w+11pro (max|mx)\b)
    },
    {
        'model': 'iPhone SE',
        'max-price': '',
        'regex': r'(\b(iphone)(|\s)se(|\s)\b)'
    },
    {
        'model': 'iPhone 12',
        'max-price': '',
        'regex': r'(\b(\w+|\s)12(|\s)\b)',
    },
    {
        'model': 'iPhone 12 mini',
        'max-price': '',
        'regex': r'(\b(\w+|\s)12(|\s)mini(|\s)\b)'
    },
    {
        'model': 'iPhone 12 Pro',
        'max-price': '',
        'regex': r'(\b(\w+|\s)12(\s|)pro(\s|)\b)',
    },
    {
        'model': 'iPhone 12 Pro Max',
        'max-price': '',
        'regex': r'(\b(\w+|\s)12(\s|)pro(\s|)(max|mx)\b)',
    },
    {
        'model': 'iPhone 13',
        'max-price': '',
        'regex': r'(\b(\w+|\s)13(|\s)\b)',
    },
    {
        'model': 'iPhone 13 mini',
        'max-price': '',
        'regex': r'(\b(\w+|\s)13(|\s)mini(|\s)\b)'
    },
    {
        'model': 'iPhone 13 Pro',
        'max-price': '',
        'regex': r'(\b(\w+|\s)13(\s|)pro(\s|)\b)',
    },
    {
        'model': 'iPhone 13 Pro Max',
        'max-price': '',
        # 'regex': r'(\b(\w+|\s)13(\s|)pro(\s|)(max|mx)\b)',
        'regex': r'(\b(\w+|\s)13(\s|)(pro|pr0|ppro|pr00|)(\s|)(max|mx)\b)',
    },
]
MA_FAKE_DATA = []
AVITO_FAKE_DATA = []


def CHROME_OPTIONS():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    return options


# SMTP
SMTP_PORT = 587
SMTP_HOST = 'smtp.gmail.com'
SMTP_FROM = 'evenma.org@gmail.com'
SMTP_TO = 'mspeedy733@gmail.com'
SMTP_PASSWORD = 'evenm@ssdlv'
SMTP_SUBJECT = 'ANNOUNCES DATA FROM SCRAPING'
SMTP_BODY = body = """\
           Bonjour
           
           Merci de trouver ci-joint un fichier csv contenant les données demandés."""

# CSV
CSV_HEADER = ['Title', 'Price', 'Date', 'City', 'Source']

