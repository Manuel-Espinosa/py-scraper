import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DOMAINS = {
    "wm": os.getenv("WALMART_DOMAIN"),
    "meli": os.getenv("MELI_DOMAIN"),
    "az": os.getenv("AMAZON_DOMAIN")
}

def get_domains(keywords):
    domains = [DOMAINS.get(keyword) for keyword in keywords if keyword in DOMAINS]
    logger.info(f'get_domains sent : "{domains}""')
    return domains