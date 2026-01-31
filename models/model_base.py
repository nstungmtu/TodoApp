# Import các thành phần cần thiết từ thư viện SQLAlchemy
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

# Định nghĩa một lớp cơ sở (base class) cho tất cả các model trong ứng dụng.
# Lớp này kế thừa từ DeclarativeBase của SQLAlchemy, cho phép các lớp con
# (các model cụ thể như User, Todo) được tự động ánh xạ tới các bảng trong database.
class ModelBase(DeclarativeBase):
    """
    Lớp ModelBase này chứa các cột chung mà mọi bảng trong cơ sở dữ liệu đều nên có.
    Việc này giúp tái sử dụng code và đảm bảo tính nhất quán.
    """
    
    # Cột 'id':
    # - Đây là khóa chính (primary_key=True) của mỗi bảng.
    # - Kiểu dữ liệu là Integer.
    # - Giá trị sẽ tự động tăng (autoincrement=True) mỗi khi có một bản ghi mới được thêm vào.
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Cột 'created_at':
    # - Lưu trữ thời điểm bản ghi được tạo ra.
    # - Kiểu dữ liệu là DateTime.
    # - Giá trị mặc định (default) là thời gian hiện tại (datetime.now) khi bản ghi được tạo.
    created_at = Column(DateTime, default=datetime.now)
    
    # Cột 'updated_at':
    # - Lưu trữ thời điểm bản ghi được cập nhật lần cuối.
    # - Kiểu dữ liệu là DateTime.
    # - Giá trị mặc định là thời gian hiện tại khi tạo bản ghi.
    # - Mỗi khi bản ghi được cập nhật (onupdate), giá trị của cột này sẽ tự động được cập nhật thành thời gian hiện tại.
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Cột 'deleted_at':
    # - Hỗ trợ "xóa mềm" (soft delete). Thay vì xóa hẳn bản ghi khỏi database,
    #   chúng ta chỉ đánh dấu là nó đã bị xóa bằng cách ghi thời gian vào cột này.
    # - Kiểu dữ liệu là DateTime.
    # - Cho phép giá trị rỗng (nullable=True), nghĩa là nếu bản ghi chưa bị xóa, cột này sẽ là NULL.
    deleted_at = Column(DateTime, nullable=True)
    
    # Cột 'is_deleted':
    # - Một cách khác để hỗ trợ "xóa mềm", thường dùng song song với 'deleted_at'.
    # - Kiểu dữ liệu là Integer, nhưng thường chỉ dùng giá trị 0 hoặc 1.
    # - Giá trị mặc định là 0, có nghĩa là bản ghi chưa bị xóa.
    # - Khi một bản ghi được "xóa mềm", giá trị này sẽ được cập nhật thành 1.
    is_deleted = Column(Integer, default=0)