from actions import *
from language import _
from classes.application_result import ApplicationResult
from providers._provider import Provider
from settings import *


class Howoge(Provider):
    @property
    def domain(self) -> str:
        return "www.howoge.de"

    async def apply_for_flat(self, url) -> ApplicationResult:
        async with open_page(url) as page:
            await page.get_by_role("button", name="Alles akzeptieren").click()

            if page.url == "https://www.howoge.de/404":
                return ApplicationResult(
                    success=False,
                    message=_("ad_offline"))

            await page.get_by_role("link", name="Besichtigung anfragen").click()

            await page.get_by_text("Ja, ich habe die Hinweise zum WBS zur Kenntnis genommen.").click()
            await page.get_by_role("button", name="Weiter").click()
            await page.get_by_text("Ja, ich habe den Hinweis zum Haushaltsnettoeinkommen zur Kenntnis genommen.").click()
            await page.get_by_role("button", name="Weiter").click()
            await page.get_by_text("Ja, ich habe den Hinweis zur Bonitätsauskunft zur Kenntnis genommen.").click()
            await page.get_by_role("button", name="Weiter").click()
            await page.locator("#immo-form-firstname").fill(FIRSTNAME)
            await page.locator("#immo-form-lastname").fill(LASTNAME)
            await page.locator("#immo-form-email").fill(EMAIL)
            if not SUBMIT_FORMS:
                return ApplicationResult(True, _("application_success_dry"))
            await page.get_by_role("button", name="Anfrage senden").click()
            if await page.get_by_role("heading", name="Vielen Dank.").is_visible():
                return ApplicationResult(True)
            return ApplicationResult(False, _("submit_conformation_msg_not_found"))

if __name__ == "__main__":
    url = "https://www.howoge.de/wohnungen-gewerbe/wohnungssuche/detail/1770-26279-6.html"
    provider = Howoge()
    provider.test_apply(url)
