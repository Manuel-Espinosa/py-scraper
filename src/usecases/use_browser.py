from frameworks.selenium import (browser,apply_price_filter_in_meli)

async def use_browser(payload):
    products_details = []
    for product in payload:
        detail =  await browser(product["ecommerce"],product["url"])
        products_details.append(detail)

    return products_details

async def apply_meli_price_filters(min_price, max_price,search_url):
    search_url_with_filters = await apply_price_filter_in_meli(min_price, max_price,search_url)
    return search_url_with_filters