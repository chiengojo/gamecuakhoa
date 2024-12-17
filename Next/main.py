import os
import pygame  # Hoặc các thư viện khác bạn đang dùng

# Chuyển thư mục làm việc sang nơi chứa file 'Next'
os.chdir(r"C:/Users/LENOVO/Desktop/gamecuakhoafinal/Next")

from Core import Core

if __name__ == "__main__":
    oCore = Core()
    oCore.main_loop()