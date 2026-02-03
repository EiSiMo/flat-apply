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
        return "wbm.de"

    async def apply_for_flat(self, url) -> ApplicationResult:
        async with open_page(url) as page:
            logger.info("\tSTEP 1: checking if page not found")
            if await page.get_by_role("heading", name="Page Not Found").is_visible():
                logger.debug("\t\t'page not found' message found - returning")
                return ApplicationResult(
                    success=False,
                    message=_("not_found"))
            logger.debug("\t\t'page not found' message not found")

            logger.info("\tSTEP 2: accepting cookies")
            cookie_accept_btn = page.get_by_text("Alle zulassen")
            if await cookie_accept_btn.is_visible():
                await cookie_accept_btn.click()
                logger.debug("\t\tcookie accept button clicked")
            else:
                logger.debug("\t\tno cookie accept button found")

            logger.info("\tSTEP 3: removing chatbot help icon")
            await page.locator('#removeConvaiseChat').click()

            logger.info("\tSTEP 4: checking if ad is offline")
            if page.url == "https://www.wbm.de/wohnungen-berlin/angebote/":
                logger.debug("\t\t'page not found' url found - returning")
                return ApplicationResult(
                    success=False,
                    message=_("ad_offline"))
            logger.debug("\t\t'page not found' url not found")


            logger.info("\tSTEP 5: go to the application form")
            await page.locator('.openimmo-detail__contact-box-button').click()

            logger.info("\tSTEP 6: filling the application form")
            if IS_POSSESSING_WBS:
                await page.locator('label[for="powermail_field_wbsvorhanden_1"]').click()
                await page.locator("input[name*='[wbsgueltigbis]']").fill(WBS_VALID_TILL.strftime("%Y-%m-%d"))
                await page.locator("select[name*='[wbszimmeranzahl]']").select_option(str(WBS_ROOMS))
                await page.locator("#powermail_field_einkommensgrenzenacheinkommensbescheinigung9").select_option(WBS_TYPE)
                if IS_PRIO_WBS:
                    await page.locator("#powermail_field_wbsmitbesonderemwohnbedarf_1").check(force=True)
            else:
                await page.locator('label[for="powermail_field_wbsvorhanden_2"]').click()

            await page.locator("#powermail_field_anrede").select_option(SALUTATION)
            await page.locator("#powermail_field_name").fill(LASTNAME)
            await page.locator("#powermail_field_vorname").fill(FIRSTNAME)
            await page.locator("#powermail_field_strasse").fill(STREET)
            await page.locator("#powermail_field_plz").fill(POSTCODE)
            await page.locator("#powermail_field_ort").fill(CITY)
            await page.locator("#powermail_field_e_mail").fill(EMAIL)
            await page.locator("#powermail_field_telefon").fill(TELEPHONE)
            await page.locator("#powermail_field_datenschutzhinweis_1").check(force=True)

            logger.info("\tSTEP 7: submit the form")
            if not SUBMIT_FORMS:
                logger.debug(f"\t\tdry run - not submitting")
                return ApplicationResult(success=True, message=_("application_success_dry"))
            await page.get_by_role("button", name="Anfrage absenden").click()

            logger.info("\tSTEP 8: check the success")
            if await page.get_by_text("Wir haben Ihre Anfrage für das Wohnungsangebot erhalten.").is_visible():
                logger.info(f"\t\tsuccess detected by text")
                return ApplicationResult(True)
            elif await self.is_missing_fields_warning(page):
                logger.warning(f"\t\tmissing fields warning detected")
                return ApplicationResult(False, _("missing_fields"))
            else:
                logger.warning(f"\t\tneither missing fields nor success detected")
                return ApplicationResult(success=False, message=_("submit_conformation_msg_not_found"))


    async def is_missing_fields_warning(self, page):
        missing_field_msg = page.get_by_text("Dieses Feld muss ausgefüllt werden!").first
        if await missing_field_msg.first.is_visible():
            return True
        return False



if __name__ == "__main__":
    # url = "https://www.wbm.de/wohnungen-berlin/angebote/details/4-zimmer-wohnung-in-spandau-1/" # not found
    url = "https://www.wbm.de/wohnungen-berlin/angebote/details/wbs-160-180-220-perfekt-fuer-kleine-familien-3-zimmer-wohnung-mit-balkon/"
    provider = Wbm()
    provider.test_apply(url)
