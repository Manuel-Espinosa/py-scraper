from fuzzywuzzy import fuzz
import logging
import re
from googletrans import Translator

logging.basicConfig(level=logging.INFO)

def translate_to_spanish(text):
    translator = Translator()
    translation = translator.translate(text, src='en', dest='es')
    return translation.text

def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text).lower()
    return text

def extract_product_from_compare_text(compare, products):
    compare = preprocess_text(compare)
    # compare = translate_to_spanish(compare)
    logging.info(f"process compare: {compare}")
    best_match = None
    highest_score = 0

    for product in products:
        if product is None:
            continue  
        product_name = preprocess_text(product["product"])
        # product_name = translate_to_spanish(product_name)
        logging.info(f"process product name: {product_name}")
        score = fuzz.token_sort_ratio(product_name, compare)
        logging.info(f"score: {score}")

        if score > highest_score:
            highest_score = score
            best_match = product
            logging.info(f"best_match: {best_match}")

    if highest_score >= 15:
        return best_match
    else:
        return None
