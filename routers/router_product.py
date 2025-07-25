from fastapi import APIRouter, HTTPException
from utilities.logging_config import logging
import logging
from core.webscraper import get_product_names_all
from core.model_ingest import model

router = APIRouter()

LOG = logging.getLogger(__name__)

@router.get("/products/", tags=["Products"])
def get_products():
    try:
        all_products = get_product_names_all()
    except Exception as e:
        LOG.error("Error getting all products {e}.")
        raise HTTPException(status_code=500, detail="Failed to fetch product page")
    
    if not all_products:
        LOG.info("Empty products list.")
        return []
    
    return all_products

@router.get("/products/search")
def get_products_for_users(user_query: str, top_k: int):
    try:
        results = model.perform_top_k_search(
            user_query=user_query,
            top_k=top_k
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get top k results")
    
    return results if results else []
    
