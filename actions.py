from contextlib import asynccontextmanager
from playwright.async_api import async_playwright, ViewportSize
from reportlab.pdfgen import canvas

from settings import *
import logging

logger = logging.getLogger("flat-apply")

@asynccontextmanager
async def open_page(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=HEADLESS,
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = await browser.new_context(
            viewport=ViewportSize({
                "width": BROWSER_WIDTH,
                "height": BROWSER_HEIGHT}),
            locale=BROWSER_LOCALE
        )

        page = await context.new_page()

        await page.goto(url)
        await page.wait_for_load_state("networkidle")

        try:
            yield page
        finally:
            await page.wait_for_timeout(POST_SUBMISSION_SLEEP_MS)
            await browser.close()

def create_dummy_pdf():
    logger.info("creating dummy pdf")
    c = canvas.Canvas("DummyPDF.pdf")
    c.drawString(100, 750, "Hello! This is a dummy PDF file.")
    c.save()
