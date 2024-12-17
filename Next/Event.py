import pygame as pg
import cv2
from Const import *

video_path = "C:/Users/lak17/OneDrive/Videos/Lê ANh KHoa -31241027375.mp4"


# Open the video file


class Event(object):
    def __init__(self):
        # Khởi tạo sự kiện.

        # Loại sự kiện:
        # 0 = Người chơi chết / Game Over
        # 1 = Người chơi chiến thắng (chạm vào lá cờ)
        self.type = 0

        # Thời gian trì hoãn trước khi xử lý sự kiện
        self.delay = 0
        # Dấu thời gian khi sự kiện bắt đầu
        self.time = 0
        # Vận tốc di chuyển trên trục x và y
        self.x_vel = 0
        self.y_vel = 0
        # Cờ xác định nếu trò chơi kết thúc
        self.game_over = False

        # Cờ xác định nếu người chơi đã vào lâu đài
        self.player_in_castle = False
        # Bộ đếm cho hoạt ảnh hoặc logic đặc biệt
        self.tick = 0
        # Bộ đếm để xử lý điểm số
        self.score_tick = 0

    def reset(self):
        # Đặt lại tất cả các giá trị về trạng thái mặc định
        self.type = 0
        self.delay = 0
        self.time = 0
        self.x_vel = 0
        self.y_vel = 0
        self.game_over = False
        self.player_in_castle = False
        self.tick = 0
        self.score_tick = 0

    def start_kill(self, core, game_over):
        """
        Khởi tạo sự kiện người chơi chết.
        """
        self.type = 0  # Loại sự kiện là "chết".
        self.delay = 4000  # Thời gian trì hoãn là 4 giây.
        self.y_vel = -4  # Vận tốc rơi ban đầu hướng lên.
        self.time = pg.time.get_ticks()  # Lấy thời gian hiện tại.
        self.game_over = game_over  # Xác định nếu đây là game over.

        # Dừng các bản nhạc nền và phát nhạc "death".
        core.get_sound().stop('overworld')
        core.get_sound().stop('overworld_fast')
        core.get_sound().play('death', 0, 0.5)

        # Đặt hình ảnh "chết" cho người chơi.
        core.get_map().get_player().set_image(len(core.get_map().get_player().sprites))

    def start_win(self, core):
        """
        Khởi tạo sự kiện chiến thắng khi chạm vào lá cờ.
        """
        self.type = 1  # Loại sự kiện là "chiến thắng".
        self.delay = 2000  # Thời gian trì hoãn là 2 giây.
        self.time = 0  # Đặt thời gian khởi đầu.

        # Dừng các bản nhạc nền và phát nhạc "level_end".
        core.get_sound().stop('overworld')
        core.get_sound().stop('overworld_fast')
        core.get_sound().play('level_end', 0, 0.5)

        # Đặt hình ảnh và di chuyển nhẹ người chơi để hiển thị hoạt ảnh chiến thắng.
        core.get_map().get_player().set_image(5)
        core.get_map().get_player().x_vel = 1
        core.get_map().get_player().rect.x += 10

        # Tính điểm thưởng dựa trên thời gian còn lại trong màn chơi.
        if core.get_map().time >= 300:  # Nếu thời gian >= 300
            core.get_map().get_player().add_score(5000)
            core.get_map().spawn_score_text(core.get_map().get_player().rect.x + 16, core.get_map().get_player().rect.y, score=5000)
        elif 200 <= core.get_map().time < 300:  # Nếu thời gian từ 200 đến 299
            core.get_map().get_player().add_score(2000)
            core.get_map().spawn_score_text(core.get_map().get_player().rect.x + 16, core.get_map().get_player().rect.y, score=2000)
        else:  # Nếu thời gian < 200
            core.get_map().get_player().add_score(1000)
            core.get_map().spawn_score_text(core.get_map().get_player().rect.x + 16, core.get_map().get_player().rect.y, score=1000)

    def update(self, core):
        """
        Cập nhật trạng thái sự kiện trong từng khung hình (frame).
        """
        self.video_played = False
        # Xử lý sự kiện chết (type = 0)
        if self.type == 0:
            core.get_mm().currentGameState = 'Loading'
            core.get_mm().oLoadingMenu.set_text_and_type('GAME OVER', False)
            core.get_mm().oLoadingMenu.update_time()
            core.get_sound().play('game_over', 0, 0.5)
            # Tăng vận tốc rơi nếu chưa đạt mức tối đa.
            # self.y_vel += GRAVITY * FALL_MULTIPLIER if self.y_vel < 6 else 0
            # core.get_map().get_player().rect.y += self.y_vel  # Cập nhật vị trí y của người chơi.

            # Nếu đã qua thời gian trì hoãn:
            # if pg.time.get_ticks() > self.time + self.delay:
            #     if not self.game_over:  # Nếu không phải game over:
            #         core.get_map().get_player().reset_move()  # Đặt lại di chuyển.
            #         core.get_map().get_player().reset_jump()  # Đặt lại nhảy.
            #         core.get_map().reset(False)  # Đặt lại màn chơi.
            #         core.get_sound().play('overworld', 9999999, 0.5)  # Phát lại nhạc nền.
            #     else:  # Nếu game over:
            #         core.get_mm().currentGameState = 'Loading'
            #         core.get_mm().oLoadingMenu.set_text_and_type('GAME OVER', False)
            #         core.get_mm().oLoadingMenu.update_time()
            #         core.get_sound().play('game_over', 0, 0.5)

        # Xử lý sự kiện chiến thắng (type = 1)
        elif self.type == 1:
            if not self.player_in_castle:  # Nếu chưa vào lâu đài
                if not core.get_map().flag.flag_omitted:  # Nếu cờ chưa hạ
                    core.get_map().get_player().set_image(5)
                    core.get_map().flag.move_flag_down()  # Hạ cờ.
                    core.get_map().get_player().flag_animation_move(core, False)
                else:  # Nếu cờ đã hạ xong:
                    self.tick += 1
                    if self.tick == 1:
                        core.get_map().get_player().direction = False  # Đặt hướng di chuyển.
                        core.get_map().get_player().set_image(6)
                        core.get_map().get_player().rect.x += 20
                    elif self.tick >= 30:
                        core.get_map().get_player().flag_animation_move(core, True)
                        core.get_map().get_player().update_image(core)
            else:  # Nếu đã vào lâu đài:
                if core.get_map().time > 0:  # Nếu còn thời gian:
                    self.score_tick += 1
                    if self.score_tick % 10 == 0:  # Cứ mỗi 10 tick, thêm điểm và phát âm thanh.
                        core.get_sound().play('scorering', 0, 0.5)
                    core.get_map().time -= 1
                    core.get_map().get_player().add_score(50)
                else:  # Khi hết thời gian:
                    if self.time == 0:  # Nếu chưa đặt thời gian ban đầu.
                        self.time = pg.time.get_ticks()
                    elif pg.time.get_ticks() >= self.time + self.delay:
                        core.get_mm().currentGameState = 'Loading'
                        core.get_mm().oLoadingMenu.set_text_and_type('BY S&D :)', False)
                        core.get_mm().oLoadingMenu.update_time()
                        core.get_sound().play('game_over', 0, 0.5)
            
            
            cap = cv2.VideoCapture(video_path)

            # Check if the video file opened successfully
            if not cap.isOpened():
                print("Error: Could not open video.")
                exit()
            if core.get_map().get_player().coins >= 17 and core.get_map().get_player().score >= 20000 and not self.video_played:
                self.video_played = True
            # Read and display the video frame by frame
                while True:
                    self.video_played = True
                    ret, frame = cap.read()
                    
                    # Break the loop if no frame is read (end of video)
                    if not ret:
                        core.get_mm().currentGameState = 'Loading'
                        core.get_mm().oLoadingMenu.set_text_and_type('BY S&D :)', False)
                        core.get_mm().oLoadingMenu.update_time()
                        core.get_sound().play('game_over', 0, 0.5)
                        break

                    # Display the frame
                    cv2.imshow('Video', frame)

                    # Press 'q' to exit the video playback
                    if cv2.waitKey(25) & 0xFF == 13:
                        core.get_mm().currentGameState = 'Loading'
                        core.get_mm().oLoadingMenu.set_text_and_type('BY S&D :)', False)
                        core.get_mm().oLoadingMenu.update_time()
                        core.get_sound().play('game_over', 0, 0.5)
                        break

                # Release the video capture object and close display windows
                cap.release()
                cv2.destroyAllWindows()
            else:
                core.get_mm().currentGameState = 'Loading'
                core.get_mm().oLoadingMenu.set_text_and_type('BY S&D :)', False)
                core.get_mm().oLoadingMenu.update_time()
                core.get_sound().play('game_over', 0, 0.5)