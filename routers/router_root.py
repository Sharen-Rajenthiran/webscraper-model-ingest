from fastapi import APIRouter, HTTPException
from utilities.logging_config import logging
import logging

router = APIRouter()

LOG = logging.getLogger(__name__)

@router.get("/")
def root():
    return {"message": "Hello World"}