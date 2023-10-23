import os
from dotenv import load_dotenv

DOMAINS = {
    "wm": os.getenv("WALMART_DOMAIN"),
    "meli": os.getenv("MELI_DOMAIN"),
    "az": os.getenv("AMAZON_DOMAIN")
}

def get_domains(keywords):
    domains = [DOMAINS.get(keyword) for keyword in keywords if keyword in DOMAINS]
    return domains
