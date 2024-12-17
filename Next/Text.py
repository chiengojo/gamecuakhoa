import pygame as pg

class Text(object):
    def __init__(self, text, fontsize, rectcenter, font='Emulogic', textcolor = (255, 255, 255)):
        # Khởi tạo các thuộc tính của đối tượng Text
        self.font = pg.font.Font('fonts/emulogic.ttf', fontsize)  # Tạo đối tượng font với kiểu chữ và kích thước được chỉ định
        self.text = self.font.render(text, False, textcolor)  # Render văn bản với màu chỉ định
        self.rect = self.text.get_rect(center=rectcenter)  # Lấy rectangle (hình chữ nhật) bao quanh văn bản, căn giữa tại rectcenter
        self.y_offset = 0  # Biến dùng để điều chỉnh vị trí dọc của văn bản khi cần thiết

    def update(self, core):
        # Cập nhật vị trí của văn bản (di chuyển lên trên mỗi lần gọi)
        self.rect.y -= 1
        self.y_offset -= 1

        # Nếu văn bản di chuyển ra khỏi màn hình (y_offset đạt đến -100), loại bỏ văn bản khỏi bản đồ
        if self.y_offset == -100:
            core.get_map().remove_text(self)

    def render(self, core):
        # Vẽ văn bản lên màn hình mà không có camera (không dịch chuyển)
        core.screen.blit(self.text, self.rect)

    def render_in_game(self, core):
        # Vẽ văn bản lên màn hình có dịch chuyển theo camera (khi có hiệu ứng cuộn màn hình)
        core.screen.blit(self.text, core.get_map().get_camera().apply(self))
