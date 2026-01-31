# Import các thành phần cần thiết từ SQLAlchemy và model cơ sở
from models.model_base import ModelBase  # Lớp cơ sở cho các model
from sqlalchemy import Integer  # Kiểu dữ liệu số nguyên
from sqlalchemy.orm import Mapped, mapped_column, relationship  # Công cụ ánh xạ và mối quan hệ
from sqlalchemy.schema import ForeignKey  # Để định nghĩa khóa ngoại

# Định nghĩa lớp TodoTag, đại diện cho bảng 'todo_tags' trong cơ sở dữ liệu.
# Đây là một BẢNG TRUNG GIAN (association table) được sử dụng để tạo mối quan hệ
# nhiều-nhiều (many-to-many) giữa bảng 'todos' và bảng 'tags'.
# Mỗi bản ghi trong bảng này sẽ liên kết một công việc (todo) với một nhãn (tag).
class TodoTag(ModelBase):
    # __tablename__ chỉ định tên của bảng trong database.
    __tablename__ = "todo_tags"

    # Cột 'todo_id': Khóa ngoại trỏ đến bảng 'todos'.
    # - Mapped[int]: Kiểu dữ liệu Python là số nguyên.
    # - ForeignKey("todos.id"): Định nghĩa đây là khóa ngoại, liên kết với cột 'id' của bảng 'todos'.
    todo_id: Mapped[int] = mapped_column(ForeignKey("todos.id"))

    # Cột 'tag_id': Khóa ngoại trỏ đến bảng 'tags'.
    # - Mapped[int]: Kiểu dữ liệu Python là số nguyên.
    # - ForeignKey("tags.id"): Định nghĩa đây là khóa ngoại, liên kết với cột 'id' của bảng 'tags'.
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"))

    # Mối quan hệ với bảng 'todos'.
    # Thuộc tính này cho phép từ một đối tượng TodoTag, ta có thể truy cập được
    # đối tượng Todo mà nó liên kết tới.
    # - Mapped["Todo"]: 'todo' là một đối tượng Todo duy nhất.
    # - relationship("Todo", ...): Thiết lập mối quan hệ nhiều-một (many-to-one) từ TodoTag đến Todo.
    #   + "Todo": Tên lớp mà nó liên kết tới.
    #   + back_populates="tags": Liên kết hai chiều với thuộc tính 'tags' trong lớp 'Todo'.
    todo: Mapped["Todo"] = relationship("Todo", back_populates="tags")

    # Mối quan hệ với bảng 'tags'.
    # Thuộc tính này cho phép từ một đối tượng TodoTag, ta có thể truy cập được
    # đối tượng Tag mà nó liên kết tới.
    # - Mapped["Tag"]: 'tag' là một đối tượng Tag duy nhất.
    # - relationship("Tag", ...): Thiết lập mối quan hệ nhiều-một (many-to-one) từ TodoTag đến Tag.
    #   + "Tag": Tên lớp mà nó liên kết tới.
    #   + back_populates="todos": Liên kết hai chiều với thuộc tính 'todos' trong lớp 'Tag'.
    tag: Mapped["Tag"] = relationship("Tag", back_populates="todos")
