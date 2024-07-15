from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    extension = Column(String)
    size = Column(Integer)
    path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    comment = Column(String, nullable=True)
