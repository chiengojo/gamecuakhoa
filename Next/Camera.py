import pygame as pg  # Nhập thư viện Pygame và đặt bí danh là "pg".
from Const import *  # Nhập tất cả các hằng số từ tệp Const.py (WINDOW_W, WINDOW_H có thể nằm ở đây).

class Camera(object):  # Định nghĩa lớp `Camera`, quản lý và di chuyển camera trong trò chơi.
    """
    Mô tả:
    Lớp `Camera` điều khiển vị trí của màn hình (camera) dựa trên mục tiêu (target).
    Người viết không hoàn toàn hiểu cách nó hoạt động và sao chép từ một dự án khác.
    """

    def __init__(self, width, height):  # Khởi tạo camera với kích thước bản đồ (width, height).
        self.rect = pg.Rect(0, 0, width, height)  # Tạo một hình chữ nhật đại diện cho vùng nhìn của camera.
        self.complex_camera(self.rect)  # Thiết lập vị trí ban đầu cho camera.

    def complex_camera(self, target_rect):  # Hàm tính toán vị trí camera dựa trên mục tiêu.
        # Lấy tọa độ x, y của mục tiêu.
        x, y = target_rect.x, target_rect.y

        # Lấy kích thước của camera.
        width, height = self.rect.width, self.rect.height

        # Tính toán vị trí mới của camera để mục tiêu ở giữa màn hình (dựa vào kích thước cửa sổ WINDOW_W, WINDOW_H).
        x, y = (-x + WINDOW_W / 2 - target_rect.width / 2), (-y + WINDOW_H / 2 - target_rect.height)

        # Giới hạn camera không vượt ra ngoài bản đồ ở trục x.
        x = min(0, x)  # Không cho camera trượt sang trái quá bản đồ.
        x = max(-(self.rect.width - WINDOW_W), x)  # Không cho camera trượt sang phải vượt biên bản đồ.

        # Cố định camera ở đáy màn hình, nếu cần thiết (trục y không di chuyển trong đoạn này).
        y = WINDOW_H - self.rect.h

        # Trả về một hình chữ nhật mới với tọa độ x, y đã điều chỉnh.
        return pg.Rect(x, y, width, height)

    def apply(self, target):  # Hàm áp dụng vị trí camera lên mục tiêu.
        # Tính toán vị trí mới của đối tượng trên màn hình dựa trên vị trí hiện tại của camera.
        return target.rect.x + self.rect.x, target.rect.y

    def update(self, target):  # Hàm cập nhật vị trí camera theo mục tiêu.
        # Cập nhật vị trí camera bằng cách tính toán lại tọa độ dựa trên mục tiêu (target).
        self.rect = self.complex_camera(target)

    def reset(self):  # Hàm đặt lại vị trí camera về tọa độ ban đầu.
        self.rect = pg.Rect(0, 0, self.rect.w, self.rect.h)
