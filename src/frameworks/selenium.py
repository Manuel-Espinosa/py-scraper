from selenium import webdriver
from utils.get_meli_prices import get_meli_prices
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)


def browser(ecommerce,url):
    if ecommerce == "meli":
        return navigate_meli(url)
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
        logging.info(f"tables: {tables}")
        title = driver.find_element(By.CLASS_NAME, 'ui-pdp-title')
        prices = get_meli_prices(driver)
        logging.info(f"prices: {prices}")
        if tables:
            print(f"Found {len(tables)} tables.")
            for table in tables:
                fetched_tables.append(table.get_attribute('outerHTML'))
        else:
            logging.info(f"Not tables found")
        transformed_tables = meli_tables_to_json_transformed(fetched_tables)
        
        data = {
            'product': title.text,
            'specs': transformed_tables,
            'original_price': prices["original_price"],
            'actual_price': prices["actual_price"],
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
