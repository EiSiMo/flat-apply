from actions import *
from language import _
from classes.application_result import ApplicationResult
from providers._provider import Provider
from settings import *

class Gewobag(Provider):
    @property
    def domain(self) -> str:
        return "www.gewobag.de"

    async def apply_for_flat(self, url) -> ApplicationResult:
        async with open_page(url) as page:
            cookie_accept_btn = page.get_by_text("Alle Cookies akzeptieren")
            if await cookie_accept_btn.is_visible():
                await cookie_accept_btn.click()

            await page.wait_for_timeout(2000)

            # 1. check if the ad is still open
            if await page.locator('#immo-mediation-notice').isVisible():
                return ApplicationResult(
                    success=False,
                    message=_("ad_deactivated"))

            return ApplicationResult(False, _("todo_association"))

if __name__ == "__main__":
    url = "https://www.gewobag.de/fuer-mietinteressentinnen/mietangebote/0100-02512-0104-0090/"
    provider = Gewobag()
    provider.test_apply(url)
