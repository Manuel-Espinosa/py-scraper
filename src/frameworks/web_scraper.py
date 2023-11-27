from bs4 import BeautifulSoup
import requests
import logging
import os
from dotenv import load_dotenv
import re
from usecases.use_browser import apply_meli_price_filters


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

DOMAINS = {
    "wm": os.getenv("WALMART_DOMAIN"),
    "meli": os.getenv("MELI_DOMAIN"),
    "az": os.getenv("AMAZON_DOMAIN")
}


def scrape_website(domain, prompt, price_range):
    logger.info(f'Domain: "{domain}", prompt="{prompt}"')

    search_url = get_search_url(domain, prompt,price_range)
    if not search_url:
        return []
    
    logger.info(f'search url: "{search_url}"')
  
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(search_url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')
    
    function_map = {
        DOMAINS["meli"]: find_all_in_meli,
        DOMAINS["az"]: find_all_in_amazon,
        DOMAINS["wm"]: find_all_in_walmart
    }
    
    return function_map.get(domain, lambda x: [])(soup,prompt,domain)


def get_search_url(domain, prompt,price_range):
    if DOMAINS["meli"] in domain:
        return construct_meli_search_url(domain, prompt,price_range)
    elif DOMAINS["wm"] in domain:
        return construct_walmart_search_url(domain,prompt,price_range)
    return None


def construct_meli_search_url(domain, prompt,price_range):
    #TODO: import and use a selenium function to apply range price filter an return a search url with the filter applied
    search_phrase = prompt.replace(" ", "-")
    encoded_phrase = prompt.replace(" ", "%20")
    search_url = f'{domain}/{search_phrase}#D[A:{encoded_phrase}]'
    search_url_with_filters = apply_meli_price_filters(price_range[0],price_range[1],search_url)
    return search_url_with_filters

def construct_amazon_search_url(domain, prompt):
    search_phrase = prompt.replace(" ", "+")
    language_parameter = "&__mk_es_MX=%C3%85M%C3%85%C5%BD%C3%95%C3%91"
    return f'{domain}/s?k={search_phrase}{language_parameter}'

def construct_walmart_search_url(domain, prompt, price_range):
    search_phrase = prompt.replace(" ", "+")
    return f'{domain}/search?q={search_phrase}&min_price={price_range[0]}&max_price{price_range[1]}'

def find_all_in_meli(soup,prompt,domain):
    # Look for specific product divs based on a class unique to Mercado Libre
    logger.info(f'searching products')

    product_divs = soup.find_all('div', class_='ui-search-result__wrapper')
    logger.info(f'product divs: "{product_divs}"')

    
    results = []

    for div in product_divs:
        # Extract the product title and href link from the anchor tag
        a_tag = div.find('a', class_='ui-search-item__group__element ui-search-link')
        if not a_tag:
            continue
        
        product_title = a_tag.get('title', '').strip()
        product_link = a_tag.get('href', '')

        # Check if the prompt partially matches the product title (case-insensitive)
        #if prompt.lower() not in product_title.lower():
         #   continue
        # Extract the product image src from the img tag
        img_tag = div.find('img', class_='ui-search-result-image__element')
        
        product_image = img_tag.get('data-src', '')
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
            "image": product_image,
            "source": "meli"
        })
        logger.info(f'results: "{results}"')



    return results

def find_all_in_amazon(soup):
    # define  html tags
    products = soup.find_all('div', class_='some-class-specific-to-amazon')
    return products

def find_all_in_walmart(soup, prompt,domain):
    # Get all product divs
    product_divs = soup.find_all('div', class_='mb0 ph1 pa0-xl bb b--near-white w-25')


    # List to store product data
    products = []

    # Iterate through each product div to extract information
    for div in product_divs:
        name_tag = div.find('span', class_="normal dark-gray mb0 mt1 lh-title f6 f5-l lh-copy")
        price_tag = div.find('div', class_="mr1 mr2-xl b black lh-copy f5 f4-l")
        discounted_tag = div.find('div', class_="mr1 mr2-xl b black green lh-copy f5 f4-l")
        a_tag = div.find('a', class_="absolute w-100 h-100 z-1 hide-sibling-opacity")
        image_tag = div.find('img', attrs={'data-testid': 'productTileImage'})

        link = domain + a_tag.get('href', '') if a_tag and 'href' in a_tag.attrs else None
        name = name_tag.text        
        image_url = image_tag.get('src', '') if image_tag else None

            # Extract only the numeric values from the price_tag using regex
        if price_tag:
            price_text = price_tag.text
            # Extract numbers, optional commas, and optional decimal points
            price_matches = re.search(r"(\d{1,3}(?:,\d{3})*(\.\d{1,2})?)", price_text)
            if price_matches:
            # Remove commas and convert to float
                
                price_value = float(price_matches.group(1).replace(',', ''))
            else:
                price_value = None
                
        if discounted_tag:
            price_text = discounted_tag.text
            # Extract numbers, optional commas, and optional decimal points
            price_matches = re.search(r"(\d{1,3}(?:,\d{3})*(\.\d{1,2})?)", price_text)
            if price_matches:
            # Remove commas and convert to float
                
                price_value = float(price_matches.group(1).replace(',', ''))
            else:
                price_value = None


        products.append({
            'name': name,
            'price': price_value,
            'link': link,
            'image': image_url,
            "source": "walmart"
        })

    return products