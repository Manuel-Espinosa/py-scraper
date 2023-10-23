import os
from dotenv import load_dotenv

load_dotenv()

DOMAINS = {
    "wm": os.getenv("WM_DOMAIN"),
    "meli": os.getenv("MELI_DOMAIN"),
    "az": os.getenv("AZ_DOMAIN")
}

def get_domains(keywords):
    return [DOMAINS.get(keyword) for keyword in keywords if keyword in DOMAINS]
