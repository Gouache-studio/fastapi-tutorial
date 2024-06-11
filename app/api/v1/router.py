from fastapi import APIRouter
from app.api.v1.endpoints import items, uploads

router = APIRouter()

router.include_router(items.router, prefix="/items", tags=["items"])
router.include_router(uploads.router, prefix="/upload", tags=["uploads"])