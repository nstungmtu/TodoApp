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
    # #Automatically hash password when setting it
    # def set_password(self, raw_password: str):
    #     import hashlib
    #     self.password = hashlib.sha256(raw_password.encode("utf-8")).hexdigest()
    # #Check password
    # def check_password(self, raw_password: str) -> bool:
    #     import hashlib
    #     return self.password == hashlib.sha256(raw_password.encode("utf-8")).hexdigest()
