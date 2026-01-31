from actions import *
from language import _
from classes.application_result import ApplicationResult
from providers._provider import Provider
from settings import *
import logging

logger = logging.getLogger("flat-apply")


class Wbm(Provider):
    @property
    def domain(self) -> str:
        return "www.wbm.de"

    async def apply_for_flat(self, url) -> ApplicationResult:
        async with open_page(url) as page:
            await page.get_by_text("Alle zulassen").click()
            await page.locator('#removeConvaiseChat').click()
            if page.url == "https://www.wbm.de/wohnungen-berlin/angebote/":
                return ApplicationResult(
                    success=False,
                    message=_("ad_offline"))
            await page.locator('.openimmo-detail__contact-box-button').click()
            if IS_POSSESSING_WBS:
                await page.locator('label[for="powermail_field_wbsvorhanden_1"]').click()
            else:
                await page.locator('label[for="powermail_field_wbsvorhanden_2"]').click()
            await page.locator("input[name*='[wbsgueltigbis]']").fill(WBS_VALID_TILL.strftime("%Y-%m-%d"))
            await page.locator("select[name*='[wbszimmeranzahl]']").select_option(str(WBS_ROOMS))
            await page.locator("#powermail_field_einkommensgrenzenacheinkommensbescheinigung9").select_option(WBS_TYPE)
            if IS_POSSESSING_WBS:
                await page.locator("#powermail_field_wbsmitbesonderemwohnbedarf_1").check(force=True)
            await page.locator("#powermail_field_anrede").select_option(SALUTATION)
            await page.locator("#powermail_field_name").fill(LASTNAME)
            await page.locator("#powermail_field_vorname").fill(FIRSTNAME)
            await page.locator("#powermail_field_strasse").fill(STREET)
            await page.locator("#powermail_field_plz").fill(POSTCODE)
            await page.locator("#powermail_field_ort").fill(CITY)
            await page.locator("#powermail_field_e_mail").fill(EMAIL)
            await page.locator("#powermail_field_telefon").fill(TELEPHONE)
            await page.locator("#powermail_field_datenschutzhinweis_1").check(force=True)
            if not SUBMIT_FORMS:
                return ApplicationResult(success=True, message=_("application_success_dry"))
            await page.get_by_role("button", name="Anfrage absenden").click()
            if await page.get_by_text("Wir haben Ihre Anfrage für das Wohnungsangebot erhalten.").is_visible():
                return ApplicationResult(True)
            return ApplicationResult(success=False, message=_("submit_conformation_msg_not_found"))



if __name__ == "__main__":
    url = "https://www.wbm.de/wohnungen-berlin/angebote/details/4-zimmer-wohnung-in-spandau-1/"
    provider = Wbm()
    provider.test_apply(url)
