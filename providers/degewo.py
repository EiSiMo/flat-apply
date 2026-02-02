from actions import *
from language import _
from classes.application_result import ApplicationResult
from providers._provider import Provider
from settings import *
import logging

logger = logging.getLogger("flat-apply")

class Degewo(Provider):
    @property
    def domain(self) -> str:
        return "www.degewo.de"

    async def apply_for_flat(self, url) -> ApplicationResult:
        async with open_page(url) as page:
            logger.info("\tSTEP 1: accepting cookies")
            if await page.locator("#cookie-consent-submit-all").is_visible():
                await page.locator("#cookie-consent-submit-all").click()
                logger.debug("\t\tcookie accept button clicked")
            else:
                logger.debug("\t\tno cookie accept button found")

            logger.info("\tSTEP 2: check if the page was not found")
            if page.url == "https://www.degewo.de/immosuche/404":
                logger.debug("\t\t'page not found' message found - returning")
                return ApplicationResult(
                    success=False,
                    message=_("ad_offline"))
            logger.debug("\t\t'page not found' message not found")

            logger.info("\tSTEP 3: check if the ad is deactivated")
            if await page.locator("span", has_text="Inserat deaktiviert").is_visible():
                logger.debug("\t\t'ad deactivated' message found - returning")
                return ApplicationResult(
                    success=False,
                    message=_("ad_deactivated"))
            logger.debug("\t\t'ad deactivated' message not found")

            logger.info("\tSTEP 4: check if the page moved")
            if await page.locator("h1", has_text="Diese Seite ist umgezogen!").is_visible():
                logger.debug("\t\t'page moved' message found - returning")
                return ApplicationResult(
                    success=False,
                    message=_("ad_offline"))
            logger.debug("\t\t'page moved' message not found")


            logger.info("\tSTEP 5: go to the application form")
            await page.get_by_role("link", name="Kontakt").click()

            logger.info("\tSTEP 6: find the form iframe")
            form_frame = page.frame_locator("iframe[src*='wohnungshelden']")

            logger.info("\tSTEP 7: fill the form")
            await form_frame.locator("#salutation").fill(SALUTATION)
            await form_frame.get_by_role("option", name=SALUTATION, exact=True).click()
            await form_frame.locator("#firstName").fill(FIRSTNAME)
            await form_frame.locator("#lastName").fill(LASTNAME)
            await form_frame.locator("#email").fill(EMAIL)
            await form_frame.locator("input[title='Telefonnummer']").fill(TELEPHONE)
            await form_frame.locator("input[title='Anzahl einziehende Personen']").fill(str(PERSON_COUNT))
            await page.wait_for_timeout(1000)
            if IS_POSSESSING_WBS:
                await form_frame.locator("input[id*='wbs_available'][id$='Ja']").click()
            else:
                await form_frame.locator("input[id*='wbs_available'][id$='Nein']").click()
            await form_frame.locator("input[title='WBS gültig bis']").fill(WBS_VALID_TILL.strftime("%d.%m.%Y"))
            await page.wait_for_timeout(1000)
            wbs_rooms_select = form_frame.locator("ng-select[id*='wbs_max_number_rooms']")
            await wbs_rooms_select.click()
            await page.wait_for_timeout(1000)
            correct_wbs_room_option = form_frame.get_by_role("option", name=str(WBS_ROOMS), exact=True)
            await correct_wbs_room_option.click()
            await page.wait_for_timeout(1000)
            await form_frame.locator("ng-select[id*='fuer_wen_ist_wohnungsanfrage']").click()
            await page.wait_for_timeout(1000)
            await form_frame.get_by_role("option", name="Für mich selbst").click()

            logger.info("\tSTEP 8: submit the form")
            if not SUBMIT_FORMS:
                logger.debug(f"\t\tdry run - not submitting")
                return ApplicationResult(success=True, message=_("application_success_dry"))
            await form_frame.locator("button[data-cy*='btn-submit']").click()
            await page.wait_for_timeout(3000)

            logger.info("\tSTEP 9: check the success")
            if await page.locator("h4", has_text="Vielen Dank für das Übermitteln Ihrer Informationen. Sie können dieses Fenster jetzt schließen.").is_visible():
                logger.info(f"\t\tsuccess detected by heading")
                return ApplicationResult(success=True)
            elif await self.is_missing_fields_warning(page):
                logger.warning(f"\t\tmissing fields warning detected")
                return ApplicationResult(success=False, message=_("missing_fields"))
            elif await self.is_already_applied_warning(page):
                logger.warning(f"\t\talready applied warning detected")
                return ApplicationResult(success=False, message=_("already_applied"))
            logger.warning(f"\t\tsubmit conformation not found")
            return ApplicationResult(success=False, message=_("submit_conformation_msg_not_found"))

    async def is_already_applied_warning(self, page):
        form_iframe = page.frame_locator("iframe[src*='wohnungshelden']")
        already_applied_warning = form_iframe.locator("span.ant-alert-message",
                                                has_text="Es existiert bereits eine Anfrage mit dieser E-Mail Adresse")
        if await already_applied_warning.first.is_visible():
            return True
        return False

    async def is_missing_fields_warning(self, page):
        form_iframe = page.frame_locator("iframe[src*='wohnungshelden']")
        already_applied_warning = form_iframe.locator("span.ant-alert-message",
                                                      has_text="Es wurden nicht alle Felder korrekt befüllt. Bitte prüfen Sie ihre Eingaben")
        if await already_applied_warning.first.is_visible():
            return True
        return False

if __name__ == "__main__":
    # url = "https://www.degewo.de/immosuche/details/neubau-mit-wbs-140-160-180-220-mit-besonderem-wohnbedarf-1" # already applied
    # url = "https://www.degewo.de/immosuche/details/wohnung-sucht-neuen-mieter-1" # angebot geschlossen
    # url = "https://www.degewo.de/immosuche/details/wohnung-sucht-neuen-mieter-145" # seite nicht gefunden
    url = "https://www.degewo.de/immosuche/details/1-zimmer-mit-balkon-3"
    provider = Degewo()
    provider.test_apply(url)

