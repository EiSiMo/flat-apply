from actions import *
from language import _
from classes.application_result import ApplicationResult
from providers._provider import Provider
from settings import *
import logging

logger = logging.getLogger("flat-apply")

class Gesobau(Provider):
    @property
    def domain(self) -> str:
        return "www.gesobau.de"

    async def apply_for_flat(self, url) -> ApplicationResult:
        async with open_page(url) as page:
            logger.info("\tSTEP 1: extracting immomio link")
            immomio_link = await page.get_by_role("link", name="Jetzt bewerben").get_attribute("href")

            logger.info("\tSTEP 2: going to immomio")
            await page.goto(immomio_link)
            await page.wait_for_timeout(1000)

            logger.info("\tSTEP 3: accepting cookies")
            cookie_accept_btn = page.get_by_role("button", name="Alle erlauben")
            if await cookie_accept_btn.is_visible():
                await cookie_accept_btn.click()
                logger.debug("\t\tcookie accept button clicked")
            else:
                logger.debug("\t\tno cookie accept button found")

            logger.info("\tSTEP 4: clicking apply now")
            await page.get_by_role("button", name="Jetzt bewerben").click()
            await page.wait_for_timeout(1000)

            logger.info("\tSTEP 5: clicking login")
            await page.get_by_role("button", name="Anmelden").click()
            await page.wait_for_timeout(1000)

            logger.info("\tSTEP 6: logging in")
            await page.locator('input[name="email"]').fill(IMMOMIO_EMAIL)
            await page.get_by_role("button", name="Anmelden").click()
            await page.wait_for_timeout(1000)
            await page.locator("#password").fill(IMMOMIO_PASSWORD)
            await page.locator("#kc-login").click()
            await page.wait_for_timeout(1000)

            logger.info("\tSTEP 7: going back to immomio")
            await page.goto(immomio_link)
            await page.wait_for_timeout(1000)

            logger.info("\tSTEP 8: click apply now")
            await page.get_by_role("button", name="Jetzt bewerben").click()
            await page.wait_for_timeout(3000)

            logger.info("\tSTEP 9: check if already applied")
            if page.url == "https://tenant.immomio.com/de/properties/applications":
                return ApplicationResult(False, message=_("already_applied"))

            logger.info("\tSTEP 10: clicking answer questions")
            answer_questions_btn = page.get_by_role("button", name="Fragen beantworten")
            if await answer_questions_btn.is_visible():
                await answer_questions_btn.click()
                logger.debug("\t\tanswer questions button clicked")
                await page.wait_for_timeout(2000)
            else:
                logger.debug("\t\tno answer questions button found")

            if await answer_questions_btn.is_visible():  # sometimes this button must be clicked twice
                await answer_questions_btn.click()
                logger.debug("\t\tanswer questions button clicked")
                await page.wait_for_timeout(2000)


            logger.info("\tSTEP 11: verifying success by answer button vanishing")
            if not await answer_questions_btn.is_visible(): # TODO better verify success
                logger.info("\t\tsuccess detected by answer button vanishing")
                return ApplicationResult(True)

        logger.info("\t\tsubmit conformation not found")
        return ApplicationResult(False, _("submit_conformation_msg_not_found"))


if __name__ == "__main__":
    # url = "https://www.gesobau.de/?immo_ref=10-03239-00007-1185" # already applied
    url = "https://www.gesobau.de/mieten/wohnungssuche/detailseite/florastrasse-10-12179-00002-1002-1d4d1a94-b555-48f8-b06d-d6fc02aecb0d/"
    url = "https://www.gesobau.de/mieten/wohnungssuche/detailseite/rolandstrasse-10-03020-00007-1052-7f47d893-e659-4e4f-a7cd-5dcd53f4e6d7/"
    provider = Gesobau()
    provider.test_apply(url)
