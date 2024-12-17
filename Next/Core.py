from os import environ  # Thư viện "os" được sử dụng để thiết lập các biến môi trường.
import pygame as pg  # Nhập thư viện Pygame và đặt bí danh là "pg".
from pygame.locals import *  # Nhập tất cả các hằng số của Pygame (như sự kiện, phím...).

from Const import *  # Nhập các hằng số từ tệp Const.py (WINDOW_W, WINDOW_H, FPS...).
from Map import Map  # Nhập lớp `Map` từ tệp Map.py (đại diện cho bản đồ trò chơi).
from MenuManager import MenuManager  # Nhập lớp `MenuManager` (quản lý menu trò chơi).
from Sound import Sound  # Nhập lớp `Sound` (quản lý âm thanh trong trò chơi).

class Core(object):  # Định nghĩa lớp chính `Core`, quản lý toàn bộ logic trò chơi.
    """
    Lớp chính của trò chơi (Core).
    """

    def __init__(self):  # Phương thức khởi tạo trò chơi.
        environ['SDL_VIDEO_CENTERED'] = '1'  # Đặt cửa sổ trò chơi ở giữa màn hình.
        pg.mixer.pre_init(44100, -16, 2, 1024)  # Thiết lập trước bộ trộn âm thanh với tần số 44.1kHz, 16-bit, âm thanh stereo.
        pg.init()  # Khởi tạo tất cả các mô-đun của Pygame.
        pg.display.set_caption('Mario by S&D')  # Đặt tiêu đề cho cửa sổ trò chơi.
        pg.display.set_mode((WINDOW_W, WINDOW_H))  # Thiết lập kích thước cửa sổ trò chơi.

        self.screen = pg.display.set_mode((WINDOW_W, WINDOW_H))  # Tạo bề mặt để vẽ các đối tượng trò chơi.
        self.clock = pg.time.Clock()  # Tạo đồng hồ để kiểm soát tốc độ khung hình.

        self.oWorld = Map('1-1')  # Tạo một bản đồ mới, cấp độ "1-1".
        self.oSound = Sound()  # Tạo đối tượng âm thanh để quản lý âm thanh trong trò chơi.
        self.oMM = MenuManager(self)  # Tạo đối tượng MenuManager, quản lý các menu của trò chơi.

        self.run = True  # Biến cờ để kiểm tra trò chơi đang chạy.
        # Các biến trạng thái kiểm tra phím nhấn (di chuyển, nhảy, tăng tốc).
        self.keyR = False  # Phím di chuyển sang phải.
        self.keyL = False  # Phím di chuyển sang trái.
        self.keyU = False  # Phím nhảy.
        self.keyD = False  # Phím cúi người (nếu cần).
        self.keyShift = False  # Phím tăng tốc.

    def main_loop(self):  # Vòng lặp chính của trò chơi.
        while self.run:  # Chạy liên tục khi `self.run` là True.
            self.input()  # Xử lý đầu vào từ người chơi.
            self.update()  # Cập nhật trạng thái trò chơi.
            self.render()  # Vẽ các đối tượng lên màn hình.
            self.clock.tick(FPS)  # Giới hạn tốc độ khung hình (FPS).

    def input(self):  # Xử lý đầu vào.
        if self.get_mm().currentGameState == 'Game':  # Nếu trạng thái là "Game", xử lý đầu vào trò chơi.
            self.input_player()
        else:  # Nếu không, xử lý đầu vào của menu.
            self.input_menu()

    def input_player(self):  # Xử lý đầu vào trong trạng thái chơi.
        for e in pg.event.get():  # Lấy danh sách các sự kiện.
            if e.type == pg.QUIT:  # Nếu sự kiện là thoát, dừng trò chơi.
                self.run = False

            elif e.type == KEYDOWN:  # Khi phím được nhấn.
                if e.key == K_RIGHT:  # Phím sang phải.
                    self.keyR = True
                elif e.key == K_LEFT:  # Phím sang trái.
                    self.keyL = True
                elif e.key == K_DOWN:  # Phím xuống.
                    self.keyD = True
                elif e.key == K_UP:  # Phím nhảy.
                    self.keyU = True
                elif e.key == K_LSHIFT:  # Phím tăng tốc.
                    self.keyShift = True

            elif e.type == KEYUP:  # Khi phím được thả ra.
                if e.key == K_RIGHT:
                    self.keyR = False
                elif e.key == K_LEFT:
                    self.keyL = False
                elif e.key == K_DOWN:
                    self.keyD = False
                elif e.key == K_UP:
                    self.keyU = False
                elif e.key == K_LSHIFT:
                    self.keyShift = False

    def input_menu(self):  # Xử lý đầu vào trong trạng thái menu.
        for e in pg.event.get():
            if e.type == pg.QUIT:  # Nếu sự kiện là thoát, dừng trò chơi.
                self.run = False

            elif e.type == KEYDOWN:  # Nếu nhấn phím Enter, bắt đầu tải trò chơi.
                if e.key == K_RETURN:
                    self.get_mm().start_loading()

    def update(self):  # Cập nhật trạng thái của trò chơi.
        self.get_mm().update(self)  # Gọi phương thức cập nhật từ `MenuManager`.

    def render(self):  # Vẽ tất cả các đối tượng lên màn hình.
        self.get_mm().render(self)  # Gọi phương thức vẽ từ `MenuManager`.

    def get_map(self):  # Trả về bản đồ hiện tại của trò chơi.
        return self.oWorld

    def get_mm(self):  # Trả về đối tượng MenuManager.
        return self.oMM

    def get_sound(self):  # Trả về đối tượng quản lý âm thanh.
        return self.oSound
