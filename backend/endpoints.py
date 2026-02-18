from fastapi import APIRouter
from backend.api import router as api_router

endpoints_router = APIRouter()

# Include all routes from api.py
endpoints_router.include_router(api_router)

# You can import endpoints_router in app.py and use app.include_router(endpoints_router)
