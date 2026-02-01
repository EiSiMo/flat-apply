from datetime import datetime as dt
from dotenv import load_dotenv
from os import getenv

load_dotenv()

LANGUAGE: str = "de"

BROWSER_WIDTH: int = 600
BROWSER_HEIGHT: int = 800
BROWSER_LOCALE: str = "de-DE"
POST_SUBMISSION_SLEEP_MS: int = 0

FULL_AUTO_MODE: bool = getenv("FULL_AUTO_MODE", "False").lower() in ("true", "1")
SUBMIT_FORMS: bool = getenv("SUBMIT_FORMS", "False").lower() in ("true", "1")
HEADLESS: bool = getenv("HEADLESS", "False").lower() in ("true", "1")

# personal information
SALUTATION: str = "Herr"
LASTNAME: str = "Mustermann"
FIRSTNAME: str = "Max"
EMAIL: str = "max.mustermann@example.com"
MESSAGE: str = "Ich habe großes Interesse an dieser Wohnung!"
TELEPHONE = "0123 45678901"
PERSON_COUNT: int = 2

STREET = "Musterstraße"
HOUSE_NUMBER = "123"
POSTCODE = "12345"
CITY = "Musterstadt"
EMAIL = "max.mustermann@example.com"


# WBS information
IS_POSSESSING_WBS: bool = True
WBS_TYPE: str = "180"
WBS_VALID_TILL: dt = dt(2026, 12, 1)
WBS_ROOMS: int = 2
WBS_ADULTS: int = 2
WBS_CHILDREN: int = 0
IS_PRIO_WBS: bool = False

# applying for another person
IS_APPLYING_FOR_THIRD: bool = True
THIRDS_FIRSTNAME: str = "Maddy"
THIRDS_LASTNAME: str = "Musterfrau"

# secrets
GMAPS_API_KEY = getenv("GMAPS_API_KEY")
TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = int(getenv("TELEGRAM_CHAT_ID"))
BERLIN_WOHNEN_USERNAME = getenv("BERLIN_WOHNEN_USERNAME")
BERLIN_WOHNEN_PASSWORD = getenv("BERLIN_WOHNEN_PASSWORD")
IMMOMIO_EMAIL = getenv("IMMOMIO_EMAIL")
IMMOMIO_PASSWORD = getenv("IMMOMIO_PASSWORD")

# telegram
TELEGRAM_POLLING_TIMEOUT: int = 30