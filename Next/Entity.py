import pygame as pg  # Nhập thư viện Pygame, đặt tên tắt là `pg`.
from Const import *  # Nhập các hằng số từ file `Const`.

class Entity(object):  # Định nghĩa lớp cha `Entity`, được sử dụng làm cơ sở cho các lớp "mob".
    """
    Lớp cha cho các thực thể di chuyển trong trò chơi (mob).
    """

    def __init__(self):  # Hàm khởi tạo.
        self.state = 0  # Trạng thái hiện tại của thực thể (có thể sử dụng để xác định hành động, ví dụ: đi, chạy, đứng yên...).
        self.x_vel = 0  # Vận tốc theo trục x.
        self.y_vel = 0  # Vận tốc theo trục y.

        self.move_direction = True  # Hướng di chuyển (True: sang phải, False: sang trái).
        self.on_ground = False  # Cờ kiểm tra thực thể có đang tiếp đất hay không.
        self.collision = True  # Cờ kiểm tra thực thể có thể va chạm hay không.

        self.image = None  # Hình ảnh của thực thể (sẽ được gán trong các lớp con).
        self.rect = None  # Hình chữ nhật bao quanh thực thể (dùng để xử lý va chạm).

    def update_x_pos(self, blocks):  # Hàm cập nhật vị trí x dựa trên vận tốc và va chạm.
        self.rect.x += self.x_vel  # Di chuyển thực thể theo vận tốc x.

        for block in blocks:  # Kiểm tra va chạm với từng khối trong danh sách "blocks".
            if block != 0 and block.type != 'BGObject':  # Loại trừ các khối nền không va chạm.
                if pg.Rect.colliderect(self.rect, block.rect):  # Nếu xảy ra va chạm.
                    if self.x_vel > 0:  # Nếu đang di chuyển sang phải.
                        self.rect.right = block.rect.left  # Dừng lại ở cạnh trái của khối.
                        self.x_vel = - self.x_vel  # Đảo hướng di chuyển.
                    elif self.x_vel < 0:  # Nếu đang di chuyển sang trái.
                        self.rect.left = block.rect.right  # Dừng lại ở cạnh phải của khối.
                        self.x_vel = - self.x_vel  # Đảo hướng di chuyển.

    def update_y_pos(self, blocks):  # Hàm cập nhật vị trí y dựa trên vận tốc và va chạm.
        self.rect.y += self.y_vel * FALL_MULTIPLIER  # Di chuyển thực thể theo vận tốc y và hệ số rơi.

        self.on_ground = False  # Mặc định là không tiếp đất.
        for block in blocks:  # Kiểm tra va chạm với từng khối.
            if block != 0 and block.type != 'BGObject':  # Loại trừ các khối nền không va chạm.
                if pg.Rect.colliderect(self.rect, block.rect):  # Nếu xảy ra va chạm.
                    if self.y_vel > 0:  # Nếu đang rơi xuống.
                        self.on_ground = True  # Đánh dấu thực thể đang tiếp đất.
                        self.rect.bottom = block.rect.top  # Căn chỉnh cạnh dưới của thực thể với cạnh trên của khối.
                        self.y_vel = 0  # Dừng rơi (vận tốc y bằng 0).

    def check_map_borders(self, core):  # Kiểm tra thực thể có vượt qua biên bản đồ không.
        if self.rect.y >= 448:  # Nếu rơi xuống dưới màn hình (y >= 448).
            self.die(core, True, False)  # Gọi hàm chết.
        if self.rect.x <= 1 and self.x_vel < 0:  # Nếu chạm biên trái của màn hình và đang di chuyển sang trái.
            self.x_vel = - self.x_vel  # Đảo hướng di chuyển.

    def die(self, core, instantly, crushed):  # Hàm xử lý thực thể bị tiêu diệt.
        pass  # Hiện tại không thực hiện gì (sẽ được định nghĩa trong các lớp con).

    def render(self, core):  # Hàm hiển thị thực thể lên màn hình.
        pass  # Hiện tại không thực hiện gì (sẽ được định nghĩa trong các lớp con).
