from entities.domain_dictionary import get_domains
from frameworks.web_scraper import scrape_website

def search_in_multiple_domains(prompt, domains_keywords, price_range):
    """
    Searches for products across multiple domains based on a given prompt and price range.

    Parameters:
    - prompt (str): The search prompt or keyword to look for.
    - domains_keywords (list or iterable): Keywords to determine which domains to scrape.
    - price_range (tuple): A tuple containing the minimum and maximum prices.

    Returns:
    - list: A list of products found across the domains and filtered by the provided price range.
    """
    
    domains = get_domains(domains_keywords)
    all_products = []
    
    for domain in domains:
        products = scrape_website(domain, prompt,price_range)
        all_products.extend(products)
        
    # Filter products within the given price range
    #filtered_products = filter_products_by_price(all_products, price_range)
    
    return all_products

def filter_products_by_price(products, price_range):
    """
    Filters a list of products based on a given price range.

    Parameters:
    - products (list): A list of product dictionaries.
    - price_range (tuple): A tuple containing the minimum and maximum prices.

    Returns:
    - list: A list of products filtered by price.
    """
    min_price, max_price = price_range
    return [product for product in products if min_price <= product["price"] <= max_price]
