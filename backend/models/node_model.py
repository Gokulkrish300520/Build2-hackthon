from sqlalchemy import Column, String, Integer
from database.db import Base

class Node(Base):
    __tablename__ = "nodes"

    node_id = Column(String, primary_key=True, index=True)
    last_seen = Column(Integer)
    battery = Column(Integer)
    status = Column(String)  # ONLINE / OFFLINE