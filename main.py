from fastapi import FastAPI
import uvicorn
from fastapi.exceptions import HTTPException
from utilities.logging_config import logging
from core.config import settings
import logging
from routers import router_product, router_root

app = FastAPI()
app.include_router(router_product.router)
app.include_router(router_root.router)

LOG = logging.getLogger(__name__)

LOG.info("Starting up...")

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=settings.PORT
    )

