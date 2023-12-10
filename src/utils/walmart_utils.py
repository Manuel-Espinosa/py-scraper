from playwright.sync_api import Page, ElementHandle
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def get_wm_prices(page: Page):
    try:
        # Check if the discount element is present
        discount_element = page.query_selector("div.bg-washed-green.br1.pv1.ph1.dib.mr2")
        is_discounted = True if discount_element else False
    except Exception:
        is_discounted = False
    
    # Log the value of is_discounted
    logging.info(f"is_discounted: {is_discounted}")
    
    actual_price = None
    original_price = None
    
    if is_discounted:
        try:
            # Find the actual price element by XPath
            actual_price_element = page.query_selector("span.b.lh-copy.dark-gray.f1.mr2.green span[itemprop='price']")
            logging.info(f"actual_price_element: {actual_price_element}")
            actual_price = actual_price_element.inner_text()
        except Exception:
            pass
    else:
        try:
            # Find the actual price element without discount by XPath
            actual_price_element = page.query_selector("span[itemprop='price']")
            logging.info(f"actual_price_element without discount: {actual_price_element}")
            actual_price = actual_price_element.inner_text()
        except Exception:
            pass

    # Log the value of actual_price
    logging.info(f"actual_price: {actual_price}")

    if is_discounted:
        try:
            # Find the original price element by XPath
            original_price_element = page.query_selector("span.w_q67L")
            logging.info(f"original_price_element: {original_price_element}")
            original_price = original_price_element.inner_text()
        except Exception:
            pass
    
    # Log the value of original_price
    logging.info(f"original_price: {original_price}")
    
    prices = {
        "actual_price": actual_price,
        "original_price": original_price
    }
    
    return prices

def extract_product_specs(page: Page):
    try:
        specs_container = page.wait_for_selector("div.nt1")
        specs = {}
        spec_elements = specs_container.query_selector_all("div.pb2")
        logging.info(f"spec_elements: {spec_elements}")
        for spec_element in spec_elements:
            key_element = spec_element.query_selector("h3")
            value_element = spec_element.query_selector("div span")
            if key_element and value_element:
                key = key_element.inner_text().strip()
                value = value_element.inner_text().strip()
                specs[key] = value

        product_specs_json = json.dumps(specs, ensure_ascii=False)

        return product_specs_json

    except Exception as e:
        # Log the error message
        logging.error(f"An error occurred getting specs: {str(e)}")

def handle_verification_challenge(page: Page):
    try:
        # Wait for the verification challenge element to be present
        message = page.wait_for_selector("div#message")
        message_text = message.inner_text()
        
        # Check if the message indicates a verification challenge
        if "Mantén presionado el botón para confirmar que no eres un robot." in message_text:
            # Find and interact with the iframe
            iframe = page.wait_for_selector("div#px-captcha iframe")
            iframe_handle = iframe.content_frame()
            
            # Perform actions to complete the challenge (click and hold in the iframe)
            challenge_button = iframe_handle.query_selector("div#px-captcha")
            #await challenge_button.click()
            #await challenge_button.click_and_hold()

            # Wait for the verification to complete (element disappears)
            #await page.wait_for_selector("div#px-captcha", state="hidden")

            # Challenge completed, return True
            return True

    except Exception as e:
        # Challenge was not required or couldn't be completed
        return False