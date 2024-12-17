import pygame as pg

from Const import *
from Text import Text


class MainMenu(object):
    def __init__(self):
        # Tải ảnh nền cho màn hình chính
        self.mainImage = pg.image.load(r'images\gamemenu1.png').convert_alpha()

        # Tạo đối tượng Text để hiển thị thông báo yêu cầu nhấn ENTER để bắt đầu
        self.toStartText = Text('Press enter to start', 16, (WINDOW_W - WINDOW_W * 0.72, WINDOW_H - WINDOW_H * 0.85))

    def render(self, core):
        # Vẽ hình ảnh nền lên màn hình
        core.screen.blit(self.mainImage, (0, 0))

        # Vẽ văn bản yêu cầu người chơi nhấn ENTER
        self.toStartText.render(core)
