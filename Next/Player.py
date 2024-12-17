import pygame as pg

from Const import *


class Player(object):
    def __init__(self, x_pos, y_pos):
        # Khởi tạo các thuộc tính của nhân vật người chơi
        self.numOfLives = 1  # Số mạng ban đầu của người chơi
        self.score = 0  # Điểm số ban đầu
        self.coins = 0  # Số lượng xu ban đầu

        self.visible = True  # Nhân vật có thể hiển thị trên màn hình
        self.spriteTick = 0  # Biến theo dõi việc thay đổi hình ảnh
        self.powerLVL = 0  # Cấp độ sức mạnh (0 là cấp độ nhỏ)

        self.unkillable = False  # Kiểm tra trạng thái bất tử
        self.unkillableTime = 0  # Thời gian bất tử

        self.inLevelUpAnimation = False  # Kiểm tra trạng thái đang tăng cấp
        self.inLevelUpAnimationTime = 0  # Thời gian tăng cấp
        self.inLevelDownAnimation = False  # Kiểm tra trạng thái đang giảm cấp
        self.inLevelDownAnimationTime = 0  # Thời gian giảm cấp

        self.already_jumped = False  # Kiểm tra xem nhân vật đã nhảy chưa
        self.next_jump_time = 0  # Thời gian nhảy tiếp theo
        self.next_fireball_time = 0  # Thời gian bắn lửa tiếp theo
        self.x_vel = 0  # Vận tốc theo hướng X (trái-phải)
        self.y_vel = 0  # Vận tốc theo hướng Y (lên-xuống)
        self.direction = True  # Hướng di chuyển của nhân vật (True là phải, False là trái)
        self.on_ground = False  # Kiểm tra xem nhân vật có đang ở trên mặt đất không
        self.fast_moving = False  # Kiểm tra xem nhân vật có đang di chuyển nhanh không
        
        self.pos_x = x_pos  # Vị trí X của nhân vật

        # Tải hình ảnh của nhân vật và các sprite
        self.image = pg.image.load('images/mario/mario.png').convert_alpha()
        self.sprites = []
        self.load_sprites()

        self.rect = pg.Rect(x_pos, y_pos, 32, 32)  # Khung bao quanh nhân vật

    def load_sprites(self):
        # Tải tất cả các sprite hình ảnh cho nhân vật
        self.sprites = [
            # 0 Small, stay
            pg.image.load('images/Mario/mario.png'),

            # 1 Small, move 0
            pg.image.load('images/Mario/mario_move0.png'),

            # 2 Small, move 1
            pg.image.load('images/Mario/mario_move1.png'),

            # 3 Small, move 2
            pg.image.load('images/Mario/mario_move2.png'),

            # 4 Small, jump
            pg.image.load('images/Mario/mario_jump.png'),

            # 5 Small, end 0
            pg.image.load('images/Mario/mario_end.png'),

            # 6 Small, end 1
            pg.image.load('images/Mario/mario_end1.png'),

            # 7 Small, stop
            pg.image.load('images/Mario/mario_st.png'),

            # =============================================

            # 8 Big, stay
            pg.image.load('images/Mario/mario1.png'),

            # 9 Big, move 0
            pg.image.load('images/Mario/mario1_move0.png'),

            # 10 Big, move 1
            pg.image.load('images/Mario/mario1_move1.png'),

            # 11 Big, move 2
            pg.image.load('images/Mario/mario1_move2.png'),

            # 12 Big, jump
            pg.image.load('images/Mario/mario1_jump.png'),

            # 13 Big, end 0
            pg.image.load('images/Mario/mario1_end.png'),

            # 14 Big, end 1
            pg.image.load('images/Mario/mario1_end1.png'),

            # 15 Big, stop
            pg.image.load('images/Mario/mario1_st.png'),

            # =============================================

            # 16 Big_fireball, stay
            pg.image.load('images/Mario/mario2.png'),

            # 17 Big_fireball, move 0
            pg.image.load('images/Mario/mario2_move0.png'),

            # 18 Big_fireball, move 1
            pg.image.load('images/Mario/mario2_move1.png'),

            # 19 Big_fireball, move 2
            pg.image.load('images/Mario/mario2_move2.png'),

            # 20 Big_fireball, jump
            pg.image.load('images/Mario/mario2_jump.png'),

            # 21 Big_fireball, end 0
            pg.image.load('images/Mario/mario2_end.png'),

            # 22 Big_fireball, end 1
            pg.image.load('images/Mario/mario2_end1.png'),

            # 23 Big_fireball, stop
            pg.image.load('images/Mario/mario2_st.png'),
        ]

        # Tạo các sprite đối diện với hướng trái
        for i in range(len(self.sprites)):
            self.sprites.append(pg.transform.flip(self.sprites[i], 180, 0))

        # Sprite thay đổi cấp độ sức mạnh, hướng phải
        self.sprites.append(pg.image.load('images/Mario/mario_lvlup.png').convert_alpha())

        # Sprite thay đổi cấp độ sức mạnh, hướng trái
        self.sprites.append(pg.transform.flip(self.sprites[-1], 180, 0))

        # Sprite khi nhân vật chết
        self.sprites.append(pg.image.load('images/Mario/mario_death.png').convert_alpha())

    def update(self, core):
        # Cập nhật trạng thái của nhân vật
        self.player_physics(core)
        self.update_image(core)
        self.update_unkillable_time()

    def player_physics(self, core):
        # Xử lý vật lý di chuyển của nhân vật
        if core.keyR:
            self.x_vel += SPEED_INCREASE_RATE  # Di chuyển sang phải
            self.direction = True
        if core.keyL:
            self.x_vel -= SPEED_INCREASE_RATE  # Di chuyển sang trái
            self.direction = False
        if not core.keyU:
            self.already_jumped = False  # Đặt lại trạng thái nhảy nếu không nhấn phím nhảy
        elif core.keyU:
            if self.on_ground and not self.already_jumped:
                self.y_vel = -JUMP_POWER  # Nhảy lên
                self.already_jumped = True  # Đánh dấu là đã nhảy
                self.next_jump_time = pg.time.get_ticks() + 750  # Đặt thời gian nhảy tiếp theo
                if self.powerLVL >= 1:
                    core.get_sound().play('big_mario_jump', 0, 0.5)  # Âm thanh nhảy nếu cấp độ lớn
                else:
                    core.get_sound().play('small_mario_jump', 0, 0.5)  # Âm thanh nhảy nếu cấp độ nhỏ


        # Fireball shoot and fast moving
        # Fireball shoot and fast moving
# Kiểm tra phím Shift để nhân vật có thể chạy nhanh hơn.
# Nếu nhân vật ở cấp sức mạnh 2 (powerLVL = 2), sẽ có khả năng bắn quả cầu lửa.

        self.fast_moving = False
        if core.keyShift:
            self.fast_moving = True
            if self.powerLVL == 2:
                if pg.time.get_ticks() > self.next_fireball_time: # Kiểm tra thời gian để bắn quả cầu lửa
                    if not (self.inLevelUpAnimation or self.inLevelDownAnimation):# Không trong animation nâng cấp hoặc giảm cấp
                        if len(core.get_map().projectiles) < 2: # Kiểm tra số lượng quả cầu lửa
                            self.shoot_fireball(core, self.rect.x, self.rect.y, self.direction) # Bắn quả cầu lửa
# Điều chỉnh tốc độ di chuyển nếu không có phím di chuyển được nhấn.
        if not (core.keyR or core.keyL):
            if self.x_vel > 0:
                self.x_vel -= SPEED_DECREASE_RATE # Giảm tốc độ di chuyển nếu không có phím trái/phải
            elif self.x_vel < 0:
                self.x_vel += SPEED_DECREASE_RATE# Tăng tốc độ di chuyển nếu đi ngược lại
        else:
            if self.x_vel > 0:
                if self.fast_moving:
                    if self.x_vel > MAX_FASTMOVE_SPEED: # Tăng tốc độ di chuyển nếu đi ngược lại
                        self.x_vel = MAX_FASTMOVE_SPEED
                else:
                    if self.x_vel > MAX_MOVE_SPEED: # Giới hạn tốc độ di chuyển bình thường
                        self.x_vel = MAX_MOVE_SPEED
            if self.x_vel < 0:
                if self.fast_moving:
                    if (-self.x_vel) > MAX_FASTMOVE_SPEED: self.x_vel = -MAX_FASTMOVE_SPEED # Giới hạn tốc độ chạy nhanh ngược
                else:
                    if (-self.x_vel) > MAX_MOVE_SPEED:
                        self.x_vel = -MAX_MOVE_SPEED

        # Loại bỏ sai số tính toán cho tốc độ di chuyển
        if 0 < self.x_vel < SPEED_DECREASE_RATE:
            self.x_vel = 0
        if 0 > self.x_vel > -SPEED_DECREASE_RATE:
            self.x_vel = 0
# Kiểm tra trạng thái trên mặt đất và xử lý chuyển động chiều dọc
        if not self.on_ground:
            # Di chuyển lên, nút nhảy được nhấn
            if (self.y_vel < 0 and core.keyU):
                self.y_vel += GRAVITY
                
             #Di chuyển lên, nút nhảy không được nhấn - nhảy thấp
            elif (self.y_vel < 0 and not core.keyU):
                self.y_vel += GRAVITY * LOW_JUMP_MULTIPLIER # Giảm lực hấp dẫn khi nhảy thấp
            
            # Moving down
            else:
                self.y_vel += GRAVITY * FALL_MULTIPLIER# Tăng tốc độ rơi
            
            if self.y_vel > MAX_FALL_SPEED:# Giới hạn tốc độ rơi
                self.y_vel = MAX_FALL_SPEED
# Lấy các khối trên bản đồ để kiểm tra va chạm
        blocks = core.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
        # Cập nhật vị trí theo chiều ngang
        self.pos_x += self.x_vel
        self.rect.x = self.pos_x
        
        self.update_x_pos(blocks)
# Cập nhật vị trí theo chiều dọc
        self.rect.y += self.y_vel
        self.update_y_pos(blocks, core)

       # Kiểm tra va chạm với mặt đất
        coord_y = self.rect.y // 32
        if self.powerLVL > 0:
            coord_y += 1
        for block in core.get_map().get_blocks_below(self.rect.x // 32, coord_y):
            if block != 0 and block.type != 'BGObject': # Kiểm tra khối không phải là đối tượng nền
                if pg.Rect(self.rect.x, self.rect.y + 1, self.rect.w, self.rect.h).colliderect(block.rect):
                    self.on_ground = True  # Kiểm tra khối không phải là đối tượng nền

        # Map border check# Kiểm tra va chạm với biên bản đồ (một số loại khối như tường, bề mặt...)
        if self.rect.y > 448:# Nếu nhân vật vượt quá giới hạn màn hình, gọi hàm chết
            core.get_map().player_death(core)

        # Kiểm tra va chạm với cột cờ (kết thúc màn chơi)
        if self.rect.colliderect(core.get_map().flag.pillar_rect):
            core.get_map().player_win(core)# Người chơi đã chiến thắng
# Set image cho nhân vật tùy theo tình trạng hiện tại (dead, đi lại, nhảy...)
    def set_image(self, image_id):
# "Dead" sprite (hình ảnh khi chết)
        # "Dead" sprite
        if image_id == len(self.sprites):
            self.image = self.sprites[-1]

        elif self.direction:
            self.image = self.sprites[image_id + self.powerLVL * 8]  # Chọn hình ảnh phù hợp với hướng và cấp sức mạnh
        else:
            self.image = self.sprites[image_id + self.powerLVL * 8 + 24] # Hình ảnh khi quay ngược
# Cập nhật hình ảnh của nhân vật (dựa trên trạng thái và chuyển động)
    def update_image(self, core):

        self.spriteTick += 1
        if (core.keyShift):# Nếu nhấn Shift, tăng thêm tốc độ cập nhật hình ảnh
            self.spriteTick += 1

        if self.powerLVL in (0, 1, 2):

            if self.x_vel == 0: # Nếu không di chuyển, đặt hình ảnh đứng yên
                self.set_image(0)
                self.spriteTick = 0

             # Nếu nhân vật đang chạy
            elif (
                    ((self.x_vel > 0 and core.keyR and not core.keyL) or
                     (self.x_vel < 0 and core.keyL and not core.keyR)) or
                    (self.x_vel > 0 and not (core.keyL or core.keyR)) or
                    (self.x_vel < 0 and not (core.keyL or core.keyR))
            ):
                             
                if (self.spriteTick > 30):# Lặp lại hình ảnh khi chạy
                    self.spriteTick = 0
                   
                if self.spriteTick <= 10:
                    self.set_image(1)
                elif 11 <= self.spriteTick <= 20:
                    self.set_image(2)
                elif 21 <= self.spriteTick <= 30:
                    self.set_image(3)
                elif self.spriteTick == 31:
                    self.spriteTick = 0
                    self.set_image(1)

           # Khi nhân vật thay đổi hướng mà chưa dừng lại
            elif (self.x_vel > 0 and core.keyL and not core.keyR) or (self.x_vel < 0 and core.keyR and not core.keyL):
                self.set_image(7)
                self.spriteTick = 0

            if not self.on_ground:
                self.spriteTick = 0
                self.set_image(4)
# Cập nhật thời gian không thể bị giết
    def update_unkillable_time(self):
        if self.unkillable:
            self.unkillableTime -= 1
            if self.unkillableTime == 0:
                self.unkillable = False
# Cập nhật vị trí theo chiều ngang (x)
    def update_x_pos(self, blocks):
        for block in blocks:
            if block != 0 and block.type != 'BGObject':# Kiểm tra các khối hợp lệ
                block.debugLight = True
                if pg.Rect.colliderect(self.rect, block.rect):# Kiểm tra va chạm với khối
                 if self.x_vel > 0:
                    if self.x_vel > 0:
                        self.rect.right = block.rect.left # Va chạm từ phải
                        self.pos_x = self.rect.left
                        self.x_vel = 0
                    elif self.x_vel < 0:
                        self.rect.left = block.rect.right # Va chạm từ trái
                        self.pos_x = self.rect.left
                        self.x_vel = 0  # Dừng di chuyển
# Cập nhật vị trí theo chiều dọc (y)
    def update_y_pos(self, blocks, core):
        self.on_ground = False
        for block in blocks:
            if block != 0 and block.type != 'BGObject':
                if pg.Rect.colliderect(self.rect, block.rect): # Kiểm tra va chạm với khối

                    if self.y_vel > 0:
                        self.on_ground = True  # Nhân vật đã chạm đất
                        self.rect.bottom = block.rect.top
                        self.y_vel = 0

                    elif self.y_vel < 0:
                        self.rect.top = block.rect.bottom  # Va chạm từ trên xuống
                        self.y_vel = -self.y_vel / 3 # Giảm tốc độ khi va chạm
                        self.activate_block_action(core, block)

    def activate_block_action(self, core, block):
        # Question Block
        if block.typeID == 22:
            core.get_sound().play('block_hit', 0, 0.5) # Phát âm thanh khi đánh vào khối
            if not block.isActivated: # Nếu block chưa được kích hoạt
                block.spawn_bonus(core) # Tạo ra vật phẩm thưởng


        # Brick Platform (Nền gạch)
        elif block.typeID == 23: 
            if self.powerLVL == 0:# Nếu người chơi không có powerlevel
                block.shaking = True # Khối sẽ rung lên
                core.get_sound().play('block_hit', 0, 0.5) # Phát âm thanh khi đánh vào khối
            else:
                block.destroy(core)
                core.get_sound().play('brick_break', 0, 0.5) # Phát âm thanh khi brick bị phá hủy
                self.add_score(50)# Thêm 50 điểm vào tổng điểm của người chơi


    def reset(self, reset_all):
        self.direction = True # Đặt hướng di chuyển của người chơi là True (có thể là phải)
        self.rect.x = 96# Đặt vị trí người chơi trên trục x
        self.pos_x = 96 # Đặt vị trí người chơi trên trục x
        self.rect.y = 351# Đặt vị trí người chơi trên trục y
        if self.powerLVL != 0: # Nếu powerLevel không phải 0
            self.powerLVL = 0# Đặt lại powerLevel về 0
            self.rect.y += 32# Điều chỉnh lại chiều cao của nhân vật
            self.rect.h = 32 # Điều chỉnh chiều cao của nhân vật


        if reset_all:
             # Nếu reset_all là True, tất cả các giá trị sẽ được reset về mặc định
            self.score = 0# Đặt điểm số về 0
            self.coins = 0# Đặt số coins về 0
            self.numOfLives = 1# Đặt số mạng về 1

            self.visible = True# Đặt trạng thái hiển thị về True
            self.spriteTick = 0# Đặt lại tick của sprite

            self.powerLVL = 0 # Đặt lại powerLevel về 0
            self.inLevelUpAnimation = False # Không có hoạt ảnh nâng cấp cấp độ
            self.inLevelUpAnimationTime = 0   # Thời gian của hoạt ảnh nâng cấp

            self.unkillable = False # Đặt trạng thái không thể bị giết về False
            self.unkillableTime = 0# Thời gian không thể bị giết

            self.inLevelDownAnimation = False# Không có hoạt ảnh giảm cấp độ
            self.inLevelDownAnimationTime = 0 # Thời gian của hoạt ảnh giảm cấp độ

            self.already_jumped = False# Đánh dấu người chơi chưa nhảy
            self.x_vel = 0  # Đặt vận tốc ngang về 0

            self.y_vel = 0 # Đặt vận tốc dọc về 0
            self.on_ground = False# Đặt trạng thái đang đứng trên mặt đất về False

    def reset_jump(self):
        self.y_vel = 0 # Đặt vận tốc dọc về 0 khi reset nhảy
        self.already_jumped = False  # Đánh dấu người chơi chưa nhảy

    def reset_move(self):
        self.x_vel = 0 # Đặt vận tốc ngang về 0 khi reset di chuyển
        self.y_vel = 0 # Đặt vận tốc ngang về 0 khi reset di chuyển

    def jump_on_mob(self):
        self.already_jumped = True # Đánh dấu người chơi đã nhảy
        self.y_vel = -4  # Thiết lập vận tốc nhảy dọc
        self.rect.y -= 6 # Di chuyển vị trí người chơi lên một chút sau khi nhảy

    def set_powerlvl(self, power_lvl, core):
        # Nếu powerLevel hiện tại là 0 và powerLevel mới bằng 0 và người chơi không bất tử
        if self.powerLVL == 0 == power_lvl and not self.unkillable:
            core.get_map().player_death(core)  # Xử lý khi người chơi chết
            self.inLevelUpAnimation = False  # Tắt hoạt ảnh nâng cấp cấp độ
            self.inLevelDownAnimation = False # Tắt hoạt ảnh hạ cấp độ

  # Nếu powerLevel hiện tại là 0 và powerLevel mới lớn hơn 0
        elif self.powerLVL == 0 and self.powerLVL < power_lvl:
            self.powerLVL = 1 # Đặt powerLevel của người chơi là 1
            core.get_sound().play('mushroom_eat', 0, 0.5) # Phát âm thanh khi ăn nấm
            core.get_map().spawn_score_text(self.rect.x + 16, self.rect.y, score=1000)
            self.add_score(1000) # Thêm điểm cho người chơi
            self.inLevelUpAnimation = True # Bật hoạt ảnh nâng cấp cấp độ
            self.inLevelUpAnimationTime = 61 # Đặt thời gian hoạt ảnh
# Nếu powerLevel hiện tại là 1 và powerLevel mới lớn hơn 1

        elif self.powerLVL == 1 and self.powerLVL < power_lvl:
            core.get_sound().play('mushroom_eat', 0, 0.5) # Phát âm thanh khi ăn nấm
            core.get_map().spawn_score_text(self.rect.x + 16, self.rect.y, score=1000) # Hiển thị điểm
            self.add_score(1000)  # Thêm điểm cho người chơi
            self.powerLVL = 2 # Đặt powerLevel của người chơi lên 2
# Nếu powerLevel hiện tại lớn hơn powerLevel mới
        elif self.powerLVL > power_lvl: 
            core.get_sound().play('pipe', 0, 0.5) # Phát âm thanh khi người chơi bị giảm cấp
            self.inLevelDownAnimation = True # Bật hoạt ảnh giảm cấp
            self.inLevelDownAnimationTime = 200 # Đặt thời gian hoạt ảnh giảm cấp

            self.unkillable = True   # Đặt trạng thái bất tử
            self.unkillableTime = 200 # Đặt thời gian bất tử

        else:
            core.get_sound().play('mushroom_eat', 0, 0.5) # Phát âm thanh khi ăn nấm
            core.get_map().spawn_score_text(self.rect.x + 16, self.rect.y, score=1000) # Hiển thị điểm
            self.add_score(1000) # Thêm điểm cho người chơi


    def change_powerlvl_animation(self):
# Xử lý hoạt ảnh khi giảm cấp độ
        if self.inLevelDownAnimation:
            self.inLevelDownAnimationTime -= 1 # Giảm thời gian hoạt ảnh

            if self.inLevelDownAnimationTime == 0:
                self.inLevelDownAnimation = False  # Kết thúc hoạt ảnh giảm cấp
                self.visible = True  # Đảm bảo nhân vật hiển thị
            elif self.inLevelDownAnimationTime % 20 == 0: # Thay đổi hiển thị sau mỗi 20 lần lặp
                if self.visible: # Đổi trạng thái hiển thị
                    self.visible = False
                else:
                    self.visible = True
                if self.inLevelDownAnimationTime == 100:
                    self.powerLVL = 0 # Đặt lại powerLevel về 0
                    self.rect.y += 32 # Điều chỉnh lại vị trí của nhân vật
                    self.rect.h = 32  # Điều chỉnh chiều cao của nhân vật
 # Xử lý hoạt ảnh khi nâng cấp cấp độ
        elif self.inLevelUpAnimation:
            self.inLevelUpAnimationTime -= 1 # Giảm thời gian hoạt ảnh nâng cấp


            if self.inLevelUpAnimationTime == 0:
                self.inLevelUpAnimation = False # Kết thúc hoạt ảnh nâng cấp
                self.rect.y -= 32  # Đặt lại vị trí
                self.rect.h = 64 # Đặt lại chiều cao
# Các điểm thời gian khác trong quá trình nâng cấp
            elif self.inLevelUpAnimationTime in (60, 30):
                self.image = self.sprites[-3] if self.direction else self.sprites[-2] # Đổi hình ảnh
                self.rect.y -= 16  # Điều chỉnh vị trí
                self.rect.h = 48 # Điều chỉnh chiều cao
            elif self.inLevelUpAnimationTime in (45, 15):
                self.image = self.sprites[0] if self.direction else self.sprites[24] # Đổi hình ảnh
                self.rect.y += 16 # Điều chỉnh vị trí
                self.rect.h = 32# Điều chỉnh chiều cao

    def flag_animation_move(self, core, walk_to_castle):
        if walk_to_castle: # Nếu người chơi đang đi về lâu đài
            self.direction = True  # Di chuyển theo hướng phải


            if not self.on_ground: # Nếu không đứng trên mặt đất
                self.y_vel += GRAVITY if self.y_vel <= MAX_FALL_SPEED else 0 # Tăng tốc độ rơi

# Lấy vị trí của nhân vật trên bản đồ
            x = self.rect.x // 32
            y = self.rect.y // 32
            blocks = core.get_map().get_blocks_for_collision(x, y)

            self.rect.x += self.x_vel   # Cập nhật vị trí ngang
            if self.rect.colliderect(core.get_map().map[205][11]):
                self.visible = False # Ẩn nhân vật khi đến lâu đài
                core.get_map().get_event().player_in_castle = True # Ẩn nhân vật khi đến lâu đài
            self.update_x_pos(blocks)

            self.rect.top += self.y_vel # Cập nhật vị trí dọc
            self.update_y_pos(blocks, core)

            # Kiểm tra xem nhân vật có đứng trên mặt đất không
            x = self.rect.x // 32
            y = self.rect.y // 32
            if self.powerLVL > 0:
                y += 1
            for block in core.get_map().get_blocks_below(x, y):
                if block != 0 and block.type != 'BGObject': # Nếu không phải đối tượng nền
                    if pg.Rect(self.rect.x, self.rect.y + 1, self.rect.w, self.rect.h).colliderect(block.rect):
                        self.on_ground = True # Đánh dấu người chơi đứng trên mặt đất

        else:
            # Nếu không đi về lâu đài, điều chỉnh vị trí theo flag
            if core.get_map().flag.flag_rect.y + 20 > self.rect.y + self.rect.h:
                self.rect.y += 3

    def shoot_fireball(self, core, x, y, move_direction):
        # Xử lý việc bắn quả cầu lửa
        core.get_map().spawn_fireball(x, y, move_direction) # Tạo quả cầu lửa trên bản đồ
        core.get_sound().play('fireball', 0, 0.5) # Phát âm thanh khi bắn quả cầu lửa
        self.next_fireball_time = pg.time.get_ticks() + 400  # Đặt thời gian giữa các lần bắn

    def add_coins(self, count):
        self.coins += count  # Thêm coins vào tổng số coins của người chơi


    def add_score(self, count):
        self.score += count # Thêm điểm vào tổng điểm của người chơi

    def render(self, core):
        if self.visible:  # Nếu nhân vật đang hiển thị
            core.screen.blit(self.image, core.get_map().get_camera().apply(self))  # Vẽ hình ảnh của nhân vật lên màn hình
