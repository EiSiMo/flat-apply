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
        return "www.stadtundland.de"

    async def apply_for_flat(self, url) -> ApplicationResult:
        async with open_page(url) as page:
            await page.get_by_text("Alle akzeptieren").click()
            if await page.get_by_role("heading", name="Hier ist etwas schief gelaufen").is_visible():
                return ApplicationResult(
                    success=False,
                    message=_("ad_offline"))
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

            if not SUBMIT_FORMS:
                return ApplicationResult(False, _("application_success_dry"))
            await page.get_by_role("button", name="Eingaben prüfen").click()
            await page.get_by_role("button", name="Absenden").click()
            await page.wait_for_timeout(2000)
            if await page.locator("p").filter(has_text="Vielen Dank!").is_visible():
                return ApplicationResult(True)
            return ApplicationResult(success=False, message=_("submit_conformation_msg_not_found"))


if __name__ == "__main__":
    url = "https://stadtundland.de/wohnungssuche/1001%2F0203%2F00310"
    provider = Stadtundland()
    provider.test_apply(url)
