from actions import *
from language import _
from classes.application_result import ApplicationResult
from providers._provider import Provider
from settings import *
import logging

logger = logging.getLogger("flat-apply")

class Gesobau(Provider):
    @property
    def domain(self) -> str:
        return "www.gesobau.de"

    async def apply_for_flat(self, url) -> ApplicationResult:
        async with open_page(url) as page:
            await page.goto("https://tenant.immomio.com/de/auth/login")
            await page.locator('input[name="email"]').fill(IMMOMIO_EMAIL)
            await page.get_by_role("button", name="Anmelden").click()
            await page.locator("#password").fill(IMMOMIO_PASSWORD)
            await page.locator("#kc-login").click()
            await page.goto(url)
            await page.get_by_role("link", name="Jetzt bewerben").click()
            await page.wait_for_timeout(5000)
            await page.get_by_text("Jetzt bewerben").click()
        return ApplicationResult(False, _("todo_association"))


if __name__ == "__main__":
    url = "https://www.gesobau.de/?immo_ref=10-03239-00007-1185"
    provider = Gesobau()
    provider.test_apply(url)
