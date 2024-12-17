import pygame as pg  # Nhập thư viện Pygame và đặt bí danh là "pg".

class DebugTable(object):  # Định nghĩa lớp `DebugTable`, dùng để hiển thị thông tin debug.
    """
    Lớp này hiển thị các thông tin biến trong thời gian thực, giúp ích trong giai đoạn phát triển.
    """

    def __init__(self):  # Hàm khởi tạo lớp.
        self.font = pg.font.SysFont('Consolas', 12)  # Thiết lập font chữ "Consolas" với kích thước 12px.
        self.darkArea = pg.Surface((200, 100)).convert_alpha()  # Tạo một bề mặt mờ làm nền cho bảng thông tin.
        self.darkArea.fill((0, 0, 0, 200))  # Đặt màu nền là đen với độ mờ (alpha) là 200.
        self.text = []  # Danh sách chứa các chuỗi văn bản sẽ hiển thị.
        self.rect = 0  # Biến để lưu hình chữ nhật của từng dòng văn bản.
        self.offsetX = 12  # Khoảng cách dọc giữa các dòng.
        self.x = 5  # Tọa độ y bắt đầu của văn bản trên màn hình.
        self.mode = 2  # Chế độ hiển thị (chỉ có chế độ 2 đang được sử dụng).

    def update_text(self, core):  # Hàm cập nhật danh sách văn bản hiển thị.
        if self.mode == 2:  # Nếu chế độ là 2, cập nhật thông tin.
            self.text = [
                'FPS: ' + str(int(core.clock.get_fps())),  # Hiển thị số FPS hiện tại.
                'Rect: ' + str(core.get_map().get_player().rect.x) + ' ' +
                str(core.get_map().get_player().rect.y) + ' h: ' +
                str(core.get_map().get_player().rect.h),  # Vị trí và chiều cao của người chơi.
                'g: ' + str(core.get_map().get_player().on_ground) +
                ' LVL: ' + str(core.get_map().get_player().powerLVL) +
                ' inv: ' + str(core.get_map().get_player().unkillable),  # Trạng thái trên mặt đất, cấp độ sức mạnh, và trạng thái không thể bị tiêu diệt.
                'Spr: ' + str(core.get_map().get_player().spriteTick) +
                ' J lock: ' + str(core.get_map().get_player().already_jumped),  # Bộ đếm hoạt ảnh và trạng thái khóa nhảy.
                'Up  : ' + str(core.get_map().get_player().inLevelUpAnimation) +
                '  time: ' + str(core.get_map().get_player().inLevelUpAnimationTime),  # Hoạt ảnh tăng cấp và thời gian của nó.
                'Down: ' + str(core.get_map().get_player().inLevelDownAnimation) +
                '  time: ' + str(core.get_map().get_player().inLevelDownAnimationTime),  # Hoạt ảnh giảm cấp và thời gian của nó.
                'Mobs: ' + str(len(core.get_map().get_mobs())) +
                ' FB: ' + str(len(core.get_map().projectiles)) +
                ' Debris: ' + str(len(core.get_map().debris))  # Số lượng kẻ thù, đạn, và mảnh vỡ.
            ]

    def render(self, core):  # Hàm vẽ bảng thông tin lên màn hình.
        self.x = 105  # Tọa độ y bắt đầu vẽ bảng debug.
        if self.mode == 2:  # Nếu chế độ là 2.
            core.screen.blit(self.darkArea, (0, 100))  # Vẽ nền tối ở góc trên màn hình.
            for string in self.text:  # Lặp qua danh sách văn bản.
                self.rect = self.font.render(string, True, (255, 255, 255))  # Tạo bề mặt cho chuỗi văn bản (màu trắng).
                core.screen.blit(self.rect, (5, self.x))  # Vẽ chuỗi lên màn hình tại tọa độ xác định.
                self.x += self.offsetX  # Tăng tọa độ y cho dòng tiếp theo.
