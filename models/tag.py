# Import các thành phần cần thiết từ SQLAlchemy và model cơ sở
from models.model_base import ModelBase  # Lớp cơ sở cho các model
from sqlalchemy import String  # Kiểu dữ liệu chuỗi cho cột
from sqlalchemy.orm import Mapped, mapped_column, relationship # Công cụ ánh xạ và mối quan hệ

# Định nghĩa lớp Tag, đại diện cho bảng 'tags' (nhãn) trong cơ sở dữ liệu.
# Lớp này kế thừa từ ModelBase để có các cột chung như id, created_at, v.v.
class Tag(ModelBase):
    # __tablename__ chỉ định tên của bảng trong database.
    __tablename__ = "tags"

    # Cột 'name': Tên của nhãn.
    # - Mapped[str]: Kiểu dữ liệu trong Python là chuỗi.
    # - String(50): Kiểu dữ liệu trong database là VARCHAR với độ dài tối đa 50 ký tự.
    # - unique=True: Đảm bảo mỗi nhãn có tên duy nhất.
    # - nullable=False: Tên nhãn là bắt buộc.
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # Cột 'description': Mô tả chi tiết hơn về nhãn.
    # - Mapped[str]: Kiểu dữ liệu trong Python là chuỗi.
    # - String(200): Kiểu dữ liệu trong database là VARCHAR(200).
    # - nullable=True: Mô tả không bắt buộc, có thể để trống (NULL).
    description: Mapped[str] = mapped_column(String(200), nullable=True)

    # Định nghĩa mối quan hệ một-nhiều (one-to-many) với bảng trung gian 'TodoTag'.
    # Thuộc tính 'todos' này cho phép từ một đối tượng Tag, ta có thể truy cập được danh sách
    # các bản ghi trong bảng TodoTag liên quan đến nó.
    # - Mapped[list["TodoTag"]]: Type hint cho biết 'todos' là một danh sách các đối tượng 'TodoTag'.
    # - relationship("TodoTag", ...): Hàm của SQLAlchemy để tạo mối quan hệ.
    #   + "TodoTag": Tên của lớp (model) ở phía "nhiều", chính là bảng trung gian.
    #   + back_populates="tag": Thiết lập mối quan hệ hai chiều. Nó chỉ định rằng trong lớp 'TodoTag',
    #     có một thuộc tính tên là "tag" cũng đang trỏ ngược lại lớp 'Tag' này.
    #     Điều này giúp SQLAlchemy đồng bộ hóa mối quan hệ. Ví dụ: khi bạn gán một TodoTag vào
    #     danh sách `my_tag.todos`, thuộc tính `tag` của TodoTag đó sẽ tự động được gán là `my_tag`.
    todos: Mapped[list["TodoTag"]] = relationship("TodoTag", back_populates="tag")
