import logging
import sys
from datetime import datetime as dt
from os import getenv
from dotenv import load_dotenv

logger = logging.getLogger("flat-apply")

load_dotenv()

def get_env_or_fail(key: str, default: str = None, required: bool = True) -> str:
    value = getenv(key, default)
    if required and value is None:
        logger.error(f"Missing required environment variable: {key}")
        sys.exit(1)
    return value

def get_bool_env(key: str, default: str = "False", required: bool = True) -> bool:
    return get_env_or_fail(key, default, required).lower() in ("true", "1", "yes", "on")

def get_int_env(key: str, default: str = None, required: bool = True) -> int:
    value_str = get_env_or_fail(key, default, required)
    try:
        return int(value_str)
    except ValueError:
        logger.error(f"Environment variable {key} must be an integer. Got: {value_str}")
        sys.exit(1)

def get_date_env(key: str, fmt: str = "%Y-%m-%d", default: str = None, required: bool = True) -> dt:
    value_str = get_env_or_fail(key, default, required)
    try:
        return dt.strptime(value_str, fmt)
    except ValueError:
        logger.error(f"Environment variable {key} must be a date in format {fmt}. Got: {value_str}")
        sys.exit(1)

# --- General Settings ---
LANGUAGE: str = get_env_or_fail("LANGUAGE", "de", False)

# --- Browser Settings ---
HEADLESS: bool = get_bool_env("HEADLESS", "True", True)
BROWSER_WIDTH: int = get_int_env("BROWSER_WIDTH", "600", False)
BROWSER_HEIGHT: int = get_int_env("BROWSER_HEIGHT", "800", False)
BROWSER_LOCALE: str = get_env_or_fail("BROWSER_LOCALE", "de-DE", False)
POST_SUBMISSION_SLEEP_MS: int = get_int_env("POST_SUBMISSION_SLEEP_MS", "0", False)

# --- Automation Mode ---
FULL_AUTO_MODE: bool = get_bool_env("FULL_AUTO_MODE", "False")
SUBMIT_FORMS: bool = get_bool_env("SUBMIT_FORMS", "False")

# --- Personal Information ---
SALUTATION: str = get_env_or_fail("SALUTATION")
LASTNAME: str = get_env_or_fail("LASTNAME")
FIRSTNAME: str = get_env_or_fail("FIRSTNAME")
EMAIL: str = get_env_or_fail("EMAIL")
TELEPHONE: str = get_env_or_fail("TELEPHONE")
STREET: str = get_env_or_fail("STREET")
HOUSE_NUMBER: str = get_env_or_fail("HOUSE_NUMBER")
POSTCODE: str = get_env_or_fail("POSTCODE")
CITY: str = get_env_or_fail("CITY")

# --- WBS Information ---
IS_POSSESSING_WBS: bool = get_bool_env("IS_POSSESSING_WBS", "False")
WBS_TYPE: str = get_env_or_fail("WBS_TYPE", "0", False)
WBS_VALID_TILL: dt = get_date_env("WBS_VALID_TILL", default="1970-01-01", required=False)
WBS_ROOMS: int = get_int_env("WBS_ROOMS", "0", False)
ADULT_COUNT: int = get_int_env("WBS_ADULTS", "0", False)
CHILDREN_COUNT: int = get_int_env("WBS_CHILDREN", "0", False)
PERSON_COUNT: int = ADULT_COUNT + CHILDREN_COUNT
IS_PRIO_WBS: bool = get_bool_env("IS_PRIO_WBS", "False")

# --- Secrets ---
TELEGRAM_TOKEN: str = get_env_or_fail("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID: int = get_int_env("TELEGRAM_CHAT_ID")
IMMOMIO_EMAIL: str = get_env_or_fail("IMMOMIO_EMAIL", required=False)
IMMOMIO_PASSWORD: str = get_env_or_fail("IMMOMIO_PASSWORD", required=False)

# --- Telegram Settings ---
TELEGRAM_POLLING_TIMEOUT: int = get_int_env("TELEGRAM_POLLING_TIMEOUT", "30", False)

def log_settings():
    logger.debug("--- Settings ---")
    logger.debug(f"LANGUAGE: {LANGUAGE}")
    logger.debug(f"BROWSER_WIDTH: {BROWSER_WIDTH}")
    logger.debug(f"BROWSER_HEIGHT: {BROWSER_HEIGHT}")
    logger.debug(f"BROWSER_LOCALE: {BROWSER_LOCALE}")
    logger.debug(f"POST_SUBMISSION_SLEEP_MS: {POST_SUBMISSION_SLEEP_MS}")
    logger.debug(f"HEADLESS: {HEADLESS}")
    logger.debug(f"FULL_AUTO_MODE: {FULL_AUTO_MODE}")
    logger.debug(f"SUBMIT_FORMS: {SUBMIT_FORMS}")
    logger.debug(f"SALUTATION: {SALUTATION}")
    logger.debug(f"LASTNAME: {LASTNAME}")
    logger.debug(f"FIRSTNAME: {FIRSTNAME}")
    logger.debug(f"EMAIL: {EMAIL}")
    logger.debug(f"TELEPHONE: {TELEPHONE}")
    logger.debug(f"STREET: {STREET}")
    logger.debug(f"HOUSE_NUMBER: {HOUSE_NUMBER}")
    logger.debug(f"POSTCODE: {POSTCODE}")
    logger.debug(f"CITY: {CITY}")
    logger.debug(f"IS_POSSESSING_WBS: {IS_POSSESSING_WBS}")
    logger.debug(f"WBS_TYPE: {WBS_TYPE}")
    logger.debug(f"WBS_VALID_TILL: {WBS_VALID_TILL}")
    logger.debug(f"WBS_ROOMS: {WBS_ROOMS}")
    logger.debug(f"WBS_ADULTS: {ADULT_COUNT}")
    logger.debug(f"WBS_CHILDREN: {CHILDREN_COUNT}")
    logger.debug(f"PERSON_COUNT: {PERSON_COUNT}")
    logger.debug(f"IS_PRIO_WBS: {IS_PRIO_WBS}")
    
    masked_token = f"{TELEGRAM_TOKEN[:4]}...{TELEGRAM_TOKEN[-4:]}" if TELEGRAM_TOKEN and len(TELEGRAM_TOKEN) > 8 else "***"
    logger.debug(f"TELEGRAM_TOKEN: {masked_token}")
    logger.debug(f"TELEGRAM_CHAT_ID: {TELEGRAM_CHAT_ID}")
    logger.debug(f"IMMOMIO_EMAIL: {IMMOMIO_EMAIL}")
    
    masked_password = "***" if IMMOMIO_PASSWORD else "None"
    logger.debug(f"IMMOMIO_PASSWORD: {masked_password}")

    logger.debug(f"TELEGRAM_POLLING_TIMEOUT: {TELEGRAM_POLLING_TIMEOUT}")
