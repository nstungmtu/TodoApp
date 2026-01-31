# Import các thư viện và module cần thiết
from sqlalchemy import create_engine # Dùng để tạo engine kết nối đến database
from sqlalchemy.orm import Session # Dùng để tạo session làm việc với database
from models import * # Import tất cả các model từ thư mục models
from fasthtml import common as FH # Import thư viện fasthtml để xây dựng giao diện web
from models import user # Import model user cụ thể
from views import * # Import tất cả các view từ thư mục views
from views import Home # Import view Home cụ thể
from datetime import datetime

import views # Import thư viện datetime để làm việc với thời gian

# Tạo engine kết nối đến database SQLite
# "sqlite+pysqlite:///todo_app.db" là chuỗi kết nối đến file database an_todo.db
# echo=True sẽ hiển thị các câu lệnh SQL được thực thi
# future=True để sử dụng các tính năng mới của SQLAlchemy 2.0
engine = create_engine("sqlite+pysqlite:///todo_app.db", echo=True, future=True)

# Tạo Beforeware để kiểm tra login trước khi truy cập các trang
# require_login là hàm sẽ được gọi trước mỗi request
# skip=["/login", "/init_db", "/static/"] là danh sách các đường dẫn không cần kiểm tra login
beforeware = FH.Beforeware(require_login, skip=["/login", "/init_db", "/static/"])

# Tạo ứng dụng FastHTML
# beforeware=beforeware: áp dụng beforeware đã tạo ở trên
# static_folder="static": thư mục chứa các file tĩnh (css, js, images)
# pico=True: sử dụng Pico.css cho giao diện
# htmx=True: tích hợp HTMX để tạo các trang web động
app,rt = FH.fast_app(
    beforeware=beforeware,
    static_folder="static",
    pico=True,
    htmx=True,
)

# Định nghĩa route "/init_db" cho phương thức GET
# Route này dùng để khởi tạo database
@rt("/init_db")
def get(request):
    #Tạo bảng trong database bằng cách gọi hàm ini_db từ model
    ini_db(engine)
    # Trả về thông báo đã khởi tạo database thành công
    return FH.H1("Database initialized.")

# Định nghĩa route "/" (trang chủ) cho phương thức GET
@rt("/")
def get(request):
    #Kiểm tra trong session có user login chưa (đoạn code này đang được comment lại)
    # session = request.session
    # if "login" not in session:
    #     return FH.Redirect("/login")
    # Nếu có thì trả về trang chủ
    # user = get_current_user(session, engine)
    # if not user:
    #     return FH.Redirect("/login")
    # Trả về một thẻ H1 chào mừng user đã login
    #return FH.H1(f"Hello, World! {request.session.get('login')}")
    user = get_current_user(request.session, engine)
    # Load todos để tránh lỗi lazy loading ngoài session
    with Session(engine) as db:
        user = db.merge(user)
        _ = user.todos  # Truy cập thuộc tính todos để load dữ liệu
        for todo in user.todos:
            todotags = todo.tags  # Truy cập thuộc tính tags để load dữ liệu
            for todotag in todotags:
                _ = todotag.tag  # Truy cập thuộc tính tag để load dữ liệu
        db.close()
    
    return Home.home_page(user)

# Định nghĩa route "/login" cho phương thức GET
# Trả về giao diện login
@rt("/login")
def get(request):
    return login_view()

# Định nghĩa route "/login" cho phương thức POST
# Xử lý việc user submit form login
@rt("/login")
def post(request, login: str, password: str):
    #Kiểm tra login và password
    with Session(engine) as db: # Mở một session để làm việc với database
        # Băm mật khẩu người dùng nhập vào để so sánh với mật khẩu trong database
        hpw = hash_password(password)
        # Truy vấn database để tìm user có login và password khớp với thông tin người dùng nhập
        user = db.query(User).filter(User.login == login, User.password == hpw).first()
        # Nếu không tìm thấy user
        if not user:
            # Trả về lại trang login với thông báo lỗi
            return login_view("Không tìm thấy user hoặc sai mật khẩu.")
        #Lưu thông tin user vào session sau khi login thành công
        request.session['login'] = user.login
        request.session['is_admin'] = user.is_admin
        request.session['user_id'] = user.id
        request.session['name'] = user.name
        request.session['email'] = user.email
        request.session['login_time'] = datetime.now().isoformat() # Lưu thời gian login
        request.session['last_active'] = datetime.now().isoformat() # Lưu thời gian hoạt động cuối cùng
        db.close() # Đóng session
    # Chuyển hướng người dùng về trang chủ
    return FH.Redirect("/")

# Chạy ứng dụng web
# app="app": tên biến chứa ứng dụng FastHTML
# host="0.0.0.0": chạy trên tất cả các địa chỉ IP của máy
# port=80: chạy ở cổng 80
FH.serve(app="app", host="0.0.0.0", port=80)