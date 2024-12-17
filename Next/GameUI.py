import pygame as pg


class GameUI(object):
    def __init__(self):
        # Khởi tạo font chữ sử dụng trong UI
        # Sử dụng font 'emulogic.ttf' với kích thước 20
        self.font = pg.font.Font('fonts/emulogic.ttf', 20)
        
        # Đoạn văn bản sẽ hiển thị: các tiêu đề cho các chỉ số (SCORE, COINS, WORLD, TIME, LIVES)
        self.text = 'SCORE SERVO WORLD TIME LIVES'

    def render(self, core):
        # Xác định vị trí ban đầu cho văn bản
        x = 10
        
        # Vòng lặp này chia đoạn văn bản thành các từ riêng biệt và hiển thị từng từ trên màn hình
        for word in self.text.split(' '):
            rect = self.font.render(word, False, (255, 255, 255))  # Render từng từ với màu trắng
            core.screen.blit(rect, (x, 0))  # Hiển thị từ tại vị trí x, 0
            x += 168  # Dịch chuyển vị trí x để từ tiếp theo không chồng lên nhau

        # Hiển thị điểm số (SCORE)
        text = self.font.render(str(core.get_map().get_player().score), False, (255, 255, 255))
        rect = text.get_rect(center=(60, 35))  # Căn giữa văn bản tại vị trí (60, 35)
        core.screen.blit(text, rect)  # Vẽ lên màn hình

        # Hiển thị số luong servo (servo)
        text = self.font.render(str(core.get_map().get_player().coins), False, (255, 255, 255))
        rect = text.get_rect(center=(230, 35))  # Căn giữa văn bản tại vị trí (230, 35)
        core.screen.blit(text, rect)  # Vẽ lên màn hình

        # Hiển thị tên của thế giới (WORLD)
        text = self.font.render(core.get_map().get_name(), False, (255, 255, 255))
        rect = text.get_rect(center=(395, 35))  # Căn giữa văn bản tại vị trí (395, 35)
        core.screen.blit(text, rect)  # Vẽ lên màn hình

        # Hiển thị thời gian còn lại (TIME)
        text = self.font.render(str(core.get_map().time), False, (255, 255, 255))
        rect = text.get_rect(center=(557, 35))  # Căn giữa văn bản tại vị trí (557, 35)
        core.screen.blit(text, rect)  # Vẽ lên màn hình

        # Hiển thị số mạng còn lại (LIVES)
        text = self.font.render(str(core.get_map().get_player().numOfLives), False, (255, 255, 255))
        rect = text.get_rect(center=(730, 35))  # Căn giữa văn bản tại vị trí (730, 35)
        core.screen.blit(text, rect)  # Vẽ lên màn hình
