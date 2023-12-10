from utils.get_meli_prices import (get_meli_prices, get_meli_prices_from_tracker)
from utils.get_meli_tables import get_meli_tables
from utils.walmart_utils import (get_wm_prices, extract_product_specs,handle_verification_challenge)
import logging
import asyncio
from playwright.async_api import async_playwright

async def browser(ecommerce, url):
    if ecommerce == "meli":
        return await navigate_meli(url)
    elif ecommerce == "wm":
        return await navigate_walmart(url)
    return None

async def init_chrome(search_url):
    try: 
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=["--disable-dev-shm-usage", "--disable-images", "--no-sandbox"])
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(search_url)
            return page
    except Exception as e:
        logging.error(f'An error occurred iniating chrome: {str(e)}')
        return None


async def navigate_meli(url):
    try:
        page = await init_chrome()
        await page.goto(url)
        
        # You can use Playwright's query_selector_all function to find elements by class name
        tables = await page.query_selector_all('.andes-table')
        if not tables:
            tables = await page.query_selector_all('.ui-vpp-striped-specs__table')
        
        # Extracting information from the page using Playwright
        title = await page.query_selector('.ui-pdp-title')
        item_id_input = await page.query_selector('input[name="item_id"]')
        item_id_value = await item_id_input.get_attribute('value') if item_id_input else ''
        
        # Handling prices and other data using Playwright
        prices = get_meli_prices(page)
        try:
            get_meli_prices_from_tracker(item_id_value)
        except:
            pass
        
        # Extracting and transforming tables
        fetched_tables = []
        for table in tables:
            table_html = await table.outer_html()
            fetched_tables.append(table_html)
        
        transformed_tables = meli_tables_to_json_transformed(fetched_tables)
        
        data = {
            'title': await title.text_content(),
            'specs': transformed_tables,
            'prices': prices,
            'url': url,
            'store': 'Mercado Libre'
        }
        await page.close()
        return data

    except Exception as e:
        print(f"Error encountered: {str(e)}")

async def apply_price_filter_in_meli(min_price, max_price, search_url):
    try:
        logging.info(f'search_url: %s', search_url)
        page = await init_chrome(search_url)
        logging.info(f'Navigation successful. Current URL: {page.url}')

        # Fill in the minimum and maximum price inputs
        await page.fill('input[data-testid="Minimum-price"]', str(min_price))
        await page.fill('input[data-testid="Maximum-price"]', str(max_price))

        # Click the apply button
        apply_button = 'button[data-testid="submit-price"]'
        await page.click(apply_button)

        # Wait for navigation or other indication that the filter has been applied
        # This might include waiting for a network response or a change in the page content
        # Example: await page.wait_for_navigation()

        # Get the current URL after applying the filter
        current_url = page.url()
        logging.info(f'current full url: %s', current_url)
        await page.close()
        return current_url
    except Exception as e:
        logging.error(f'An error occurred: {str(e)}')
        return None

async def navigate_walmart(url):
    try:
        url_maincontent = url + '#maincontent'
        page = await init_chrome()
        await page.goto(url_maincontent)
        
        # Check if verification challenge is required
        challenge_required = await handle_verification_challenge(page)
        
        if not challenge_required:
            # Continue with scraping logic using Playwright
            title_element = await page.query_selector('#main-title')
            title = await title_element.text_content()
            prices = get_wm_prices(page)
            specs = extract_product_specs(page)
            product = {
                'title': title,
                'prices': prices,
                'specs': specs,
                'store': 'Walmart',
                'url': url
            }
            await page.close()
            return product 

    except Exception as e:
        print(f"An error occurred scraping product: {str(e)}")

# The rest of your code remains the same

# You'll need to define get_meli_prices, get_meli_prices_from_tracker,
# and other functions used in the code using Playwright as well.
