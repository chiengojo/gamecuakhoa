import pygame as pg  # Nhập thư viện Pygame và đặt bí danh là "pg".

class CoinDebris(object):  # Định nghĩa lớp `CoinDebris`, đại diện cho đồng xu xuất hiện khi khối "?" bị đánh.
    """
    Đồng xu xuất hiện khi bạn đánh khối câu hỏi (Question Block).
    """

    def __init__(self, x_pos, y_pos):  # Khởi tạo đối tượng `CoinDebris` với vị trí ban đầu.
        self.rect = pg.Rect(x_pos, y_pos, 16, 28)  # Tạo hình chữ nhật cho đồng xu với kích thước 16x28 pixel.

        self.y_vel = -2  # Tốc độ di chuyển ban đầu theo trục y (di chuyển lên).
        self.y_offset = 0  # Biến lưu trữ sự thay đổi vị trí theo trục y.
        self.moving_up = True  # Biến cờ để kiểm tra đồng xu đang di chuyển lên hay xuống.

        self.current_image = 0  # Chỉ số của hình ảnh hiện tại trong danh sách ảnh động.
        self.image_tick = 0  # Bộ đếm để điều chỉnh tốc độ chuyển đổi giữa các ảnh động.
        self.images = [  # Danh sách hình ảnh của đồng xu, dùng để tạo hoạt ảnh.
            pg.image.load('images/servo (5).png').convert_alpha(),
            pg.image.load('images/servo (6).png').convert_alpha(),
            pg.image.load('images/servo (7).png').convert_alpha(),
            pg.image.load('images/servo (8).png').convert_alpha()
        ]

    def update(self, core):  # Hàm cập nhật trạng thái của đồng xu.
        self.image_tick += 1  # Tăng bộ đếm hình ảnh để chuyển đổi hoạt ảnh.

        if self.image_tick % 15 == 0:  # Mỗi 15 khung hình, chuyển sang hình ảnh tiếp theo.
            self.current_image += 1

        if self.current_image == 4:  # Khi đạt đến hình ảnh cuối, quay lại hình ảnh đầu tiên.
            self.current_image = 0
            self.image_tick = 0

        if self.moving_up:  # Nếu đồng xu đang di chuyển lên.
            self.y_offset += self.y_vel  # Cập nhật vị trí theo tốc độ y.
            self.rect.y += self.y_vel
            if self.y_offset < -50:  # Khi đồng xu di chuyển lên trên 50 pixel, đổi hướng.
                self.moving_up = False
                self.y_vel = -self.y_vel  # Đảo chiều tốc độ y.
        else:  # Nếu đồng xu đang di chuyển xuống.
            self.y_offset += self.y_vel
            self.rect.y += self.y_vel
            if self.y_offset == 0:  # Khi đồng xu trở về vị trí ban đầu, xóa nó khỏi bản đồ.
                core.get_map().debris.remove(self)

    def render(self, core):  # Hàm vẽ đồng xu lên màn hình.
        # Vẽ hình ảnh hiện tại của đồng xu lên màn hình dựa trên vị trí được điều chỉnh bởi camera.
        core.screen.blit(self.images[self.current_image], core.get_map().get_camera().apply(self))
