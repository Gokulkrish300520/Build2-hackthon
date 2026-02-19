from fastapi import APIRouter
from database.db import SessionLocal
from models.node_model import Node
from database.schemas import NodeResponse
from typing import List

router = APIRouter()

@router.get("/nodes", response_model=List[NodeResponse])
def get_nodes():
    db = SessionLocal()
    nodes = db.query(Node).all()
    db.close()
    return nodes