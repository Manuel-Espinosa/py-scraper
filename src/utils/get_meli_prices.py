from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

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
