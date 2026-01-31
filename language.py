import tomllib

from settings import *
from paths import *

with open(TRANSLATIONS_FILE, "rb") as f:
    TRANSLATIONS = tomllib.load(f)

def get_text(message):
    if message not in TRANSLATIONS.keys():
        raise KeyError(f"{message} is not a valid translation.")
    if LANGUAGE not in TRANSLATIONS[message].keys():
        raise KeyError(f"there is no {LANGUAGE} translation for {message}.")
    return TRANSLATIONS[message][LANGUAGE]

_ = get_text