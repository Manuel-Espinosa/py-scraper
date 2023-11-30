import os
import requests
import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
logging.basicConfig(level=logging.INFO)


tracker_url = os.getenv("TRACKER_URL")

def get_meli_prices(driver):
    xpaths = {
        "actual_price": '//div[@class="ui-pdp-price__second-line"]//span[@class="andes-money-amount__fraction"]',
        "original_price": '//s[@class="andes-money-amount ui-pdp-price__part ui-pdp-price__original-value andes-money-amount--previous andes-money-amount--cents-superscript andes-money-amount--compact"]//span[@class="andes-money-amount__fraction"]'
    }
    
    actual_price_element = driver.find_element(By.XPATH, xpaths["actual_price"])
    
    try:
        original_price_element = driver.find_element(By.XPATH, xpaths["original_price"])
        original_price = original_price_element.text
    except NoSuchElementException:
        original_price = None
    
    actual_price = actual_price_element.text
    
    prices = {
        "actual_price": actual_price,
        "original_price": original_price
    }
    
    return prices

def get_meli_prices_from_tracker(id):
    payload = ""
    headers = {}
    url = f"{tracker_url}{id}/prices"
    response = requests.request("GET", url, data=payload, headers=headers)
    try:
        response_data = response.json()
        logging.info(f"prices from tracker: {response_data}")
    except ValueError:
        logging.error("Invalid JSON response from tracker")
    return