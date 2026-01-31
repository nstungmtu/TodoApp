# Đây là file __init__.py trong thư mục 'Home'.
# Sự tồn tại của file này (kể cả khi nó trống) giúp Python nhận diện thư mục 'Home'
# là một package. Điều này cho phép bạn import các module từ bên trong nó,
# ví dụ: from views.Home import index

# Bạn cũng có thể đặt code khởi tạo cho package 'Home' tại đây nếu cần.
from .index import *  # Import tất cả các hàm và lớp từ index.py