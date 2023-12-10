from bs4 import BeautifulSoup
import requests
import logging
import os
from dotenv import load_dotenv
import re
from usecases.use_browser import apply_meli_price_filters
import aiohttp




# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

DOMAINS = {
    "wm": os.getenv("WALMART_DOMAIN"),
    "meli": os.getenv("MELI_DOMAIN"),
    "az": os.getenv("AMAZON_DOMAIN")
}


async def scrape_website(domain, prompt, price_range):
    logger.info(f'Domain: "{domain}", prompt="{prompt}"')

    search_url = await get_search_url(domain, prompt, price_range)
    logging.info(f"search_url: %s",search_url)
    if not search_url:
        return []

    logger.info(f'search url: "{search_url}"')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Use aiohttp to make an asynchronous GET request
    async with aiohttp.ClientSession() as session:
        async with session.get(search_url, headers=headers) as response:
            response_status = response.status
            content = await response.read()

    logger.info(f'Response Status Code: {response_status}')
    logger.info(f'Response Content Length: {len(content)}')

    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    function_map = {
        DOMAINS["meli"]: find_all_in_meli,
        DOMAINS["az"]: find_all_in_amazon,
        DOMAINS["wm"]: find_all_in_walmart
    }

    # Extract the appropriate function from the map and then await its call
    scraping_function = function_map.get(domain, lambda soup, prompt, domain: [])
    result = await scraping_function(soup, prompt, domain)

    return result



async def get_search_url(domain, prompt,price_range):
    if DOMAINS["meli"] in domain:
        return await construct_meli_search_url(domain, prompt,price_range)
    elif DOMAINS["wm"] in domain:
        return await construct_walmart_search_url(domain,prompt,price_range)
    return None


async def construct_meli_search_url(domain, prompt,price_range):
    #TODO: import and use a selenium function to apply range price filter an return a search url with the filter applied
    search_phrase = prompt.replace(" ", "-")
    encoded_phrase = prompt.replace(" ", "%20")
    search_url = f'{domain}/{search_phrase}#D[A:{encoded_phrase}]'
    logging.info(f"search_url in constructor %s: ",search_url)
    search_url_with_filters = await apply_meli_price_filters(price_range[0],price_range[1],search_url)
    return search_url_with_filters

async def construct_amazon_search_url(domain, prompt):
    search_phrase = prompt.replace(" ", "+")
    language_parameter = "&__mk_es_MX=%C3%85M%C3%85%C5%BD%C3%95%C3%91"
    return f'{domain}/s?k={search_phrase}{language_parameter}'

async def construct_walmart_search_url(domain, prompt, price_range):
    search_phrase = prompt.replace(" ", "+")
    return f'{domain}/search?q={search_phrase}&min_price={price_range[0]}&max_price{price_range[1]}'


async def find_all_in_meli(soup, prompt,domain):
    # Find the specific section
    search_section = soup.select_one('section.ui-search-results.ui-search-results--without-disclaimer')
    
    if not search_section:
        return []

    # Find the ordered list within the section
    ol_tag = search_section.select_one('ol.ui-search-layout.ui-search-layout--stack')

    if not ol_tag:
        return []

    # Find all list items within the ordered list
    li_tags = ol_tag.select('li.ui-search-layout__item')


    item_ids = []
    for li in li_tags:
        # Find the hidden input element for item ID
        item_id_input = li.select_one('input[type="hidden"][name="itemId"]')
        if item_id_input:
            item_id = item_id_input.get('value', '').strip()
            item_ids.append(item_id)

    return item_ids

async def find_all_in_amazon(soup):
    # define  html tags
    products = soup.find_all('div', class_='some-class-specific-to-amazon')
    return products

async def find_all_in_walmart(soup, prompt,domain):
    logging.info('finding in walmart')
    # Get all product divs
    product_divs = soup.find_all('div', class_='mb0 ph1 pa0-xl bb b--near-white w-25')
    logging.info(f'finding divs walmart %s', product_divs)

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
        logging.info(f'product: %s', {
            'name': name,
            'price': price_value,
            'link': link,
            'image': image_url,
            "source": "walmart"
        })

        products.append({
            'name': name,
            'price': price_value,
            'link': link,
            'image': image_url,
            "source": "walmart"
        })

    return products