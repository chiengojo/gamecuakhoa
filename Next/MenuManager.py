import pygame as pg

from LoadingMenu import LoadingMenu
from MainMenu import MainMenu


class MenuManager(object):
    """
    Lớp này cho phép dễ dàng xử lý các trạng thái trò chơi.
    Tùy thuộc vào tình huống, nó sẽ cập nhật và vẽ các thành phần khác nhau.
    """
    def __init__(self, core):
        # Khởi tạo trạng thái trò chơi hiện tại là 'MainMenu'
        self.currentGameState = 'MainMenu'

        # Tạo đối tượng menu chính và menu tải
        self.oMainMenu = MainMenu()
        self.oLoadingMenu = LoadingMenu(core)

    def update(self, core):
        """Cập nhật theo trạng thái trò chơi hiện tại."""
        if self.currentGameState == 'MainMenu':
            # Trạng thái Menu chính, không làm gì ở đây
            pass

        elif self.currentGameState == 'Loading':
            # Nếu trạng thái là 'Loading', cập nhật màn hình tải
            self.oLoadingMenu.update(core)

        elif self.currentGameState == 'Game':
            # Nếu trạng thái là 'Game', cập nhật bản đồ trò chơi
            core.get_map().update(core)

    def render(self, core):
        """Vẽ các thành phần giao diện tương ứng với trạng thái trò chơi."""
        if self.currentGameState == 'MainMenu':
            # Trạng thái Menu chính: vẽ bản đồ và menu chính
            core.get_map().render_map(core)
            self.oMainMenu.render(core)

        elif self.currentGameState == 'Loading':
            # Trạng thái Loading: vẽ màn hình tải
            self.oLoadingMenu.render(core)

        elif self.currentGameState == 'Game':
            # Trạng thái Game: vẽ bản đồ và giao diện người chơi
            core.get_map().render(core)
            core.get_map().get_ui().render(core)

        # Cập nhật màn hình
        pg.display.update()

    def start_loading(self):
        """Chuyển sang trạng thái 'Loading' khi bắt đầu tải màn chơi."""
        self.currentGameState = 'Loading'
        self.oLoadingMenu.update_time()
