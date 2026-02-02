from actions import *
from language import _
from classes.application_result import ApplicationResult
from providers._provider import Provider
from settings import *
import logging

logger = logging.getLogger("flat-apply")

class Howoge(Provider):
    @property
    def domain(self) -> str:
        return "www.howoge.de"

    async def apply_for_flat(self, url) -> ApplicationResult:
        async with open_page(url) as page:
            logger.info("\tSTEP 1: accepting cookies")
            cookie_accept_btn = page.get_by_role("button", name="Alles akzeptieren")
            if await cookie_accept_btn.is_visible():
                await cookie_accept_btn.click()
                logger.debug("\t\tcookie accept button clicked")
            else:
                logger.debug("\t\tno cookie accept button found")

            logger.info("\tSTEP 2: check if the page was not found")
            if page.url == "https://www.howoge.de/404":
                logger.debug("\t\t'page not found' message found - returning")
                return ApplicationResult(
                    success=False,
                    message=_("not_found"))
            logger.debug("\t\t'page not found' message not found")

            logger.info("\tSTEP 3: go to the application form")
            await page.get_by_role("link", name="Besichtigung anfragen").click()

            logger.info("\tSTEP 4: fill the form")
            await page.get_by_text("Ja, ich habe die Hinweise zum WBS zur Kenntnis genommen.").click()
            await page.get_by_role("button", name="Weiter").click()
            await page.get_by_text("Ja, ich habe den Hinweis zum Haushaltsnettoeinkommen zur Kenntnis genommen.").click()
            await page.get_by_role("button", name="Weiter").click()
            await page.get_by_text("Ja, ich habe den Hinweis zur Bonitätsauskunft zur Kenntnis genommen.").click()
            await page.get_by_role("button", name="Weiter").click()
            await page.locator("#immo-form-firstname").fill(FIRSTNAME)
            await page.locator("#immo-form-lastname").fill(LASTNAME)
            await page.locator("#immo-form-email").fill(EMAIL)

            logger.info("\tSTEP 5: submit the form")
            if not SUBMIT_FORMS:
                logger.debug(f"\t\tdry run - not submitting")
                return ApplicationResult(True, _("application_success_dry"))
            await page.get_by_role("button", name="Anfrage senden").click()

            logger.info("\tSTEP 6: check the success")
            if await page.get_by_role("heading", name="Vielen Dank.").is_visible():
                return ApplicationResult(True)
            return ApplicationResult(False, _("submit_conformation_msg_not_found"))

if __name__ == "__main__":
    # url = "https://www.howoge.de/wohnungen-gewerbe/wohnungssuche/detail/1770-26279-6.html" # not found
    url = "https://www.howoge.de/immobiliensuche/wohnungssuche/detail/1770-27695-194.html"
    provider = Howoge()
    provider.test_apply(url)
