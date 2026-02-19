from fastapi import FastAPI
from database.db import engine, Base
from routers import websocket_router, event_router, node_router
from services.heartbeat_service import check_offline_nodes
import threading
import time

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(websocket_router.router)
app.include_router(event_router.router)
app.include_router(node_router.router)

def background_offline_checker():
    while True:
        check_offline_nodes()
        time.sleep(30)

threading.Thread(target=background_offline_checker, daemon=True).start()