from bs4 import BeautifulSoup
import requests
import logging
import os
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

DOMAINS = {
    "wm": os.getenv("WM_DOMAIN"),
    "meli": os.getenv("MELI_DOMAIN"),
    "az": os.getenv("AZ_DOMAIN")
}


def scrape_website(domain, prompt):
    logger.info(f'Domain: "{domain}", prompt="{prompt}"')

    search_url = get_search_url(domain, prompt)
    if not search_url:
        return []
    
    logger.info(f'search url: "{search_url}"')
  
    response = requests.get(search_url)

    soup = BeautifulSoup(response.content, 'html.parser')
    
    function_map = {
        DOMAINS["meli"]: find_all_in_meli,
        DOMAINS["az"]: find_all_in_amazon,
        DOMAINS["wm"]: find_all_in_walmart
    }
    
    return function_map.get(domain, lambda x: [])(soup,prompt)


def get_search_url(domain, prompt):
    if "mercadolibre.com.mx" in domain:
        return construct_meli_search_url(domain, prompt)
    return None

def construct_meli_search_url(domain, prompt):
    search_phrase = prompt.replace(" ", "-")
    encoded_phrase = prompt.replace(" ", "%20")
    return f'{domain}/{search_phrase}#D[A:{encoded_phrase}]'

def construct_amazon_search_url(domain, prompt):
    search_phrase = prompt.replace(" ", "+")
    language_parameter = "&__mk_es_MX=%C3%85M%C3%85%C5%BD%C3%95%C3%91"
    return f'{domain}/s?k={search_phrase}{language_parameter}'

def construct_walmart_search_url(domain, prompt):
    search_phrase = prompt.replace(" ", "+")
    return f'{domain}/search?q={search_phrase}'


def find_all_in_meli(soup,prompt):
    # Look for specific product divs based on a class unique to Mercado Libre
    product_divs = soup.find_all('div', class_='ui-search-result__wrapper')
    
    results = []

    for div in product_divs:
        # Extract the product title and href link from the anchor tag
        a_tag = div.find('a', class_='ui-search-item__group__element ui-search-link')
        if not a_tag:
            continue
        
        product_title = a_tag.get('title', '').strip()
        product_link = a_tag.get('href', '')

        # Check if the prompt partially matches the product title (case-insensitive)
        if prompt.lower() not in product_title.lower():
            continue

        # Extract the price from the span tag
        price_span = div.find('span', class_='andes-money-amount__fraction')
        if not price_span:
            continue
        
        try:
            price = int(price_span.text.replace(',', '').strip())
        except ValueError:
            continue

        # Append the product details to results
        results.append({
            "product": product_title,
            "price": price,
            "link": product_link,
            "source": "meli"
        })

    return results



def find_all_in_amazon(soup):
    # define  html tags
    products = soup.find_all('div', class_='some-class-specific-to-amazon')
    return products

def find_all_in_walmart(soup):
    # define  html tags
    products = soup.find_all('div', class_='some-class-specific-to-walmart')
    return products
