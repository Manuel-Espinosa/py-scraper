from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json
import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait




# Configure logging
logging.basicConfig(level=logging.INFO)

def get_wm_prices(driver):
    try:
        # Check if the discount element is present
        discount_element = driver.find_element(By.XPATH, "//div[@class='bg-washed-green br1 pv1 ph1 dib mr2']")
        is_discounted = True
    except NoSuchElementException:
        is_discounted = False
    
    # Log the value of is_discounted
    logging.info(f"is_discounted: {is_discounted}")
    
    if is_discounted:
        try:
            # Find the actual price element by XPath
            actual_price_element = driver.find_element(By.XPATH, "//span[@class='b lh-copy dark-gray f1 mr2 green']//span[@itemprop='price']")
            logging.info(f"actual_price_element: {actual_price_element}")
            actual_price = actual_price_element.text
        except NoSuchElementException:
            actual_price = None
    else:
        try:
            # Find the actual price element without discount by XPath
            actual_price_element = driver.find_element(By.XPATH, "//span[@itemprop='price']")
            logging.info(f"actual_price_element without discount: {actual_price_element}")
            actual_price = actual_price_element.text
        except NoSuchElementException:
            actual_price = None

    # Log the value of actual_price
    logging.info(f"actual_price: {actual_price}")

    if is_discounted:
        try:
            # Find the original price element by XPath
            original_price_element = driver.find_element(By.XPATH, "//span[@class='w_q67L']")
            logging.info(f"original_price_element: {original_price_element}")
            original_price = original_price_element.text
        except NoSuchElementException:
            original_price = None
    else:
        original_price = None
    
    # Log the value of original_price
    logging.info(f"original_price: {original_price}")
    
    prices = {
        "actual_price": actual_price,
        "original_price": original_price
    }
    
    return prices

def extract_product_specs(driver):
    try:
        specs_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "nt1"))
        )
        specs = {}
        spec_elements = specs_container.find_elements_by_xpath(".//div[@class='pb2']")
        logging.info(f"spec_elements: {spec_elements}")
        for spec_element in spec_elements:
            key = spec_element.find_element_by_xpath(".//h3").text.strip()
            value = spec_element.find_element_by_xpath(".//div/span").text.strip()
            specs[key] = value

        product_specs_json = json.dumps(specs, ensure_ascii=False)

        return product_specs_json

    except Exception as e:
        # Log the error message
        logging.error(f"An error occurred getting specs: {str(e)}")

def handle_verification_challenge(driver):
    try:
        # Wait for the verification challenge element to be present
        message = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.ID, 'message'))
        )

        # Check if the message indicates a verification challenge
        if "Mantén presionado el botón para confirmar que no eres un robot." in message.text:
            # Find and interact with the iframe
            iframe = WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='px-captcha']/iframe"))
            )
            driver.switch_to.frame(iframe)
            
            # Perform actions to complete the challenge (click and hold in the iframe)
            challenge_button = WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='px-captcha']"))
            )
            action = ActionChains(driver)
            action.click_and_hold(challenge_button).perform()

            # Wait for the verification to complete (element disappears)
            verification_complete = WebDriverWait(driver, 60).until(
                EC.invisibility_of_element_located((By.XPATH, "//div[@id='px-captcha']"))
            )

            # Switch back to the default content
            driver.switch_to.default_content()

            # Challenge completed, return True
            return True

    except Exception as e:
        # Challenge was not required or couldn't be completed
        return False