from datetime import datetime, timedelta
from random import random
from models.model_base import ModelBase
from sqlalchemy import ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Todo(ModelBase):
    __tablename__ = "todos"
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=lambda: datetime.now() + timedelta(14*int(random()*5)))
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    tags: Mapped[list["TodoTag"]] = relationship("TodoTag", back_populates="todo")
    user: Mapped["User"] = relationship("User", back_populates="todos")
    
