# Import các thư viện và module cần thiết
from datetime import datetime, timedelta  # Để làm việc với ngày giờ
from random import random  # Để tạo số ngẫu nhiên cho ngày hết hạn mặc định
from models.model_base import ModelBase  # Lớp cơ sở cho các model
from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, DateTime  # Các công cụ và kiểu dữ liệu của SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship  # Công cụ ánh xạ và mối quan hệ

# Định nghĩa lớp Todo, đại diện cho bảng 'todos' (công việc) trong cơ sở dữ liệu.
# Lớp này kế thừa từ ModelBase để có các cột chung.
class Todo(ModelBase):
    # __tablename__ chỉ định tên của bảng trong database.
    __tablename__ = "todos"

    # Cột 'title': Tiêu đề của công việc.
    # - Mapped[str]: Kiểu dữ liệu Python là chuỗi.
    # - String(100): Kiểu dữ liệu database là VARCHAR(100).
    # - nullable=False: Tiêu đề là bắt buộc.
    title: Mapped[str] = mapped_column(String(100), nullable=False)

    # Cột 'description': Mô tả chi tiết cho công việc.
    # - Mapped[str]: Kiểu dữ liệu Python là chuỗi.
    # - String(500): Kiểu dữ liệu database là VARCHAR(500).
    # - nullable=True: Mô tả không bắt buộc.
    description: Mapped[str] = mapped_column(String(500), nullable=True)

    # Cột 'status': Trạng thái của công việc.
    # - Mapped[str]: Kiểu dữ liệu Python là chuỗi.
    # - String(20): Kiểu dữ liệu database là VARCHAR(20).
    # - CheckConstraint(...): Một ràng buộc ở cấp độ database, đảm bảo rằng giá trị của cột 'status'
    #   chỉ có thể là một trong các giá trị 'pending', 'in_progress', hoặc 'completed'.
    # - nullable=False: Trạng thái là bắt buộc.
    # - default='pending': Giá trị mặc định khi tạo công việc mới là 'pending' (đang chờ).
    status: Mapped[str] = mapped_column(String(20), CheckConstraint("status IN ('pending', 'in_progress', 'completed')"), nullable=False, default='pending')

    # Cột 'due_date': Ngày hết hạn của công việc.
    # - Mapped[datetime]: Kiểu dữ liệu Python là đối tượng datetime.
    # - DateTime: Kiểu dữ liệu tương ứng trong database.
    # - nullable=True: Ngày hết hạn không bắt buộc.
    # - default=lambda...: Giá trị mặc định được tính toán bằng một hàm lambda. Ở đây, nó tạo ra một ngày
    #   hết hạn ngẫu nhiên trong tương lai (trong khoảng 0 đến 14*4 = 56 ngày).
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=lambda: datetime.now() + timedelta(days=14*int(random()*5)))

    # Cột 'priority': Mức độ ưu tiên của công việc.
    # - Mapped[int]: Kiểu dữ liệu Python là số nguyên.
    # - Integer: Kiểu dữ liệu tương ứng trong database.
    # - nullable=False: Mức độ ưu tiên là bắt buộc.
    # - default=1: Giá trị mặc định là 1.
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    # Cột 'user_id': Khóa ngoại (foreign key) trỏ đến bảng 'users'.
    # - Mapped[int]: Kiểu dữ liệu Python là số nguyên.
    # - ForeignKey("users.id"): Định nghĩa đây là một khóa ngoại, liên kết với cột 'id' của bảng 'users'.
    #   Điều này tạo ra mối quan hệ nhiều-một (many-to-one): nhiều công việc có thể thuộc về một người dùng.
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Mối quan hệ với bảng trung gian 'TodoTag'.
    # - Mapped[list["TodoTag"]]: 'tags' là một danh sách các đối tượng TodoTag.
    # - relationship("TodoTag", ...): Thiết lập mối quan hệ một-nhiều (one-to-many) từ Todo đến TodoTag.
    #   + "TodoTag": Tên lớp của bảng trung gian.
    #   + back_populates="todo": Liên kết hai chiều với thuộc tính 'todo' trong lớp 'TodoTag'.
    tags: Mapped[list["TodoTag"]] = relationship("TodoTag", back_populates="todo")

    # Mối quan hệ với bảng 'users'.
    # - Mapped["User"]: 'user' là một đối tượng User duy nhất.
    # - relationship("User", ...): Thiết lập mối quan hệ nhiều-một (many-to-one) từ Todo đến User.
    #   + "User": Tên lớp mà nó liên kết tới.
    #   + back_populates="todos": Liên kết hai chiều với thuộc tính 'todos' trong lớp 'User'.
    user: Mapped["User"] = relationship("User", back_populates="todos")