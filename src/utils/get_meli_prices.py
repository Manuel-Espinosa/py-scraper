import os
import requests
import logging
from playwright.async_api import async_playwright
logging.basicConfig(level=logging.INFO)


tracker_url = os.getenv("TRACKER_URL")

async def get_meli_prices(page):
    actual_price_element = await page.querySelector('//div[@class="ui-pdp-price__second-line"]//span[@class="andes-money-amount__fraction"]')

    try:
        original_price_element = await page.querySelector('//s[@class="andes-money-amount ui-pdp-price__part ui-pdp-price__original-value andes-money-amount--previous andes-money-amount--cents-superscript andes-money-amount--compact"]//span[@class="andes-money-amount__fraction"]')
        original_price = await original_price_element.text_content()
    except Exception:
        original_price = None

    actual_price = await actual_price_element.text_content()

    prices = {
        "actual_price": actual_price,
        "original_price": original_price
    }

    return prices


async def get_meli_prices_from_tracker(id):
    payload = ""
    headers = {}
    url = f"{tracker_url}{id}/prices"
    response = await requests.get(url, data=payload, headers=headers)
    try:
        response_data = await response.json()
        logging.info(f"prices from tracker: {response_data}")
    except ValueError:
        logging.error("Invalid JSON response from tracker")
    return
