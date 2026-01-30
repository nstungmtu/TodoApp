from models.model_base import ModelBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(ModelBase):
    __tablename__ = "users"
    login: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False),
    is_admin: Mapped[int] = mapped_column(Integer, default=0),
    todos: Mapped[list["Todo"]] = relationship("Todo", back_populates="user")