# File __init__.py trong thư mục models
# File này thường được sử dụng để khởi tạo package 'models'
# và định nghĩa các hàm, biến có thể truy cập từ package này.

# Import các thư viện và module cần thiết
import hashlib  # Thư viện để băm mật khẩu
from models.model_base import ModelBase  # Import lớp cơ sở cho các model
from models.todo import Todo  # Import model Todo
from models.tag import Tag  # Import model Tag
from models.todo_tag import TodoTag  # Import model TodoTag (bảng trung gian)
from models.user import User  # Import model User
from sqlalchemy.orm import Session  # Import Session để tương tác với database

def ini_db(engine):
    """
    Hàm này dùng để khởi tạo cơ sở dữ liệu.
    Nó sẽ xóa tất cả các bảng hiện có và tạo lại chúng từ đầu,
    sau đó thêm một số dữ liệu mẫu.

    Args:
        engine: Đối tượng engine của SQLAlchemy đã được tạo trước đó.
    """
    with engine.begin() as conn:
        # Mở một kết nối đến database
        
        # Xóa tất cả các bảng cũ (nếu có)
        print("Đang xóa các bảng cũ...")
        ModelBase.metadata.drop_all(engine)
        print("Đã xóa xong.")

        # Tạo lại tất cả các bảng mới dựa trên các model đã định nghĩa
        print("Đang tạo các bảng mới...")
        ModelBase.metadata.create_all(engine)
        print("Đã tạo xong.")

        # Bắt đầu thêm dữ liệu mẫu
        print("Đang thêm dữ liệu mẫu...")
        session = Session(bind=conn) # Tạo một session mới để thực hiện các transaction

        # --- Thêm tài khoản quản trị (admin) ---
        admin_user = User(login="admin", email="admin@example.com", is_admin=True, name="Administrator")
        admin_user.password = hash_password("admin")  # Băm mật khẩu "admin"
        session.add(admin_user) # Thêm user admin vào session
        session.commit() # Lưu thay đổi vào database

        # --- Thêm các tài khoản người dùng mẫu ---
        user1 = User(login="john", email="john@example.com", name="John Doe")
        user1.password = hash_password("123456") # Băm mật khẩu
        user2 = User(login="jane", email="jane@example.com", name="Jane Smith")
        user2.password = hash_password("123456")
        session.add_all([user1, user2]) # Thêm nhiều user cùng lúc
        session.commit()

        # --- Thêm các nhãn (tag) mẫu ---
        tag1 = Tag(name="Công việc")
        tag2 = Tag(name="Cá nhân")
        tag3 = Tag(name="Học tập")
        session.add_all([tag1, tag2, tag3])
        session.commit()

        # --- Thêm các công việc (todo) mẫu và gán cho user ---
        todo1 = Todo(title="Hoàn thành báo cáo dự án", description="Hoàn thành báo cáo cuối kỳ cho dự án ABC.", user=user1)
        todo2 = Todo(title="Đi mua đồ tạp hóa", description="Mua sữa, trứng, và bánh mì.", user=user1)
        todo3 = Todo(title="Họp nhóm", description="Thảo luận tiến độ dự án với các thành viên trong nhóm.", user=user2)
        session.add_all([todo1, todo2, todo3])
        session.commit()

        # --- Gán các nhãn cho công việc (tạo mối quan hệ nhiều-nhiều) ---
        # Sử dụng bảng trung gian TodoTag
        todo1.tags.append(TodoTag(tag=tag1, todo=todo1)) # Gán tag "Công việc" cho todo1
        todo1.tags.append(TodoTag(tag=tag2, todo=todo1)) # Gán tag "Cá nhân" cho todo1
        todo2.tags.append(TodoTag(tag=tag2, todo=todo2)) # Gán tag "Cá nhân" cho todo2
        todo2.tags.append(TodoTag(tag=tag3, todo=todo2)) # Gán tag "Học tập" cho todo2
        todo3.tags.append(TodoTag(tag=tag1, todo=todo3)) # Gán tag "Công việc" cho todo3
        
        session.commit() # Lưu các mối quan hệ tag-todo
        session.close() # Đóng session sau khi hoàn tất
        print("Khởi tạo và thêm dữ liệu mẫu cho cơ sở dữ liệu thành công.")

def hash_password(password: str) -> str:
    """
    Hàm để băm mật khẩu sử dụng thuật toán SHA256.

    Args:
        password (str): Mật khẩu ở dạng chuỗi thuần túy (chưa băm).

    Returns:
        str: Chuỗi hex của mật khẩu đã được băm.
    """
    # Mã hóa chuỗi mật khẩu sang UTF-8, sau đó băm bằng SHA256
    # .hexdigest() để chuyển đổi kết quả băm thành dạng chuỗi hex dễ đọc và lưu trữ
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_password(stored_password_hash: str, provided_password: str) -> bool:
    """
    Hàm để xác thực mật khẩu người dùng cung cấp với mật khẩu đã được băm và lưu trong database.

    Args:
        stored_password_hash (str): Chuỗi băm mật khẩu lấy từ database.
        provided_password (str): Mật khẩu người dùng nhập vào (chuỗi thuần túy).

    Returns:
        bool: True nếu mật khẩu khớp, False nếu không khớp.
    """
    # Băm mật khẩu người dùng cung cấp và so sánh với chuỗi băm đã lưu
    return stored_password_hash == hashlib.sha256(provided_password.encode("utf-8")).hexdigest()
