import pygame as pg  # Nhập thư viện Pygame và đặt bí danh là "pg".

class BGObject(object):  # Định nghĩa một lớp tên là BGObject, đại diện cho một đối tượng nền.
    def __init__(self, x, y, image):  # Phương thức khởi tạo (constructor) của lớp BGObject.
        self.rect = pg.Rect(x, y, 32, 32)  # Tạo một hình chữ nhật (rect) với tọa độ (x, y) và kích thước 32x32 pixel.
        self.image = image  # Lưu hình ảnh của đối tượng, được truyền vào qua tham số `image`.
        self.type = 'BGObject'  # Đặt thuộc tính `type` để xác định đây là một đối tượng nền (Background Object).

    def render(self, core):  # Phương thức để vẽ đối tượng lên màn hình.
        # Vẽ hình ảnh của đối tượng lên màn hình thông qua camera, đảm bảo hình ảnh di chuyển theo bản đồ.
        # `core.screen.blit()` dùng để vẽ hình ảnh lên màn hình.
        # `core.get_map().get_camera().apply(self)` xử lý việc di chuyển của đối tượng trên màn hình, phụ thuộc vào vị trí camera.
        core.screen.blit(self.image, core.get_map().get_camera().apply(self))
