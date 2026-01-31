# Import các thành phần cần thiết từ SQLAlchemy và model cơ sở
from models.model_base import ModelBase  # Lớp cơ sở cho các model
from sqlalchemy import Integer, String, Boolean  # Các kiểu dữ liệu cho cột
from sqlalchemy.orm import Mapped, mapped_column, relationship # Các công cụ để ánh xạ cột và định nghĩa mối quan hệ

# Định nghĩa lớp User, đại diện cho bảng 'users' trong cơ sở dữ liệu.
# Lớp này kế thừa từ ModelBase, do đó nó sẽ có các cột chung như id, created_at, v.v.
class User(ModelBase):
    # __tablename__ chỉ định tên của bảng trong cơ sở dữ liệu sẽ được ánh xạ tới lớp này.
    __tablename__ = "users"

    # Định nghĩa các cột của bảng 'users' bằng cách sử dụng Mapped và mapped_column của SQLAlchemy.
    # 'Mapped' là một type hint giúp trình kiểm tra kiểu (như mypy) hiểu được kiểu dữ liệu Python tương ứng.
    # 'mapped_column' dùng để định nghĩa chi tiết về cột trong database.

    # Cột 'login': Tên đăng nhập của người dùng.
    # - Mapped[str]: Kiểu dữ liệu trong Python là chuỗi (string).
    # - String(20): Kiểu dữ liệu trong database là VARCHAR với độ dài tối đa 20 ký tự.
    # - unique=True: Đảm bảo mỗi người dùng có một tên đăng nhập duy nhất, không trùng lặp.
    # - nullable=False: Cột này không được phép để trống (bắt buộc phải có giá trị).
    login: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    # Cột 'password': Mật khẩu của người dùng (đã được băm).
    # - Mapped[str]: Kiểu dữ liệu Python là chuỗi.
    # - String(256): Kiểu dữ liệu database là VARCHAR(256), đủ dài để lưu trữ chuỗi băm an toàn (ví dụ: SHA256).
    # - nullable=False: Mật khẩu là bắt buộc.
    password: Mapped[str] = mapped_column(String(256), nullable=False)

    # Cột 'name': Tên đầy đủ của người dùng.
    # - Mapped[str]: Kiểu dữ liệu Python là chuỗi.
    # - String(50): Kiểu dữ liệu database là VARCHAR(50).
    # - nullable=False: Tên người dùng là bắt buộc.
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    # Cột 'email': Địa chỉ email của người dùng.
    # - Mapped[str]: Kiểu dữ liệu Python là chuỗi.
    # - String(100): Kiểu dữ liệu database là VARCHAR(100).
    # - unique=True: Mỗi email là duy nhất.
    # - nullable=False: Email là bắt buộc.
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # Cột 'is_admin': Cho biết người dùng có phải là quản trị viên hay không.
    # - Mapped[bool]: Kiểu dữ liệu Python là boolean (True/False).
    # - Boolean: Kiểu dữ liệu database tương ứng (thường là 0 hoặc 1).
    # - default=False: Giá trị mặc định khi tạo user mới là không phải admin.
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    # Định nghĩa mối quan hệ một-nhiều (one-to-many) với bảng 'todos'.
    # Thuộc tính 'todos' này không phải là một cột trong bảng 'users'.
    # Nó là một thuộc tính "ảo" giúp dễ dàng truy cập danh sách các công việc (Todo) của một người dùng.
    # - Mapped[list["Todo"]]: Type hint cho biết 'todos' là một danh sách các đối tượng 'Todo'.
    # - relationship("Todo", ...): Hàm của SQLAlchemy để tạo mối quan hệ.
    #   + "Todo": Tên của lớp (model) ở phía "nhiều".
    #   + back_populates="user": Đây là chìa khóa để tạo mối quan hệ hai chiều. Nó chỉ định rằng
    #     ở trong lớp 'Todo', có một thuộc tính tên là "user" cũng sử dụng relationship()
    #     và trỏ ngược lại lớp 'User' này. Điều này giúp SQLAlchemy tự động đồng bộ
    #     khi bạn thay đổi mối quan hệ từ một trong hai phía (ví dụ: user.todos.append(my_todo)
    #     sẽ tự động gán my_todo.user = user).
    todos: Mapped[list["Todo"]] = relationship("Todo", back_populates="user")
