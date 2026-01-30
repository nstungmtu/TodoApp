from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class ModelBase(DeclarativeBase):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)
    is_deleted = Column(Integer, default=0)

    