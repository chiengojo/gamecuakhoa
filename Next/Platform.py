import pygame as pg

class Platform(object):
    def __init__(self, x, y, image, type_id):
        # Khởi tạo platform với vị trí (x, y), hình ảnh và loại platform (type_id)
        self.image = image  # Hình ảnh của platform
        self.rect = pg.Rect(x, y, 32, 32)  # Tạo một đối tượng rect cho platform với kích thước 32x32

        # 22 - question block
        # 23 - brick block
        self.typeID = type_id  # Loại platform (22 cho question block, 23 cho brick block)

        self.type = 'Platform'  # Loại đối tượng là platform

        # Các thuộc tính cho hiệu ứng rung của platform khi người chơi tương tác
        self.shaking = False  # Đánh dấu nếu platform đang rung
        self.shakingUp = True  # Đánh dấu nếu platform đang di chuyển lên
        self.shakeOffset = 0  # Độ dịch chuyển khi rung

        if self.typeID == 22:
            # Nếu là question block (typeID == 22), khởi tạo các thuộc tính liên quan đến animation
            self.currentImage = 0  # Chỉ số hình ảnh hiện tại
            self.imageTick = 0  # Biến đếm thời gian cho hoạt ảnh
            self.isActivated = False  # Đánh dấu nếu question block đã được kích hoạt
            self.bonus = 'coin'  # Phần thưởng mặc định là đồng xu

    def update(self):
        # Cập nhật trạng thái của platform
        if self.typeID == 22:
            # Nếu là question block, cập nhật hoạt ảnh của block
            self.imageTick += 1
            if self.imageTick == 50:
                self.currentImage = 1  # Đổi hình ảnh sau 50 bước
            elif self.imageTick == 60:
                self.currentImage = 2  # Đổi hình ảnh sau 60 bước
            elif self.imageTick == 70:
                self.currentImage = 1  # Đổi hình ảnh sau 70 bước
            elif self.imageTick == 80:
                self.currentImage = 0  # Quay lại hình ảnh ban đầu sau 80 bước
                self.imageTick = 0  # Reset biến đếm

    def shake(self):
        # Xử lý hiệu ứng rung của platform
        if self.shakingUp:
            # Di chuyển platform lên
            self.shakeOffset -= 2
            self.rect.y -= 2
        else:
            # Di chuyển platform xuống
            self.shakeOffset += 2
            self.rect.y += 2
        if self.shakeOffset == -20:
            # Khi đã di chuyển lên đủ, bắt đầu di chuyển xuống
            self.shakingUp = False
        if self.shakeOffset == 0:
            # Khi hoàn thành hiệu ứng rung, dừng rung và đặt trạng thái quay lại ban đầu
            self.shaking = False
            self.shakingUp = True

    def spawn_bonus(self, core):
        # Khi platform được kích hoạt, spawn phần thưởng
        self.isActivated = True  # Đánh dấu platform đã được kích hoạt
        self.shaking = True  # Bắt đầu hiệu ứng rung
        self.imageTick = 0  # Reset biến đếm hoạt ảnh
        self.currentImage = 3  # Chuyển sang hình ảnh phần thưởng

        if self.bonus == 'mushroom':
            # Nếu phần thưởng là nấm, tạo nấm trong game
            core.get_sound().play('mushroom_appear', 0, 0.5)  # Phát âm thanh nấm xuất hiện
            if core.get_map().get_player().powerLVL == 0:
                # Nếu người chơi chưa có power-up, spawn mushroom
                core.get_map().spawn_mushroom(self.rect.x, self.rect.y)
            else:
                # Nếu người chơi đã có power-up, spawn flower
                core.get_map().spawn_flower(self.rect.x, self.rect.y)

        elif self.bonus == 'coin':
            # Nếu phần thưởng là đồng xu, tạo đồng xu trong game
            core.get_sound().play('coin', 0, 0.5)  # Phát âm thanh đồng xu
            core.get_map().spawn_debris(self.rect.x + 8, self.rect.y - 32, 1)  # Tạo vụn đồng xu
            core.get_map().get_player().add_coins(1)  # Tăng số lượng đồng xu của người chơi
            core.get_map().get_player().add_score(200)  # Tăng điểm của người chơi

    def destroy(self, core):
        # Khi platform bị phá hủy, tạo vụn debris và loại bỏ platform khỏi game
        core.get_map().spawn_debris(self.rect.x, self.rect.y, 0)  # Tạo vụn debris
        core.get_map().remove_object(self)  # Loại bỏ platform khỏi bản đồ

    def render(self, core):
        # Vẽ platform lên màn hình
        if self.typeID == 22:
            # Nếu là question block
            if not self.isActivated:
                self.update()  # Cập nhật hoạt ảnh nếu chưa được kích hoạt
            elif self.shaking:
                self.shake()  # Nếu platform đang rung, áp dụng hiệu ứng rung
            core.screen.blit(self.image[self.currentImage], core.get_map().get_camera().apply(self))  # Vẽ hình ảnh của question block

        elif self.typeID == 23 and self.shaking:
            # Nếu là brick block và đang rung
            self.shake()  # Áp dụng hiệu ứng rung
            core.screen.blit(self.image, core.get_map().get_camera().apply(self))  # Vẽ hình ảnh của brick block

        else:
            # Nếu không phải question block hoặc brick block, vẽ hình ảnh bình thường
            core.screen.blit(self.image, core.get_map().get_camera().apply(self))  # Vẽ hình ảnh của platform
