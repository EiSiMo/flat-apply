import asyncio
import logging
from rich.console import Console
from rich.logging import RichHandler
from urllib.parse import urlparse

import providers
from language import _
from classes.application_result import ApplicationResult
from telegram import Telegram

from settings import *
from utils import *

def setup_logging():
    logging.basicConfig(
        level=logging.WARNING,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(markup=True, console=Console(width=110))]
    )
    logging.getLogger("flat-apply").setLevel(logging.DEBUG)

logger = logging.getLogger("flat-apply")
setup_logging()


class FlatApplier:
    def __init__(self):
        self.telegram = Telegram()

    def scan_and_apply(self):
        logger.info("checking for new messages")
        messages = self.telegram.check_messages()
        logger.info(f"found {len(messages)} new messages")
        for number, message in enumerate(messages, 1):
            message_text_preview = str_to_preview(message.get('text', ''), 30)
            logger.info(f"{str(number).rjust(2)}: {message_text_preview}")
            url = self.get_apply_url_from_message(message)
            if not url:
                logger.info("\tno url found in message")
                return
            logger.info(f"\turl found in message")
            domain = urlparse(url).netloc.lower()
            logger.info(f"\tdomain {domain} extracted from url")

            if domain not in providers.PROVIDERS:
                logger.warning(f"\tunsupported provider")
                feedback = ApplicationResult(False, message=_("unsupported_association"))
            else:
                try:
                    logger.info(f"\tapplying for flat")
                    provider = providers.PROVIDERS[domain]
                    feedback = asyncio.run(provider.apply_for_flat(url))
                    logger.info(f"\tflat application result: {repr(feedback)}")
                except Exception as e:
                    logger.error(f"error while executing apply script:\n{e}")
                    feedback = ApplicationResult(False, f"Script Error:\n{e}")

            logger.info(f"\tformulating response message")
            response_text = str(feedback)
            logger.info(f"\tsending response message")
            self.telegram.send_message(response_text)


    def get_apply_url_from_message(self, message):
        if not FULL_AUTO_MODE:
            text = message.get("text", "").strip()
            if text.lower() != "bewerben":
                return None
            if "reply_to_message" not in message:
                return None
            message = message["reply_to_message"]

        if "entities" not in message:
            return None

        last_url = None
        for entity in message["entities"]:
            if entity["type"] == "text_link":
                last_url = entity["url"]
        return last_url


if __name__ == "__main__":
    flat_applier = FlatApplier()
    while True:
        flat_applier.scan_and_apply()
