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

            # 1. check if the ad is still open
            if page.url == "https://www.degewo.de/immosuche/404":
                return ApplicationResult(
                    success=False,
                    message=_("ad_offline"))

            elif await page.locator("span", has_text="Inserat deaktiviert").is_visible():
                return ApplicationResult(
                    success=False,
                    message=_("ad_deactivated"))

            # 2. accept cookies
            if await page.locator("#cookie-consent-submit-all").is_visible():
                await page.locator("#cookie-consent-submit-all").click()

            # 3. click contact
            await page.get_by_role("link", name="Kontakt").click()

            # 4. fill the form
            # 4.1 find the frame
            form_frame = page.frame_locator("iframe[src*='wohnungshelden']")
            # 4.2 fill salutation
            assert SALUTATION in ["Herr", "Frau", "Keine"]
            await form_frame.locator("#salutation").click()
            await form_frame.locator("#salutation").fill(SALUTATION)
            await form_frame.get_by_role("option", name=SALUTATION, exact=True).click()
            # 4.3 basic form fields
            await form_frame.locator("#firstName").fill(FIRSTNAME)
            await form_frame.locator("#lastName").fill(LASTNAME)
            await form_frame.locator("#email").fill(EMAIL)
            await form_frame.locator("#applicant-message").fill(MESSAGE)
            await form_frame.locator("input[title='Telefonnummer']").fill(TELEPHONE)#Anzahl einziehende Personen
            await form_frame.locator("input[title='Anzahl einziehende Personen']").fill(str(PERSON_COUNT))

            await page.wait_for_timeout(1000)

            # WBS forms
            if IS_POSSESSING_WBS:
                await form_frame.locator("input[id*='wbs_available'][id$='Ja']").click()
            else:
                await form_frame.locator("input[id*='wbs_available'][id$='Nein']").click()
            await form_frame.locator("input[title='WBS gültig bis']").fill(WBS_VALID_TILL.strftime("%d.%m.%Y"))

            await page.wait_for_timeout(1000)

            wbs_rooms_select = form_frame.locator("ng-select[id*='wbs_max_number_rooms']")
            await wbs_rooms_select.click()
            correct_wbs_room_option = form_frame.get_by_role("option", name=str(WBS_ROOMS), exact=True)
            await page.wait_for_timeout(1000)
            await correct_wbs_room_option.click()
            await page.wait_for_timeout(1000)


            # third party form
            await form_frame.locator("ng-select[id*='fuer_wen_ist_wohnungsanfrage']").click()
            await page.wait_for_timeout(1000)
            if not IS_APPLYING_FOR_THIRD:
                await form_frame.get_by_role("option", name="Für mich selbst").click()
            else:
                await form_frame.get_by_role("option", name="Für eine andere Person / einen Dritten").click()
                await page.wait_for_timeout(1000)
                # name of the third person
                await form_frame.locator("input[id*='vorname_anderer_person_von_dritten']").fill(THIRDS_FIRSTNAME)
                await form_frame.locator("input[id*='nachname_anderer_person_von_dritten']").fill(THIRDS_LASTNAME)

            if not SUBMIT_FORMS:
                return ApplicationResult(success=True, message=_("application_success_dry"))

            await form_frame.locator("button[data-cy*='btn-submit']").click()
            await page.wait_for_timeout(3000)
            if await page.locator("h4", has_text="Vielen Dank für das Übermitteln Ihrer Informationen. Sie können dieses Fenster jetzt schließen.").is_visible():
                return ApplicationResult(success=True)
            return ApplicationResult(success=False, message=_("submit_conformation_msg_not_found"))


if __name__ == "__main__":
    url = "https://www.degewo.de/immosuche/details/neubau-mit-wbs-140-160-180-220-mit-besonderem-wohnbedarf-1"
    provider = Degewo()
    provider.test_apply(url)
