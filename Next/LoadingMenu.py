import pygame as pg

from Const import *
from Text import Text


class LoadingMenu(object):
    def __init__(self, core):
        self.iTime = pg.time.get_ticks()  # Lưu thời gian bắt đầu khi tạo LoadingMenu
        self.loadingType = True  # Biến để xác định loại màn hình tải (True cho màn hình tải game, False cho màn hình tải menu)
        self.bg = pg.Surface((WINDOW_W, WINDOW_H))  # Tạo một bề mặt để làm nền cho màn hình tải
        self.text = Text('WORLD ' + core.oWorld.get_name(), 32, (WINDOW_W / 2, WINDOW_H / 2))  # Tạo đối tượng Text để hiển thị tên thế giới

    def update(self, core):
        # Kiểm tra nếu đã đủ thời gian tải để chuyển sang màn hình tiếp theo
        if pg.time.get_ticks() >= self.iTime + (5250 if not self.loadingType else 2500):
            if self.loadingType:
                # Chuyển sang màn hình "Game" sau khi hết thời gian tải
                core.oMM.currentGameState = 'Game'  
                core.get_sound().play('overworld', 999999, 0.5)  # Phát nhạc nền cho màn chơi
                core.get_map().in_event = False  # Đặt trạng thái của bản đồ là không trong sự kiện
            else:
                # Nếu không phải màn hình game, quay lại menu chính
                core.oMM.currentGameState = 'MainMenu'  
                self.set_text_and_type('WORLD ' + core.oWorld.get_name(), True)  # Đặt lại thông báo với tên thế giới
                core.get_map().reset(True)  # Reset lại bản đồ khi quay lại menu chính

    def set_text_and_type(self, text, type):
        # Hàm để thay đổi văn bản và loại màn hình tải
        self.text = Text(text, 32, (WINDOW_W / 2, WINDOW_H / 2))  # Cập nhật văn bản mới
        self.loadingType = type  # Cập nhật loại màn hình tải

    def render(self, core):
        # Vẽ nền và văn bản lên màn hình
        core.screen.blit(self.bg, (0, 0))
        self.text.render(core)  # Hiển thị văn bản

    def update_time(self):
        # Cập nhật thời gian hiện tại (để tính toán thời gian tải)
        self.iTime = pg.time.get_ticks()
