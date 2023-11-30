from selenium import webdriver
from utils.get_meli_prices import (get_meli_prices, get_meli_prices_from_tracker)
from utils.get_meli_tables import get_meli_tables
from utils.walmart_utils import (get_wm_prices, extract_product_specs,handle_verification_challenge)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)


def browser(ecommerce,url):
    if ecommerce == "meli":
        return navigate_meli(url)
    elif ecommerce == "wm":
        return navigate_walmart(url)
    return 

def init_chrome():
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--v=1")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_experimental_option('w3c', False)
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def navigate_meli(url):
    try:
        driver = init_chrome()
        driver.get(url)
        wait = WebDriverWait(driver, 5)
        fetched_tables = []
        logging.info(f"Fetching tables directly from the HTML...")
        tables = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'andes-table')))
        if not tables:
            tables = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ui-vpp-striped-specs__table')))
        logging.info(f"tables: {tables}")
        title = driver.find_element(By.CLASS_NAME, 'ui-pdp-title')
        prices = get_meli_prices(driver)
        # Find the input tag with name="item_id" using Selenium
        item_id_input = driver.find_element(By.NAME, 'item_id')

        # Extract the value from the input tag
        item_id_value = item_id_input.get_attribute('value') if item_id_input else ''
        logging.info(f"item_id_value: {item_id_value}")
        get_meli_prices_from_tracker(item_id_value)

        logging.info(f"prices: {prices}")
        if tables:
            print(f"Found {len(tables)} tables.")
            for table in tables:
                fetched_tables.append(table.get_attribute('outerHTML'))
        else:
            logging.info(f"Not tables found")
        transformed_tables = meli_tables_to_json_transformed(fetched_tables)
        
        data = {
            'title': title.text,
            'specs': transformed_tables,
            'prices': prices,
            'url':url,
            'store':'Mercado Libre'
            }
        driver.quit()
        return data

    except Exception as e:
        logging.error(f"Error encountered: {str(e)}", exc_info=True)
        
def meli_tables_to_json_transformed(tables_html):
    """
    Convert list of tables' outerHTML to a JSON structure and then transform the structure.
    """
    result = []

    for index, table_html in enumerate(tables_html):
        soup = BeautifulSoup(table_html, 'html.parser')
        headers = [th.text for th in soup.find_all("th")]
        rows = [[td.text for td in tr.find_all("td")] for tr in soup.find_all("tr")]
        transformed_table = {header: rows[i][0] if i < len(rows) and rows[i] else None for i, header in enumerate(headers)}
        result.append({f"spec_group_{index + 1}": transformed_table})

    logging.info(f"Transformed table data: {result}")
    return result

def apply_price_filter_in_meli(min_price, max_price,search_url):
    driver = init_chrome()
    wait = WebDriverWait(driver, 5)

    driver.get(search_url)
    price_filter_section = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ui-search-filter-groups')))

    min_price_input = price_filter_section.find_element(By.XPATH, './/input[@data-testid="Minimum-price"]')
    max_price_input = price_filter_section.find_element(By.XPATH, './/input[@data-testid="Maximum-price"]')
    apply_button = price_filter_section.find_element(By.XPATH, './/button[@data-testid="submit-price"]')
    
    min_price_input.clear()
    min_price_input.send_keys(str(min_price))
    max_price_input.clear()
    max_price_input.send_keys(str(max_price))
    
    apply_button.click()
    
    wait.until(EC.staleness_of(price_filter_section))
    
    return driver.current_url


def navigate_walmart(url):
    try:
        url_maincontent = url+'#maincontent'
        driver = init_chrome()
        driver.get(url_maincontent)
        
        # Check if verification challenge is required
        challenge_required = handle_verification_challenge(driver)
        logging.info(f"challenge_required: {str(challenge_required)}")
        
        if not challenge_required:
            # Continue with scraping logic
            title_element = driver.find_element(By.ID, 'main-title')
            title = title_element.text
            prices = get_wm_prices(driver)
            specs = extract_product_specs(driver)
            product = {
                'title': title,
                'prices': prices,
                'specs': specs,
                'store': 'Walmart',
                'url':url
            }
            driver.quit()
            return product 

    except Exception as e:
        # Log the error message
        logging.error(f"An error occurred scraping product: {str(e)}")