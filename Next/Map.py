import pygame as pg  # Thư viện chính để tạo game 2D
from pytmx.util_pygame import load_pygame  # Hỗ trợ đọc file bản đồ .tmx (dùng Tiled Map Editor)

# Import các file khác quản lý đối tượng, UI, kẻ địch, sự kiện
from GameUI import GameUI  # Hiển thị giao diện (thời gian, điểm số, mạng sống)
from BGObject import BGObject  # Các đối tượng nền
from Camera import Camera  # Xử lý camera di chuyển theo người chơi
from Event import Event  # Quản lý sự kiện (ví dụ: kết thúc màn chơi)
from Flag import Flag  # Lá cờ kết thúc game
from Const import *  # Chứa các hằng số cho game (ví dụ: WINDOW_W, WINDOW_H)
from Platform import Platform  # Xử lý các khối (block) trong bản đồ
from Player import Player  # Người chơi (Mario)
from Goombas import Goombas  # Kẻ địch Goombas
from Mushroom import Mushroom  # Nấm giúp Mario tăng sức mạnh
from Flower import Flower  # Hoa giúp Mario bắn đạn lửa
from Koopa import Koopa  # Kẻ địch Koopa
from Tube import Tube  # Ống nước
from PlatformDebris import PlatformDebris  # Mảnh vỡ khi khối bị phá hủy
from CoinDebris import CoinDebris  # Mảnh vỡ khi đồng xu bị thu thập
from Fireball import Fireball  # Đạn lửa của Mario
from Text import Text  # Hiển thị văn bản (ví dụ: điểm số nổi)

class Map(object):
    """
    Lớp Map quản lý toàn bộ các đối tượng trên bản đồ như gạch, mob, người chơi,
    cùng với camera, sự kiện, và giao diện người chơi (UI).
    """

    def __init__(self, world_num):
        """
        Khởi tạo bản đồ với các danh sách để lưu trữ các đối tượng và trạng thái trò chơi.
        """
        self.obj = []  # Danh sách các đối tượng trên bản đồ.
        self.obj_bg = []  # Danh sách các đối tượng nền.
        self.tubes = []  # Danh sách các ống (tube).
        self.debris = []  # Danh sách các mảnh vụn (debris) khi phá gạch hoặc khối hỏi chấm.
        self.mobs = []  # Danh sách các mob (quái vật).
        self.projectiles = []  # Danh sách các đạn lửa (projectiles).
        self.text_objects = []  # Danh sách các đối tượng văn bản (như điểm số).
        self.map = 0  # Dữ liệu bản đồ dưới dạng 2D.
        self.flag = None  # Cờ (flag) khi người chơi hoàn thành màn chơi.

        self.mapSize = (0, 0)  # Kích thước bản đồ.
        self.sky = 0  # Bầu trời nền.

        self.textures = {}  # Các texture được sử dụng trên bản đồ.
        self.worldNum = world_num  # Số màn chơi (world).

        self.loadWorld_11()  # Tải bản đồ cho màn chơi cụ thể.

        self.is_mob_spawned = [False, False]  # Trạng thái sinh mob.
        self.score_for_killing_mob = 100  # Điểm số khi tiêu diệt mob.
        self.score_time = 0  # Điểm số dựa trên thời gian.

        self.in_event = False  # Trạng thái sự kiện (đang xảy ra sự kiện).
        self.tick = 0  # Đếm số khung hình (frames).
        self.time = 400  # Thời gian giới hạn của màn chơi.

        self.oPlayer = Player(x_pos=128, y_pos=351)  # Khởi tạo đối tượng người chơi.
        self.oCamera = Camera(self.mapSize[0] * 32, 14)  # Khởi tạo camera.
        self.oEvent = Event()  # Khởi tạo đối tượng sự kiện.
        self.oGameUI = GameUI()  # Khởi tạo giao diện người chơi (UI).

    def loadWorld_11(self):
        """
        Tải dữ liệu bản đồ từ tệp .tmx và khởi tạo các đối tượng tương ứng.
        """
        tmx_data = load_pygame("worlds/1-1/W11.tmx")  # Tải tệp bản đồ.
        self.mapSize = (tmx_data.width, tmx_data.height)  # Lấy kích thước bản đồ.

        self.sky = pg.Surface((WINDOW_W, WINDOW_H))  # Khởi tạo bầu trời nền.
        self.sky.fill((pg.Color('#5c94fc')))  # Tô màu bầu trời.

        # Khởi tạo danh sách 2D để lưu thông tin gạch trên bản đồ.
        self.map = [[0] * tmx_data.height for i in range(tmx_data.width)]

        layer_num = 0  # Chỉ số layer trong tệp .tmx.
        for layer in tmx_data.visible_layers:  # Duyệt qua tất cả các lớp hiển thị.
            for y in range(tmx_data.height):  # Duyệt qua từng hàng.
                for x in range(tmx_data.width):  # Duyệt qua từng cột.

                    # Lấy hình ảnh từ tile.
                    image = tmx_data.get_tile_image(x, y, layer_num)

                    # Nếu không có tile tại vị trí này thì bỏ qua.
                    if image is not None:
                        tileID = tmx_data.get_tile_gid(x, y, layer_num)

                        if layer.name == 'Foreground':  # Lớp nền trước.
                            # Nếu là khối hỏi chấm (ID 22), tải toàn bộ trạng thái của nó.
                            if tileID == 22:
                                image = (
                                    image,  # Trạng thái ban đầu.
                                    tmx_data.get_tile_image(0, 15, layer_num),  # Trạng thái 1.
                                    tmx_data.get_tile_image(1, 15, layer_num),  # Trạng thái 2.
                                    tmx_data.get_tile_image(2, 15, layer_num)  # Trạng thái kích hoạt.
                                )

                            # Lưu thông tin vào danh sách "map" để xử lý va chạm
                            # và danh sách "obj" để hiển thị.
                            self.map[x][y] = Platform(x * tmx_data.tileheight, y * tmx_data.tilewidth, image, tileID)
                            self.obj.append(self.map[x][y])

                        elif layer.name == 'Background':  # Lớp nền sau.
                            self.map[x][y] = BGObject(x * tmx_data.tileheight, y * tmx_data.tilewidth, image)
                            self.obj_bg.append(self.map[x][y])
            layer_num += 1

        # Khởi tạo các ống (tube) tại các vị trí xác định.
        self.spawn_tube(28, 10)
        self.spawn_tube(37, 9)
        self.spawn_tube(46, 8)
        self.spawn_tube(55, 8)
        self.spawn_tube(163, 10)
        self.spawn_tube(179, 10)

        # Khởi tạo mob (Goombas) tại các vị trí xác định.
        self.mobs.append(Goombas(736, 352, False))
        self.mobs.append(Goombas(1295, 352, True))
        self.mobs.append(Goombas(1632, 352, False))
        self.mobs.append(Goombas(1672, 352, False))
        self.mobs.append(Goombas(5570, 352, False))
        self.mobs.append(Goombas(5620, 352, False))

        # Gán phần thưởng (mushroom) cho các khối cụ thể.
        self.map[21][8].bonus = 'mushroom'
        self.map[78][8].bonus = 'mushroom'
        self.map[109][4].bonus = 'mushroom'

        self.flag = Flag(6336, 48)  # Đặt cờ (flag) khi hoàn thành màn chơi.

    def reset(self, reset_all):
        """
        Reset trạng thái bản đồ về ban đầu.
        """
        self.obj = []  # Xóa danh sách các đối tượng.
        self.obj_bg = []  # Xóa danh sách các đối tượng nền.
        self.tubes = []  # Xóa danh sách các ống.
        self.debris = []  # Xóa danh sách các mảnh vụn.
        self.mobs = []  # Xóa danh sách mob.
        self.is_mob_spawned = [False, False]  # Reset trạng thái sinh mob.

        self.in_event = False  # Tắt trạng thái sự kiện.
        self.flag = None  # Reset cờ.
        self.sky = None  # Reset bầu trời nền.
        self.map = None  # Reset dữ liệu bản đồ.

        self.tick = 0  # Reset bộ đếm khung hình.
        self.time = 400  # Reset thời gian chơi.

        self.mapSize = (0, 0)  # Reset kích thước bản đồ.
        self.textures = {}  # Xóa các texture.

        self.loadWorld_11()  # Tải lại bản đồ ban đầu.

        self.get_event().reset()  # Reset sự kiện.
        self.get_player().reset(reset_all)  # Reset trạng thái người chơi.
        self.get_camera().reset()  # Reset camera.


    def get_name(self):
        if self.worldNum == '1-1':
            return '1-1'

    def get_player(self):
        return self.oPlayer

    def get_camera(self):
        return self.oCamera

    def get_event(self):
        return self.oEvent

    def get_ui(self):
        return self.oGameUI

    def get_blocks_for_collision(self, x, y):
        """

        Returns tiles around the entity

        """
        return (
            self.map[x][y - 1],
            self.map[x][y + 1],
            self.map[x][y],
            self.map[x - 1][y],
            self.map[x + 1][y],
            self.map[x + 2][y],
            self.map[x + 1][y - 1],
            self.map[x + 1][y + 1],
            self.map[x][y + 2],
            self.map[x + 1][y + 2],
            self.map[x - 1][y + 1],
            self.map[x + 2][y + 1],
            self.map[x][y + 3],
            self.map[x + 1][y + 3]
        )

    def get_blocks_below(self, x, y):
        """

        Returns 2 blocks below entity to check its on_ground parameter

        """
        return (
            self.map[x][y + 1],
            self.map[x + 1][y + 1]
        )

    def get_mobs(self):
        return self.mobs

    def spawn_tube(self, x_coord, y_coord):
        self.tubes.append(Tube(x_coord, y_coord))

        # Adding tube's collision just by spawning tiles inside the tube.
        # They will not render because we are adding them to "collision" list.
        for y in range(y_coord, 12): # 12 because it's ground level.
            for x in range(x_coord, x_coord + 2):
                self.map[x][y] = Platform(x * 32, y * 32, image=None, type_id=0)

    def spawn_mushroom(self, x, y):
        self.get_mobs().append(Mushroom(x, y, True))

    def spawn_goombas(self, x, y, move_direction):
        self.get_mobs().append(Goombas(x, y, move_direction))

    def spawn_koopa(self, x, y, move_direction):
        self.get_mobs().append(Koopa(x, y, move_direction))

    def spawn_flower(self, x, y):
        self.mobs.append(Flower(x, y))

    def spawn_debris(self, x, y, type):
        if type == 0:
            self.debris.append(PlatformDebris(x, y))
        elif type == 1:
            self.debris.append(CoinDebris(x, y))

    def spawn_fireball(self, x, y, move_direction):
        self.projectiles.append(Fireball(x, y, move_direction))

    def spawn_score_text(self, x, y, score=None):
        """

        This text appears when you, for example, kill a mob. It shows how many points
        you got.

        """

        # Score is none only when you kill a mob. If you got a killstreak,
        # amount of points for killing a mob will increase: 100, 200, 400, 800...
        # So you don't know how many points you should add.
        if score is None:
            self.text_objects.append(Text(str(self.score_for_killing_mob), 16, (x, y)))

            # Next score will be bigger
            self.score_time = pg.time.get_ticks()
            if self.score_for_killing_mob < 1600:
                self.score_for_killing_mob *= 2

        # That case for all other situations.
        else:
            self.text_objects.append(Text(str(score), 16, (x, y)))

    def remove_object(self, object):
        self.obj.remove(object)
        self.map[object.rect.x // 32][object.rect.y // 32] = 0

    def remove_whizbang(self, whizbang):
        self.projectiles.remove(whizbang)

    def remove_text(self, text_object):
        self.text_objects.remove(text_object)

    def update_player(self, core):
        self.get_player().update(core)

    def update_entities(self, core):
        for mob in self.mobs:
            mob.update(core)
            if not self.in_event:
                self.entity_collisions(core)

    def update_time(self, core):
        """

        Updating a map time.

        """

        # Time updates only if map not in event
        if not self.in_event:
            self.tick += 1
            if self.tick % 40 == 0:
                self.time -= 1
                self.tick = 0
            if self.time == 100 and self.tick == 1:
                core.get_sound().start_fast_music(core)
            elif self.time == 0:
                self.player_death(core)

    def update_score_time(self):
        """

        When player kill mobs in a row, score for each mob
        will increase. When player stops kill mobs, points
        will reset to 100. This function updates these points.

        """
        if self.score_for_killing_mob != 100:

            # Delay is 750 ms
            if pg.time.get_ticks() > self.score_time + 750:
                self.score_for_killing_mob //= 2

    def entity_collisions(self, core):
        """
        Xử lý va chạm giữa thực thể (mob) và người chơi.
        """
        if not core.get_map().get_player().unkillable:  # Kiểm tra xem người chơi có ở trạng thái bất tử không.
            for mob in self.mobs:  # Duyệt qua tất cả các mob.
                mob.check_collision_with_player(core)  # Kiểm tra va chạm với người chơi.

    def try_spawn_mobs(self, core):
        """
        Sinh ra mob tại các vị trí cụ thể khi người chơi đạt tọa độ x nhất định.
        """
        player_x = self.get_player().rect.x  # Lấy tọa độ x của người chơi.

        if player_x > 2080 and not self.is_mob_spawned[0]:
            self.spawn_goombas(2495, 224, False)  # Sinh mob ở vị trí đầu tiên.
            self.spawn_goombas(2560, 96, False)   # Sinh mob ở vị trí thứ hai.
            self.is_mob_spawned[0] = True  # Đánh dấu mob đã được sinh ra.

        elif player_x > 2460 and not self.is_mob_spawned[1]:
            spawn_positions = [
                (3200, 352), (3250, 352), (3700, 352), (3750, 352),
                (4060, 352), (4110, 352), (4190, 352), (4240, 352)
            ]
            for x, y in spawn_positions:
                self.spawn_goombas(x, y, False)  # Sinh mob tại từng vị trí trong danh sách.

            self.spawn_koopa(3400, 352, False)  # Sinh Koopa tại vị trí cụ thể.
            self.is_mob_spawned[1] = True  # Đánh dấu mob đã được sinh ra.

    def player_death(self, core):
        """
        Xử lý khi người chơi chết (mất mạng hoặc kết thúc trò chơi).
        """
        self.in_event = True  # Bật trạng thái sự kiện để dừng các hành động khác.
        player = self.get_player()
        player.reset_jump()  # Reset trạng thái nhảy.
        player.reset_move()  # Reset trạng thái di chuyển.
        player.numOfLives -= 1  # Giảm số mạng của người chơi.

        # Xử lý kết thúc trò chơi hoặc tiếp tục chơi.
        game_over = player.numOfLives == 0
        self.get_event().start_kill(core, game_over=game_over)

    def player_win(self, core):
        """
        Xử lý khi người chơi chiến thắng màn chơi.
        """
        self.in_event = True  # Bật trạng thái sự kiện để dừng các hành động khác.
        player = self.get_player()
        player.reset_jump()  # Reset trạng thái nhảy.
        player.reset_move()  # Reset trạng thái di chuyển.
        self.get_event().start_win(core)  # Bắt đầu sự kiện chiến thắng.

    def update(self, core):
        """
        Cập nhật trạng thái trò chơi ở mỗi khung hình (frame).
        """
        self.update_entities(core)  # Cập nhật trạng thái của các thực thể.

        if not core.get_map().in_event:  # Nếu không có sự kiện đặc biệt.
            player = self.get_player()

            if player.inLevelUpAnimation:  # Khi người chơi đang tăng cấp độ.
                player.change_powerlvl_animation()

            elif player.inLevelDownAnimation:  # Khi người chơi đang giảm cấp độ.
                player.change_powerlvl_animation()
                self.update_player(core)  # Cập nhật trạng thái người chơi.

            else:  # Trạng thái chơi thông thường.
                self.update_player(core)  # Cập nhật trạng thái người chơi.

        else:
            self.get_event().update(core)  # Xử lý các sự kiện đặc biệt.

        # Cập nhật các mảnh vụn (debris) xuất hiện khi phá gạch hoặc kích hoạt khối hỏi chấm.
        for debris in self.debris:
            debris.update(core)

        # Cập nhật các đạn lửa của người chơi.
        for whizbang in self.projectiles:
            whizbang.update(core)

        # Cập nhật các đối tượng văn bản (điểm số).
        for text_object in self.text_objects:
            text_object.update(core)

        # Cập nhật camera trừ khi có sự kiện dừng camera.
        if not self.in_event:
            self.get_camera().update(core.get_map().get_player().rect)

        self.try_spawn_mobs(core)  # Kiểm tra và sinh mob mới.

        self.update_time(core)  # Cập nhật thời gian chơi.
        self.update_score_time()  # Cập nhật điểm số dựa trên thời gian.

    def render_map(self, core):
        """
        Vẽ bản đồ chỉ bao gồm các ô gạch (tiles), thường dùng cho menu chính.
        """
        core.screen.blit(self.sky, (0, 0))  # Vẽ bầu trời nền.

        for obj_group in (self.obj_bg, self.obj):
            for obj in obj_group:
                obj.render(core)  # Vẽ từng đối tượng trong nhóm.

        for tube in self.tubes:  # Vẽ các ống (tube).
            tube.render(core)

    def render(self, core):
        """
        Vẽ tất cả các đối tượng trong trò chơi.
        """
        core.screen.blit(self.sky, (0, 0))  # Vẽ bầu trời nền.

        for obj in self.obj_bg:  # Vẽ các đối tượng nền.
            obj.render(core)

        for mob in self.mobs:  # Vẽ các mob.
            mob.render(core)

        for obj in self.obj:  # Vẽ các đối tượng trong bản đồ.
            obj.render(core)

        for tube in self.tubes:  # Vẽ các ống.
            tube.render(core)

        for whizbang in self.projectiles:  # Vẽ các đạn lửa.
            whizbang.render(core)

        for debris in self.debris:  # Vẽ các mảnh vụn.
            debris.render(core)

        self.flag.render(core)  # Vẽ cờ khi người chơi hoàn thành màn chơi.

        for text_object in self.text_objects:  # Vẽ các điểm số hoặc chữ trên màn hình.
            text_object.render_in_game(core)

        self.get_player().render(core)  # Vẽ người chơi.
        self.get_ui().render(core)  # Vẽ giao diện người chơi (UI).

