from fastapi import HTTPException
from bs4 import BeautifulSoup
import requests
from urllib.error import HTTPError
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from core.config import settings
from utilities.logging_config import logging
import logging

LOG = logging.getLogger(__name__)

URL = settings.ZUS_DRINKWARE_URL

def get_product_names_all(url=URL):
    try:
        page = requests.get(url=url, timeout=10)
    except requests.RequestException as e:
        LOG.error(f"Failed to fetch ZUS drinkware page: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch product page")

    if page.content is None:
        LOG.error("Page content was found empty")
        return []
    
    soup = BeautifulSoup(page.content, "html.parser")

    drinkware_products = list()

    product_span = soup.find_all("span", class_="product-card__title")
    all_product_titles = [product_titles.text for product_titles in product_span]

    for product in all_product_titles:
        drinkware_products.append({
            "product": product
        })
    
    LOG.info(f"Sucessfully retrieved drinkware products. Scraped {len(drinkware_products)} products")

    return drinkware_products

