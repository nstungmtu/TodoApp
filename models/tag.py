from models.model_base import ModelBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Tag(ModelBase):
    __tablename__ = "tags"
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=True)
    todos: Mapped[list["TodoTag"]] = relationship("TodoTag", back_populates="tag")