import pygame as pg

from Const import *

class PlatformDebris(object):
    """
    Debris which appears when you destroy a brick block.
    This class handles the debris pieces that scatter when a block is destroyed.
    """
    def __init__(self, x_pos, y_pos):
        # Tải hình ảnh của mảnh vụn từ tệp hình ảnh.
        self.image = pg.image.load('images/block_debris0.png').convert_alpha()

        # Tạo 4 mảnh vụn với các vị trí khác nhau xung quanh vị trí của block.
        self.rectangles = [
            pg.Rect(x_pos - 20, y_pos + 16, 16, 16),  # Mảnh vụn phía bên trái dưới
            pg.Rect(x_pos - 20, y_pos - 16, 16, 16),  # Mảnh vụn phía bên trái trên
            pg.Rect(x_pos + 20, y_pos + 16, 16, 16),  # Mảnh vụn phía bên phải dưới
            pg.Rect(x_pos + 20, y_pos - 16, 16, 16)   # Mảnh vụn phía bên phải trên
        ]
        self.y_vel = -4  # Tốc độ rơi ban đầu theo phương y (ngược chiều với trục y)
        self.rect = None  # Biến không được sử dụng, có thể dùng cho vẽ mảnh vụn

    def update(self, core):
        # Cập nhật vận tốc rơi theo gia tốc trọng trường (FALL_MULTIPLIER có thể là một hằng số)
        self.y_vel += GRAVITY * FALL_MULTIPLIER

        # Cập nhật vị trí của từng mảnh vụn
        for i in range(len(self.rectangles)):
            self.rectangles[i].y += self.y_vel  # Cập nhật vị trí theo chiều dọc (y)

            # Di chuyển các mảnh vụn sang trái hoặc phải tùy thuộc vào chỉ số mảnh
            if i < 2:
                self.rectangles[i].x -= 1  # Mảnh vụn phía bên trái di chuyển sang trái
            else:
                self.rectangles[i].x += 1  # Mảnh vụn phía bên phải di chuyển sang phải

        # Nếu mảnh vụn đi ra ngoài màn hình, xóa nó khỏi danh sách debris
        if self.rectangles[1].y > core.get_map().mapSize[1] * 32:
            core.get_map().debris.remove(self)

    def render(self, core):
        # Vẽ tất cả mảnh vụn lên màn hình
        for rect in self.rectangles:
            self.rect = rect  # Cập nhật rect hiện tại
            core.screen.blit(self.image, core.get_map().get_camera().apply(self))  # Vẽ mảnh vụn trên màn hình
