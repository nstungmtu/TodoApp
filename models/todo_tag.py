from models.model_base import ModelBase
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey

class TodoTag(ModelBase):
    __tablename__ = "todo_tags"
    todo_id: Mapped[int] = mapped_column(ForeignKey("todos.id"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"))
    todo: Mapped["Todo"] = relationship("Todo", back_populates="tags")
    tag: Mapped["Tag"] = relationship("Tag", back_populates="todos")