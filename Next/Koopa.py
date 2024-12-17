import pygame as pg

from Entity import Entity
from Const import *


class Koopa(Entity):
    def __init__(self, x_pos, y_pos, move_direction):
        super().__init__()  # Gọi hàm khởi tạo của lớp cha (Entity)
        self.rect = pg.Rect(x_pos, y_pos, 32, 46)  # Tạo hình chữ nhật cho Koopa với kích thước 32x46

        self.move_direction = move_direction  # Hướng di chuyển của Koopa

        # Thiết lập vận tốc di chuyển theo hướng
        if move_direction:
            self.x_vel = 1
        else:
            self.x_vel = -1

        self.current_image = 0  # Hình ảnh hiện tại của Koopa
        self.image_tick = 0  # Bộ đếm thời gian cho hình ảnh
        self.images = [
            pg.image.load('images/koopa_0.png').convert_alpha(),  # Hình ảnh Koopa di chuyển bình thường
            pg.image.load('images/koopa_1.png').convert_alpha(),  # Hình ảnh Koopa di chuyển bình thường (ảnh thứ 2)
            pg.image.load('images/koopa_dead.png').convert_alpha()  # Hình ảnh Koopa khi chết
        ]
        # Thêm các hình ảnh Koopa khi quay lật (flip)
        self.images.append(pg.transform.flip(self.images[0], 180, 0))
        self.images.append(pg.transform.flip(self.images[1], 180, 0))
        self.images.append(pg.transform.flip(self.images[2], 0, 180))

    """
    Các trạng thái của Koopa:
    0 - Di chuyển bình thường
    1 - Ẩn
    2 - Ẩn và di chuyển nhanh
    -1 - Chết
    """

    def check_collision_with_player(self, core):
        # Kiểm tra va chạm giữa Koopa và người chơi
        if self.collision:
            if self.rect.colliderect(core.get_map().get_player().rect):
                if self.state != -1:  # Nếu Koopa chưa chết
                    if core.get_map().get_player().y_vel > 0:  # Người chơi nhảy lên Koopa
                        self.change_state(core)  # Thay đổi trạng thái của Koopa
                        core.get_sound().play('kill_mob', 0, 0.5)  # Phát âm thanh giết quái
                        core.get_map().get_player().reset_jump()  # Reset nhảy của người chơi
                        core.get_map().get_player().jump_on_mob()  # Người chơi nhảy lên Koopa
                    else:
                        # Nếu không nhảy, người chơi bị trừ mạng
                        if not core.get_map().get_player().unkillable:
                            core.get_map().get_player().set_powerlvl(0, core)

    def check_collision_with_mobs(self, core):
        # Kiểm tra va chạm giữa Koopa và các mob khác
        for mob in core.get_map().get_mobs():
            if mob is not self:  # Tránh va chạm với chính Koopa
                if self.rect.colliderect(mob.rect):  # Kiểm tra va chạm
                    if mob.collision:
                        mob.die(core, instantly=False, crushed=False)  # Xử lý khi va chạm với mob khác

    def die(self, core, instantly, crushed):
        # Xử lý khi Koopa chết
        if not instantly:
            core.get_map().get_player().add_score(core.get_map().score_for_killing_mob)  # Thêm điểm cho người chơi
            core.get_map().spawn_score_text(self.rect.x + 16, self.rect.y)  # Hiển thị điểm trên màn hình
            self.state = -1  # Đánh dấu trạng thái chết
            self.y_vel = -4  # Đẩy Koopa lên một chút
            self.current_image = 5  # Hình ảnh Koopa khi chết
        else:
            core.get_map().get_mobs().remove(self)  # Xóa Koopa khỏi bản đồ

    def change_state(self, core):
        # Thay đổi trạng thái của Koopa
        self.state += 1
        self.current_image = 2  # Hình ảnh khi Koopa bị tấn công

        # Chuyển từ trạng thái 0 sang 1 (Koopa bị ẩn)
        if self.rect.h == 46:
            self.x_vel = 0  # Dừng lại khi bị ẩn
            self.rect.h = 32  # Thay đổi chiều cao của Koopa khi ẩn
            self.rect.y += 14  # Di chuyển Koopa lên
            core.get_map().get_player().add_score(100)  # Thêm điểm cho người chơi
            core.get_map().spawn_score_text(self.rect.x + 16, self.rect.y, score=100)

        # Chuyển từ trạng thái 1 sang 2 (Koopa di chuyển nhanh)
        elif self.state == 2:
            core.get_map().get_player().add_score(100)  # Thêm điểm cho người chơi
            core.get_map().spawn_score_text(self.rect.x + 16, self.rect.y, score=100)

            # Xác định hướng di chuyển của Koopa
            if core.get_map().get_player().rect.x - self.rect.x <= 0:
                self.x_vel = 6  # Di chuyển sang phải
            else:
                self.x_vel = -6  # Di chuyển sang trái

        # Chuyển từ trạng thái 2 sang 3 (Koopa chết)
        elif self.state == 3:
            self.die(core, instantly=False, crushed=False)

    def update_image(self):
        # Cập nhật hình ảnh của Koopa theo thời gian
        self.image_tick += 1

        # Xác định hướng di chuyển của Koopa
        if self.x_vel > 0:
            self.move_direction = True  # Di chuyển sang phải
        else:
            self.move_direction = False  # Di chuyển sang trái

        # Cập nhật hình ảnh dựa trên bộ đếm thời gian
        if self.image_tick == 35:
            if self.move_direction:
                self.current_image = 4  # Hình ảnh Koopa di chuyển sang phải
            else:
                self.current_image = 1  # Hình ảnh Koopa di chuyển sang trái
        elif self.image_tick == 70:
            if self.move_direction:
                self.current_image = 3  # Hình ảnh Koopa di chuyển sang phải (ảnh thứ 2)
            else:
                self.current_image = 0  # Hình ảnh Koopa di chuyển sang trái (ảnh thứ 2)
            self.image_tick = 0  # Reset bộ đếm hình ảnh

    def update(self, core):
        # Cập nhật trạng thái và hành vi của Koopa
        if self.state == 0:  # Nếu Koopa còn sống và đang di chuyển bình thường
            self.update_image()  # Cập nhật hình ảnh

            if not self.on_ground:
                self.y_vel += GRAVITY  # Áp dụng trọng lực

            # Lấy các khối có thể va chạm với Koopa
            blocks = core.get_map().get_blocks_for_collision(self.rect.x // 32, (self.rect.y - 14) // 32)
            self.update_x_pos(blocks)  # Cập nhật vị trí theo trục x
            self.update_y_pos(blocks)  # Cập nhật vị trí theo trục y

            self.check_map_borders(core)  # Kiểm tra va chạm với biên bản đồ

        elif self.state == 1:  # Nếu Koopa bị ẩn
            blocks = core.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
            self.update_x_pos(blocks)
            self.update_y_pos(blocks)

            self.check_map_borders(core)

        elif self.state == 2:  # Nếu Koopa di chuyển nhanh
            if not self.on_ground:
                self.y_vel += GRAVITY  # Áp dụng trọng lực

            blocks = core.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
            self.update_x_pos(blocks)
            self.update_y_pos(blocks)

            self.check_map_borders(core)
            self.check_collision_with_mobs(core)  # Kiểm tra va chạm với các mob khác

        elif self.state == -1:  # Nếu Koopa đã chết
            self.rect.y += self.y_vel
            self.y_vel += GRAVITY  # Áp dụng trọng lực

            self.check_map_borders(core)

    def render(self, core):
        # Vẽ Koopa lên màn hình
        core.screen.blit(self.images[self.current_image], core.get_map().get_camera().apply(self))
