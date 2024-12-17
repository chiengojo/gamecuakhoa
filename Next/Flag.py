import pygame as pg


class Flag(object):
    """
    Lớp đại diện cho cột cờ trong trò chơi.
    """
    def __init__(self, x_pos, y_pos):
        # Khởi tạo thuộc tính của cột cờ.

        # `rect` là hình chữ nhật để theo dõi vị trí, khởi tạo là None.
        self.rect = None

        # Offset của cờ, được sử dụng để kiểm soát chuyển động xuống của lá cờ.
        self.flag_offset = 0

        # Trạng thái của cờ: True = cờ đã hạ, False = cờ vẫn còn trên cao.
        self.flag_omitted = False

        # Cột cờ bao gồm 2 phần: cột (pillar) và lá cờ (flag).

        # Hình ảnh và hình chữ nhật của cột cờ.
        self.pillar_image = pg.image.load('images/flag_pillar.png').convert_alpha()
        self.pillar_rect = pg.Rect(x_pos + 8, y_pos, 16, 304)

        # Hình ảnh và hình chữ nhật của lá cờ.
        self.flag_image = pg.image.load('images/flag.png').convert_alpha()
        self.flag_rect = pg.Rect(x_pos - 18, y_pos + 16, 32, 32)

    def move_flag_down(self):
        """
        Hạ lá cờ xuống bằng cách tăng vị trí y và cập nhật offset.
        """
        self.flag_offset += 3  # Tăng offset để theo dõi khoảng cách di chuyển của lá cờ.
        self.flag_rect.y += 3  # Di chuyển vị trí y của lá cờ xuống dưới.

        # Nếu lá cờ đã di chuyển đủ khoảng cách (255 pixels).
        if self.flag_offset >= 255:
            self.flag_omitted = True  # Đánh dấu rằng cờ đã được hạ xong.

    def render(self, core):
        """
        Vẽ cột và lá cờ lên màn hình.
        """
        # Vẽ cột cờ:
        self.rect = self.pillar_rect
        core.screen.blit(self.pillar_image, core.get_map().get_camera().apply(self))

        # Vẽ lá cờ:
        self.rect = self.flag_rect
        core.screen.blit(self.flag_image, core.get_map().get_camera().apply(self))
