import pygame as pg


class Sound(object):
    def __init__(self):
        # Khởi tạo một từ điển để lưu trữ các đối tượng âm thanh
        self.sounds = {}
        # Gọi phương thức để tải các âm thanh vào từ điển
        self.load_sounds()

    def load_sounds(self):
        # Tải các tệp âm thanh từ các file tương ứng và lưu vào từ điển sounds
        self.sounds['overworld'] = pg.mixer.Sound('sounds/overworld.wav')
        self.sounds['overworld_fast'] = pg.mixer.Sound('sounds/overworld-fast.wav')
        self.sounds['level_end'] = pg.mixer.Sound('sounds/levelend.wav')
        self.sounds['coin'] = pg.mixer.Sound('sounds/coin.wav')
        self.sounds['small_mario_jump'] = pg.mixer.Sound('sounds/jump.wav')
        self.sounds['big_mario_jump'] = pg.mixer.Sound('sounds/jumpbig.wav')
        self.sounds['brick_break'] = pg.mixer.Sound('sounds/blockbreak.wav')
        self.sounds['block_hit'] = pg.mixer.Sound('sounds/blockhit.wav')
        self.sounds['mushroom_appear'] = pg.mixer.Sound('sounds/mushroomappear.wav')
        self.sounds['mushroom_eat'] = pg.mixer.Sound('sounds/mushroomeat.wav')
        self.sounds['death'] = pg.mixer.Sound('sounds/death.wav')
        self.sounds['pipe'] = pg.mixer.Sound('sounds/pipe.wav')
        self.sounds['kill_mob'] = pg.mixer.Sound('sounds/kill_mob.wav')
        self.sounds['game_over'] = pg.mixer.Sound('sounds/gameover.wav')
        self.sounds['scorering'] = pg.mixer.Sound('sounds/scorering.wav')
        self.sounds['fireball'] = pg.mixer.Sound('sounds/fireball.wav')
        self.sounds['shot'] = pg.mixer.Sound('sounds/shot.wav')

    def play(self, name, loops, volume):
        # Phát âm thanh đã tải vào dựa trên tên, với số lần lặp lại và âm lượng
        self.sounds[name].play(loops=loops)
        self.sounds[name].set_volume(volume)

    def stop(self, name):
        # Dừng phát âm thanh đã chọn
        self.sounds[name].stop()

    def start_fast_music(self, core):
        # Nếu màn chơi là '1-1', dừng nhạc chính và phát nhạc nhanh
        if core.get_map().get_name() == '1-1':
            self.stop('overworld')  # Dừng nhạc hiện tại
            self.play('overworld_fast', 99999, 0.5)  # Phát nhạc nhanh với lặp lại không giới hạn
