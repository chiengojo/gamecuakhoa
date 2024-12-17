import pygame as pg

from Entity import Entity
from Const import *


class Goombas(Entity):
    def __init__(self, x_pos, y_pos, move_direction):
        super().__init__()  # Gọi hàm khởi tạo của lớp cha (Entity)
        self.rect = pg.Rect(x_pos, y_pos, 32, 32)  # Tạo hình chữ nhật cho Goomba

        # Thiết lập vận tốc di chuyển theo hướng (1 là di chuyển phải, -1 là di chuyển trái)
        if move_direction:
            self.x_vel = 1
        else:
            self.x_vel = -1

        self.crushed = False  # Trạng thái của Goomba khi bị nghiền

        # Khởi tạo các hình ảnh cho Goomba
        self.current_image = 0
        self.image_tick = 0
        self.images = [
            pg.image.load('images/goombas_0.png').convert_alpha(),  # Hình ảnh Goomba đang sống
            pg.image.load('images/goombas_1.png').convert_alpha(),  # Hình ảnh Goomba đang sống (ảnh thứ 2)
            pg.image.load('images/goombas_dead.png').convert_alpha()  # Hình ảnh Goomba bị chết
        ]
        # Thêm hình ảnh của Goomba lật ngược
        self.images.append(pg.transform.flip(self.images[0], 0, 180))

    def die(self, core, instantly, crushed):
        # Hàm xử lý khi Goomba chết
        if not instantly:
            # Thêm điểm cho người chơi khi giết Goomba
            core.get_map().get_player().add_score(core.get_map().score_for_killing_mob)
            # Hiển thị điểm trên màn hình
            core.get_map().spawn_score_text(self.rect.x + 16, self.rect.y)

            # Nếu Goomba bị nghiền (nhảy lên trên đầu)
            if crushed:
                self.crushed = True
                self.image_tick = 0
                self.current_image = 2  # Hình ảnh Goomba bị nghiền
                self.state = -1  # Đánh dấu trạng thái của Goomba là chết
                core.get_sound().play('kill_mob', 0, 0.5)  # Phát âm thanh giết quái
                self.collision = False  # Không còn va chạm với Goomba

            # Nếu Goomba bị bắn ra (khi bị tấn công)
            else:
                self.y_vel = -4  # Đẩy Goomba lên trên một chút
                self.current_image = 3  # Hình ảnh Goomba bị bắn
                core.get_sound().play('shot', 0, 0.5)  # Phát âm thanh bắn
                self.state = -1  # Đánh dấu Goomba đã chết
                self.collision = False  # Không còn va chạm với Goomba

        else:
            core.get_map().get_mobs().remove(self)  # Nếu chết ngay lập tức, xóa Goomba khỏi bản đồ

    def check_collision_with_player(self, core):
        # Kiểm tra va chạm giữa Goomba và người chơi
        if self.collision:
            if self.rect.colliderect(core.get_map().get_player().rect):
                # Nếu Goomba chưa chết và người chơi nhảy xuống phía trên Goomba
                if self.state != -1:
                    if core.get_map().get_player().y_vel > 0:
                        # Goomba bị nghiền khi nhảy lên trên
                        self.die(core, instantly=False, crushed=True)
                        core.get_map().get_player().reset_jump()  # Reset nhảy của người chơi
                        core.get_map().get_player().jump_on_mob()  # Người chơi nhảy lên Goomba
                    else:
                        # Nếu không nhảy lên, người chơi bị trừ mạng
                        if not core.get_map().get_player().unkillable:
                            core.get_map().get_player().set_powerlvl(0, core)

    def update_image(self):
        # Cập nhật hình ảnh của Goomba theo thời gian
        self.image_tick += 1
        if self.image_tick == 14:
            self.current_image = 1  # Hình ảnh khi Goomba di chuyển
        elif self.image_tick == 28:
            self.current_image = 0  # Hình ảnh mặc định
            self.image_tick = 0  # Reset bộ đếm hình ảnh

    def update(self, core):
        # Cập nhật trạng thái và hành vi của Goomba
        if self.state == 0:  # Nếu Goomba còn sống
            self.update_image()  # Cập nhật hình ảnh

            if not self.on_ground:
                self.y_vel += GRAVITY  # Áp dụng lực trọng trường

            # Lấy các khối có thể va chạm với Goomba
            blocks = core.get_map().get_blocks_for_collision(int(self.rect.x // 32), int(self.rect.y // 32))
            self.update_x_pos(blocks)  # Cập nhật vị trí Goomba theo hướng x
            self.update_y_pos(blocks)  # Cập nhật vị trí Goomba theo hướng y

            self.check_map_borders(core)  # Kiểm tra Goomba có va chạm với biên bản đồ không

        elif self.state == -1:  # Nếu Goomba đã chết
            if self.crushed:
                # Nếu Goomba bị nghiền, đợi một thời gian rồi xóa khỏi bản đồ
                self.image_tick += 1
                if self.image_tick == 50:
                    core.get_map().get_mobs().remove(self)
            else:
                self.y_vel += GRAVITY  # Áp dụng lực trọng trường cho Goomba
                self.rect.y += self.y_vel  # Cập nhật vị trí y của Goomba
                self.check_map_borders(core)  # Kiểm tra Goomba có va chạm với biên bản đồ không

    def render(self, core):
        # Vẽ Goomba lên màn hình
        core.screen.blit(self.images[self.current_image], core.get_map().get_camera().apply(self))
