# Import các thư viện và module cần thiết
import datetime  # Để làm việc với ngày giờ
from models.user import User  # Import model User để truy vấn thông tin người dùng
from sqlalchemy.orm import Session  # Import Session để tương tác với database
from fasthtml import common as FH  # Import thư viện FastHTML để xây dựng giao diện

# --- Hàm trợ giúp (Helper Function) ---
def get_current_user(session, engine) -> User | None:
    """
    Hàm này lấy thông tin của người dùng hiện tại đang đăng nhập dựa vào session.

    Args:
        session: Đối tượng session của request, chứa thông tin phiên làm việc.
        engine: Đối tượng engine của SQLAlchemy để kết nối database.

    Returns:
        User | None: Trả về đối tượng User nếu tìm thấy, ngược lại trả về None.
    """
    # Kiểm tra xem có 'login' trong session không. Nếu không, tức là chưa đăng nhập.
    if 'login' not in session:
        return None
    
    # Mở một session mới để truy vấn database
    with Session(engine) as db:
        # Truy vấn bảng 'users' để tìm người dùng có 'login' trùng với giá trị trong session
        user = db.query(User).filter(User.login == session.get('login')).first()
        db.close() # Đóng session sau khi xong việc
        return user # Trả về đối tượng user hoặc None nếu không tìm thấy

# --- Hàm tạo giao diện (View Function) ---
def login_view(error_msg: str = ""):
    """
    Hàm này tạo và trả về giao diện trang đăng nhập.

    Args:
        error_msg (str, optional): Một thông báo lỗi (nếu có) để hiển thị trên trang. Mặc định là chuỗi rỗng.

    Returns:
        FH.Html: Một đối tượng HTML hoàn chỉnh cho trang đăng nhập.
    """
    # Sử dụng các component của FastHTML (FH) để xây dựng cây HTML
    return FH.Html(
        FH.Head(
            FH.Title("Đăng nhập"),  # Tiêu đề của trang
            FH.picolink  # Tự động thêm link đến CSS của Pico.css để có giao diện đẹp
        ),
        FH.Body(
            FH.H1("Đăng nhập"), # Tiêu đề chính trên trang
            # Nếu có thông báo lỗi (error_msg không rỗng) thì hiển thị nó trong một thẻ Div màu đỏ
            FH.Div(error_msg, style="color:red;") if error_msg else None,
            # Tạo form đăng nhập
            FH.Form(
                # Nhãn và ô nhập liệu cho tên đăng nhập
                FH.Label("Tên đăng nhập: ", FH.Input(name="login", type="text", value="admin")),
                # Nhãn và ô nhập liệu cho mật khẩu
                FH.Label("Mật khẩu: ", FH.Input(name="password", type="password", value="admin")),
                # Nút submit form
                FH.Button("Gửi", type="submit"),
                id="login-form", # ID của form
                action="/login", # URL để gửi dữ liệu form khi submit (gửi đến route POST /login)
                method="POST",   # Phương thức HTTP là POST
            ),
            cls="container" # Áp dụng class 'container' của Pico.css cho thẻ Body
        )
    )

# --- Middleware Function ---
def require_login(request, session):
    """
    Đây là một "beforeware" (middleware), được thực thi trước khi xử lý một request.
    Chức năng chính là kiểm tra xem người dùng đã đăng nhập hay chưa.

    Args:
        request: Đối tượng request đến.
        session: Đối tượng session của request.

    Returns:
        FH.Redirect | None: Nếu chưa đăng nhập hoặc session hết hạn, trả về một đối tượng Redirect
                            để chuyển hướng người dùng đến trang login. Nếu đã đăng nhập và hợp lệ,
                            trả về None để cho phép request được tiếp tục xử lý bình thường.
    """
    # Nếu không có 'login' trong session, chuyển hướng ngay đến trang /login
    if 'login' not in session:
        return FH.Redirect("/login")
    
    # Kiểm tra thời gian không hoạt động. Nếu quá 15 phút, xóa session và bắt đăng nhập lại.
    # Lấy thời gian hiện tại
    now = datetime.datetime.now()
    # Lấy thời gian hoạt động cuối cùng từ session (được lưu dưới dạng chuỗi ISO format)
    last_active_str = session.get('last_active')
    if last_active_str:
        last_active = datetime.datetime.fromisoformat(last_active_str)
        # Nếu khoảng thời gian từ lần hoạt động cuối đến giờ lớn hơn 15 phút
        if now - last_active > datetime.timedelta(minutes=15):
            session.clear()  # Xóa toàn bộ dữ liệu trong session
            return FH.Redirect("/login") # Chuyển hướng về trang login

    # Nếu mọi thứ đều ổn, cập nhật lại thời gian hoạt động cuối cùng là thời gian hiện tại
    session['last_active'] = now.isoformat()
    
    # Trả về None để cho phép request đi tiếp
    return None
