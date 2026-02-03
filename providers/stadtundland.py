from actions import *
from language import _
from classes.application_result import ApplicationResult
from providers._provider import Provider
from settings import *
import logging

logger = logging.getLogger("flat-apply")

class Stadtundland(Provider):
    @property
    def domain(self) -> str:
        return "stadtundland.de"

    async def apply_for_flat(self, url) -> ApplicationResult:
        async with open_page(url) as page:
            logger.info("\tSTEP 1: accepting cookies")
            cookie_accept_btn = page.get_by_text("Alle akzeptieren")
            if await cookie_accept_btn.is_visible():
                await cookie_accept_btn.click()
                logger.debug("\t\tcookie accept button clicked")
            else:
                logger.debug("\t\tno cookie accept button found")

            logger.info("\tSTEP 2: check if ad is still open")
            if await page.get_by_role("heading", name="Hier ist etwas schief gelaufen").is_visible():
                logger.debug("\t\tsomething went wrong notice found - returning")
                return ApplicationResult(
                    success=False,
                    message=_("ad_offline"))
            logger.debug("\t\tsomething went wrong notice not found")

            logger.info("\tSTEP 3: fill the form")
            await page.locator("#name").fill(FIRSTNAME)
            await page.locator("#surname").fill(LASTNAME)
            await page.locator("#street").fill(STREET)
            await page.locator("#houseNo").fill(HOUSE_NUMBER)
            await page.locator("#postalCode").fill(POSTCODE)
            await page.locator("#city").fill(CITY)
            await page.locator("#phone").fill(TELEPHONE)
            await page.locator("#email").fill(EMAIL)
            await page.locator("#privacy").check()
            await page.locator("#provision").check()

            logger.info("\tSTEP 4: submit the form")
            if not SUBMIT_FORMS:
                logger.debug(f"\t\tdry run - not submitting")
                return ApplicationResult(False, _("application_success_dry"))
            await page.get_by_role("button", name="Eingaben prüfen").click()
            await page.get_by_role("button", name="Absenden").click()
            await page.wait_for_timeout(2000)

            logger.info("\tSTEP 5: check the success")
            if await page.locator("p").filter(has_text="Vielen Dank!").is_visible():
                logger.info(f"\t\tsuccess detected by paragraph text")
                return ApplicationResult(True)
            logger.warning(f"\t\tsuccess message not found")
            return ApplicationResult(success=False, message=_("submit_conformation_msg_not_found"))


if __name__ == "__main__":
    # url = "https://stadtundland.de/wohnungssuche/1001%2F0203%2F00310" # offline
    url = "https://stadtundland.de/wohnungssuche/1050%2F8222%2F00091" # wbs
    provider = Stadtundland()
    provider.test_apply(url)
