import logging

import requests
from settings import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_POLLING_TIMEOUT

logger = logging.getLogger("flat-apply")


class Telegram:
    def __init__(self):
        self.offset = 0

    def check_messages(self):
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"

        params = {
            "timeout": TELEGRAM_POLLING_TIMEOUT,
            "allowed_updates": ["message"],
            "offset": self.offset
        }

        try:
            response = requests.get(url, params=params, timeout=TELEGRAM_POLLING_TIMEOUT+5)
            data = response.json()
            logger.debug(f"raw telegram response: {data}")
        except Exception as e:
            logger.error(f"Network error getting updates: {e}")
            logger.warning(f"network error fetching telegram updates")
            return []
        if not data.get("ok"):
            logger.error(f"Error from Telegram: {data}")
            return []

        messages = list()
        updates = data.get("result", [])
        logger.debug(f"found {len(updates)} updates")
        for update in updates:
            self.offset = update['update_id'] + 1
            if "message" not in update.keys():
                continue
            message = update["message"]
            if message["chat"]["id"] != TELEGRAM_CHAT_ID:
                continue
            messages.append(message)
        logger.debug(f"returning {len(messages)} messages")
        return messages

    def send_message(self, msg):
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }
        try:
            requests.post(url, json=payload, timeout=10)
        except Exception as e:
            logger.error(f"failed to send telegram message: {e}")

    def send_message_reply(self, msg, reply_to_message_id):
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True,
            "reply_to_message_id": reply_to_message_id
        }
        try:
            requests.post(url, json=payload, timeout=10)
        except Exception as e:
            logger.error(f"failed to send telegram message: {e}")
