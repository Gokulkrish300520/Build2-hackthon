from fastapi import FastAPI
from .api import router as api_router

app = FastAPI()
app.include_router(api_router)

# Existing upload_video endpoint and stubs can be moved here for clarity
