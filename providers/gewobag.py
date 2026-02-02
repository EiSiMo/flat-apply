from actions import *
from language import _
from classes.application_result import ApplicationResult
from providers._provider import Provider
from settings import *
import logging

logger = logging.getLogger("flat-apply")

class Gewobag(Provider):
    @property
    def domain(self) -> str:
        return "www.gewobag.de"

    async def apply_for_flat(self, url) -> ApplicationResult:
        async with open_page(url) as page:
            logger.info("\tSTEP 1: accepting cookies")
            cookie_accept_btn = page.get_by_text("Alle Cookies akzeptieren")
            if await cookie_accept_btn.is_visible():
                await cookie_accept_btn.click()
                logger.debug("\t\tcookie accept button clicked")
            else:
                logger.debug("\t\tno cookie accept button found")

            logger.info("\tSTEP 2: check if the page was not found")
            if await page.get_by_text("Mietangebot nicht gefunden").first.is_visible():
                logger.debug("\t\t'page not found' message found - returning")
                return ApplicationResult(
                    success=False,
                    message=_("not_found"))
            logger.debug("\t\t'page not found' message not found")


            logger.info("\tSTEP 3: check if ad is still open")
            if await page.locator('#immo-mediation-notice').is_visible():
                logger.debug("\t\tad closed notice found - returning")
                return ApplicationResult(
                    success=False,
                    message=_("ad_deactivated"))
            logger.debug("\t\tno ad closed notice found")

            logger.info("\tSTEP 4: go to the application form")
            await page.get_by_role("button", name="Anfrage senden").first.click()

            logger.info("\tSTEP 5: check if the flat is for seniors only")
            if await self.is_senior_flat(page):
                logger.debug("\t\tflat is for seniors only - returning")
                return ApplicationResult(False, _("senior_flat"))
            logger.debug("\t\tflat is not seniors only")

            logger.info("\tSTEP 6: check if the flat is for special needs wbs only")
            if await self.is_special_needs_wbs(page):
                logger.debug("\t\tflat is for special needs wbs only - returning")
                return ApplicationResult(False, _("special_need_wbs_flat"))
            logger.debug("\t\tflat is not for special needs wbs only")

            logger.info("\tSTEP 7: find the form iframe")
            form_iframe = page.frame_locator("#contact-iframe")

            logger.info("\tSTEP 8: define helper functions")
            async def fill_field(locator, filling):
                logger.debug(f"\t\tfill_field('{locator}', '{filling}')")
                field = form_iframe.locator(locator)
                if await field.is_visible():
                    await field.fill(filling)
                    await page.wait_for_timeout(100)
                else:
                    logger.debug(f"\t\t\tfield was not found")

            async def select_field(locator, selection):
                logger.debug(f"\t\tselect_field('{locator}', '{selection}')")
                field = form_iframe.locator(locator)
                if await field.is_visible():
                    await field.click()
                    await page.wait_for_timeout(100)
                    await form_iframe.get_by_role("option", name=selection, exact=True).click()
                    await page.wait_for_timeout(100)
                else:
                    logger.debug(f"\t\t\tfield was not found")

            async def check_checkbox(locator):
                logger.debug(f"\t\tcheck_checkbox('{locator}')")
                field = form_iframe.locator(locator)
                if await field.first.is_visible():
                    await field.evaluate_all("elements => elements.forEach(el => el.click())")
                    await page.wait_for_timeout(100)
                else:
                    logger.debug(f"\t\t\tfield was not found")

            async def upload_files(locator, files):
                logger.debug(f"\t\tupload_files('{locator}', {str(files)})")
                wbs_upload_section = form_iframe.locator(locator)
                if await wbs_upload_section.count() > 0:
                    await wbs_upload_section.locator("input[type='file']").set_input_files(files)
                    await page.wait_for_timeout(2000)
                else:
                    logger.debug(f"\t\t\tfield was not found")


            logger.info("\tSTEP 9: fill the form")
            await select_field("#salutation-dropdown", SALUTATION)
            await fill_field("#firstName", FIRSTNAME)
            await fill_field("#lastName", LASTNAME)
            await fill_field("#email", EMAIL)
            await fill_field("#phone-number", TELEPHONE)
            await fill_field("#street", STREET)
            await fill_field("#house-number", HOUSE_NUMBER)
            await fill_field("#zip-code", POSTCODE)
            await fill_field("#city", CITY)
            await fill_field("input[id*='anzahl_erwachsene']", str(WBS_ADULTS))
            await fill_field("input[id*='anzahl_kinder']", str(WBS_CHILDREN))
            await fill_field("input[id*='gesamtzahl_der_einziehenden_personen']", str(WBS_ADULTS + WBS_CHILDREN))
            await check_checkbox("[data-cy*='wbs_available'][data-cy*='-Ja']")
            await fill_field("input[id*='wbs_valid_until']", WBS_VALID_TILL.strftime("%d.%m.%Y"))
            await select_field("input[id*='wbs_max_number_rooms']", f"{WBS_ROOMS} Räume")
            await select_field("input[id*='art_bezeichnung_des_wbs']", f"WBS {WBS_TYPE}")
            await select_field("input[id*='fuer_wen']", "Für mich selbst")
            await fill_field("input[id*='telephone_number']", TELEPHONE)
            await check_checkbox("input[id*='datenschutzhinweis']")
            await upload_files("el-application-form-document-upload", ["DummyPDF.pdf"])

            logger.info("\tSTEP 10: submit the form")
            if not SUBMIT_FORMS:
                logger.debug(f"\t\tdry run - not submitting")
                return ApplicationResult(True, _("application_success_dry"))
            await form_iframe.get_by_role("button", name="Anfrage versenden").click()
            await page.wait_for_timeout(5000)

            logger.info("\tSTEP 11: check the success")
            if page.url.startswith("https://www.gewobag.de/daten-uebermittelt/"):
                logger.info(f"\t\tsuccess detected by page url")
                return ApplicationResult(True)
            elif self.is_missing_fields_warning(page):
                logger.warning(f"\t\tmissing fields warning detected")
                return ApplicationResult(False, _("missing_fields"))
            else:
                logger.warning(f"\t\tneither missing fields nor success detected")
                return ApplicationResult(False, _("submit_conformation_msg_not_found"))

    async def is_senior_flat(self, page):
        form_iframe = page.frame_locator("#contact-iframe")
        return await form_iframe.locator("label[for*='mindestalter_seniorenwohnhaus_erreicht']").first.is_visible()

    async def is_special_needs_wbs(self, page):
        form_iframe = page.frame_locator("#contact-iframe")
        return await form_iframe.locator("label[for*='wbs_mit_besonderem_wohnbedarf_vorhanden']").first.is_visible()

    async def is_missing_fields_warning(self, page):
        form_iframe = page.frame_locator("#contact-iframe")
        missing_field_msg = form_iframe.locator("span.ant-alert-message",
                                                has_text="Es wurden nicht alle Felder korrekt befüllt.")
        if await missing_field_msg.first.is_visible():
            return True
        return False

if __name__ == "__main__":
    #url = "https://www.gewobag.de/fuer-mietinteressentinnen/mietangebote/0100-01036-0601-0286-vms1/" # wbs
    #url = "https://www.gewobag.de/fuer-mietinteressentinnen/mietangebote/7100-72401-0101-0011/" # senior
    #url = "https://www.gewobag.de/fuer-mietinteressentinnen/mietangebote/6011-31046-0105-0045/" # more wbs fields
    #url = "https://www.gewobag.de/fuer-mietinteressentinnen/mietangebote/0100-01036-0401-0191/" # special need wbs
    #url = "https://www.gewobag.de/fuer-mietinteressentinnen/mietangebote/0100-02571-0103-0169/"
    url = "https://www.gewobag.de/fuer-mietinteressentinnen/mietangebote/0100-02571-0103-169/" # page not found
    provider = Gewobag()
    provider.test_apply(url)
