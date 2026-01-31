# Đây là file index.py trong package views.Home.
# File này được dự định để chứa các hàm xử lý logic và tạo giao diện
# cho trang chủ (index) của ứng dụng.

# Ví dụ, bạn có thể định nghĩa một hàm `index_view()` tại đây để trả về
# HTML cho trang chủ, hiển thị danh sách công việc của người dùng đang đăng nhập.

from fasthtml import common as FH
from sqlalchemy.orm import Session
from models import User, Todo

def home_page(user: User):
    return FH.Div(
        FH.H1(f"Chào mừng trở lại, {user.name}!"),
        FH.H2("Đây là danh sách công việc của bạn:"),
        FH.Ul(*[
            FH.Li(f"{todo.title} - Trạng thái: {todo.status} - Nhãn: {', '.join(tag.tag.name for tag in todo.tags)} - {todo.due_date}") for todo in user.todos
        ])
    )
