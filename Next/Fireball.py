import pygame as pg

from Const import *


class Fireball(object):
    """
    Lớp đại diện cho quả cầu lửa (fireball) trong trò chơi.
    """
    def __init__(self, x_pos, y_pos, move_direction: bool):
        # Khởi tạo vị trí, vận tốc, và hình ảnh ban đầu của quả cầu lửa.
        super().__init__()

        # Hình chữ nhật đại diện cho vị trí và kích thước của fireball.
        self.rect = pg.Rect(x_pos, y_pos, 16, 16)

        # Trạng thái của fireball: 0 = bình thường, -1 = phát nổ.
        self.state = 0

        # Hướng di chuyển: True = phải, False = trái.
        self.direction = move_direction

        # Vận tốc trên trục x và y.
        self.x_vel = 5 if move_direction else -5  # Tốc độ dựa trên hướng.
        self.y_vel = 0

        # Hình ảnh hiện tại và bộ đếm cho hoạt ảnh.
        self.current_image = 0
        self.image_tick = 0

        # Tải hình ảnh và các biến thể lật của quả cầu lửa.
        self.images = [pg.image.load('images/fireball.png').convert_alpha()]
        self.images.append(pg.transform.flip(self.images[0], 0, 90))  # Lật 90 độ theo trục y.
        self.images.append(pg.transform.flip(self.images[0], 90, 90))  # Lật 90 độ theo cả hai trục.
        self.images.append(pg.transform.flip(self.images[0], 90, 0))  # Lật 90 độ theo trục x.
        self.images.append(pg.image.load('images/firework0.png').convert_alpha())  # Hình phát nổ 1.
        self.images.append(pg.image.load('images/firework1.png').convert_alpha())  # Hình phát nổ 2.
        self.images.append(pg.image.load('images/firework2.png').convert_alpha())  # Hình phát nổ 3.

    def update_image(self, core):
        """
        Cập nhật hình ảnh dựa trên trạng thái và thời gian.
        """
        self.image_tick += 1

        if self.state == 0:  # Trạng thái di chuyển bình thường.
            if self.image_tick % 15 == 0:  # Thay đổi hình ảnh mỗi 15 tick.
                self.current_image += 1
                if self.current_image > 3:
                    self.current_image = 0
                    self.image_tick = 0
        elif self.state == -1:  # Trạng thái phát nổ.
            if self.image_tick % 10 == 0:  # Thay đổi hình ảnh mỗi 10 tick.
                self.current_image += 1
            if self.current_image == 7:  # Khi hình ảnh phát nổ kết thúc.
                core.get_map().remove_whizbang(self)  # Xóa fireball khỏi bản đồ.

    def start_boom(self):
        """
        Kích hoạt trạng thái phát nổ.
        """
        self.x_vel = 0  # Ngừng di chuyển.
        self.y_vel = 0
        self.current_image = 4  # Bắt đầu từ hình ảnh phát nổ đầu tiên.
        self.image_tick = 0
        self.state = -1  # Đặt trạng thái phát nổ.

    def update_x_pos(self, blocks):
        """
        Cập nhật vị trí x và kiểm tra va chạm ngang.
        """
        self.rect.x += self.x_vel  # Di chuyển theo trục x.

        for block in blocks:
            if block != 0 and block.type != 'BGObject':  # Chỉ kiểm tra va chạm với các khối có thể va chạm.
                if pg.Rect.colliderect(self.rect, block.rect):  # Nếu có va chạm:
                    self.start_boom()  # Kích hoạt phát nổ.

    def update_y_pos(self, blocks):
        """
        Cập nhật vị trí y và kiểm tra va chạm dọc.
        """
        self.rect.y += self.y_vel  # Di chuyển theo trục y.

        for block in blocks:
            if block != 0 and block.type != 'BGObject':  # Chỉ kiểm tra va chạm với các khối có thể va chạm.
                if pg.Rect.colliderect(self.rect, block.rect):  # Nếu có va chạm:
                    self.rect.bottom = block.rect.top  # Đặt quả cầu lửa lên trên khối.
                    self.y_vel = -3  # Bật ngược lại nhẹ.

    def check_map_borders(self, core):
        """
        Kiểm tra xem quả cầu lửa có ra ngoài bản đồ không.
        """
        if self.rect.x <= 0 or self.rect.x >= 6768 or self.rect.y > 448:
            core.get_map().remove_whizbang(self)  # Nếu ra ngoài bản đồ, xóa khỏi bản đồ.

    def move(self, core):
        """
        Cập nhật vị trí di chuyển của fireball.
        """
        self.y_vel += GRAVITY  # Áp dụng trọng lực.

        # Lấy danh sách các khối gần fireball để kiểm tra va chạm.
        blocks = core.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
        self.update_y_pos(blocks)  # Cập nhật vị trí dọc.
        self.update_x_pos(blocks)  # Cập nhật vị trí ngang.

        self.check_map_borders(core)  # Kiểm tra giới hạn bản đồ.

    def check_collision_with_mobs(self, core):
        """
        Kiểm tra va chạm với kẻ địch (mobs).
        """
        for mob in core.get_map().get_mobs():
            if self.rect.colliderect(mob.rect):  # Nếu có va chạm với mob:
                if mob.collision:  # Nếu mob có thể va chạm:
                    mob.die(core, instantly=False, crushed=False)  # Mob chết.
                    self.start_boom()  # Fireball phát nổ.

    def update(self, core):
        """
        Cập nhật trạng thái và hành vi của fireball.
        """
        if self.state == 0:  # Nếu đang trong trạng thái di chuyển.
            self.update_image(core)  # Cập nhật hoạt ảnh.
            self.move(core)  # Di chuyển.
            self.check_collision_with_mobs(core)  # Kiểm tra va chạm với mobs.
        elif self.state == -1:  # Nếu đang trong trạng thái phát nổ.
            self.update_image(core)  # Cập nhật hoạt ảnh phát nổ.

    def render(self, core):
        """
        Vẽ hình ảnh fireball lên màn hình.
        """
        # Áp dụng góc nhìn camera và vẽ hình ảnh hiện tại.
        core.screen.blit(self.images[self.current_image], core.get_map().get_camera().apply(self))
