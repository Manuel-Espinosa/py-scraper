from entities.domain_dictionary import get_domains
from frameworks.web_scraper import scrape_website
import asyncio

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def search_in_multiple_domains(prompt, domains_keywords, price_range):
    logger.info(f'search_in_multiple_domains gots : "{domains_keywords}", prompt="{prompt}"')
    
    domains = get_domains(domains_keywords)
    logger.info(f'get_domains gots : "{domains}""')

    all_products = []

    # Create a list of coroutine objects for the tasks
    tasks = [scrape_website(domain, prompt, price_range) for domain in domains]

    # Use asyncio.gather to await all tasks concurrently
    results = await asyncio.gather(*tasks)

    # Extend the all_products list with the results
    for products in results:
        all_products.extend(products)

    # Filter products within the given price range
    # filtered_products = filter_products_by_price(all_products, price_range)

    return all_products