from entities.domain_dictionary import get_domains
from frameworks.web_scraper import scrape_website

def search_in_multiple_domains(prompt, domains_keywords):
    domains = get_domains(domains_keywords)
    all_products = []
    
    for domain in domains:
        products = scrape_website(domain, prompt)
        all_products.extend(products)
        
    return all_products
