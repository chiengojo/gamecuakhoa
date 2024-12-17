import pygame as pg

from Entity import Entity


class Flower(Entity):
    """
    Lớp đại diện cho loài hoa trong trò chơi.
    """
    def __init__(self, x_pos, y_pos):
        super().__init__()

        # Khởi tạo các thuộc tính của hoa, bao gồm vị trí và trạng thái ban đầu.
        self.rect = pg.Rect(x_pos, y_pos, 32, 32)  # Hình chữ nhật đại diện cho hoa.
        self.spawned = False  # Trạng thái của hoa: False = chưa xuất hiện, True = đã xuất hiện.
        self.spawn_y_offset = 0  # Độ dịch chuyển dọc của hoa khi xuất hiện.

        # Hình ảnh của hoa trong các trạng thái khác nhau.
        self.current_image = 0
        self.image_tick = 0
        self.images = (
            pg.image.load('images/flower0.png').convert_alpha(),
            pg.image.load('images/flower1.png').convert_alpha(),
            pg.image.load('images/flower2.png').convert_alpha(),
            pg.image.load('images/flower3.png').convert_alpha()
        )

    def check_collision_with_player(self, core):
        """
        Kiểm tra va chạm với người chơi.
        Nếu hoa va chạm với người chơi, tăng cấp độ sức mạnh của người chơi và xóa hoa.
        """
        if self.rect.colliderect(core.get_map().get_player().rect):
            core.get_map().get_player().set_powerlvl(3, core)  # Tăng cấp độ sức mạnh của người chơi.
            core.get_map().get_mobs().remove(self)  # Loại bỏ hoa khỏi danh sách các mob.

    def update_image(self):
        """
        Cập nhật hình ảnh của hoa theo thời gian.
        Sau mỗi 15 tick, hoa thay đổi hình ảnh.
        """
        self.image_tick += 1

        if self.image_tick == 60:  # Sau 60 tick, đặt lại hình ảnh về 0.
            self.image_tick = 0
            self.current_image = 0

        elif self.image_tick % 15 == 0:  # Mỗi 15 tick, thay đổi hình ảnh.
            self.current_image += 1

    def spawn_animation(self):
        """
        Hoạt ảnh khi hoa xuất hiện, di chuyển lên trên.
        """
        self.spawn_y_offset -= 1  # Tăng độ dịch chuyển lên trên.
        self.rect.y -= 1  # Di chuyển hoa lên trên.

        # Nếu hoa đã hoàn thành hoạt ảnh, đánh dấu là đã xuất hiện.
        if self.spawn_y_offset == -32:
            self.spawned = True

    def update(self, core):
        """
        Cập nhật trạng thái của hoa.
        Nếu hoa đã xuất hiện, cập nhật hình ảnh. Nếu chưa, chạy hoạt ảnh xuất hiện.
        """
        if self.spawned:
            self.update_image()
        else:
            self.spawn_animation()

    def render(self, core):
        """
        Vẽ hoa lên màn hình.
        """
        core.screen.blit(self.images[self.current_image], core.get_map().get_camera().apply(self))
