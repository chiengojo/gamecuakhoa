import pygame as pg
from Entity import Entity  # Đảm bảo Entity được định nghĩa đúng
from Const import *  # Kiểm tra xem các hằng số như GRAVITY, v.v có tồn tại không

class Mushroom(Entity):
    def __init__(self, x_pos, y_pos, move_direction):
        super().__init__()  # Gọi constructor của lớp cha (Entity)

        # Khởi tạo rect (hình chữ nhật) đại diện cho nấm với kích thước 32x32
        self.rect = pg.Rect(x_pos, y_pos, 32, 32)

        # Đặt vận tốc di chuyển của nấm trên trục x tùy vào hướng di chuyển
        if move_direction:
            self.x_vel = 1  # Di chuyển sang phải
        else:
            self.x_vel = -1  # Di chuyển sang trái

        # Thuộc tính theo dõi việc nấm đã được tạo ra chưa
        self.spawned = False
        self.spawn_y_offset = 0  # Để điều khiển việc nấm xuất hiện

        # Nạp hình ảnh của nấm, đảm bảo tệp hình ảnh tồn tại trong thư mục đúng
        try:
            self.image = pg.image.load('images/mushroom.png').convert_alpha()  # Nạp hình ảnh nấm
        except FileNotFoundError:  # Nếu không tìm thấy tệp hình ảnh, in thông báo lỗi
            print("Error: Image 'images/mushroom.png' not found!")

    def check_collision_with_player(self, core):
        """Kiểm tra va chạm với người chơi."""
        if self.rect.colliderect(core.get_map().get_player().rect):  # Kiểm tra va chạm với người chơi
            core.get_map().get_player().set_powerlvl(2, core)  # Tăng cấp cho người chơi
            core.get_map().get_mobs().remove(self)  # Loại bỏ nấm khỏi danh sách mob

    def die(self, core, instantly, crushed):
        """Xử lý khi nấm bị tiêu diệt."""
        core.get_map().get_mobs().remove(self)  # Loại bỏ nấm khỏi danh sách mob khi chết

    def spawn_animation(self):
        """Hoạt ảnh khi nấm xuất hiện (di chuyển lên trên)."""
        self.spawn_y_offset -= 1  # Tạo hiệu ứng nấm nhảy lên
        self.rect.y -= 1  # Di chuyển nấm lên trên

        # Khi nấm đã nhảy lên đủ, đánh dấu là đã xuất hiện
        if self.spawn_y_offset == -32:
            self.spawned = True

    def update(self, core):
        """Cập nhật trạng thái và di chuyển của nấm."""
        if self.spawned:  # Nếu nấm đã xuất hiện
            if not self.on_ground:  # Nếu nấm chưa chạm đất, áp dụng trọng lực
                self.y_vel += GRAVITY

            # Kiểm tra va chạm với các khối trên bản đồ
            blocks = core.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
            self.update_x_pos(blocks)  # Cập nhật vị trí theo trục x
            self.update_y_pos(blocks)  # Cập nhật vị trí theo trục y

            # Kiểm tra các biên giới bản đồ (ví dụ: nếu nấm ra ngoài màn hình)
            self.check_map_borders(core)
        else:
            # Nếu nấm chưa xuất hiện, thực hiện hoạt ảnh xuất hiện
            self.spawn_animation()

    def render(self, core):
        """Vẽ nấm lên màn hình."""
        core.screen.blit(self.image, core.get_map().get_camera().apply(self))  # Vẽ nấm lên màn hình
