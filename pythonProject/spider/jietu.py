import cv2
import numpy as np
import time
import os
from mss import mss
from PIL import Image

def capture_screen(bbox=None):
    """捕获屏幕的指定区域"""
    with mss() as sct:
        screenshot = sct.grab(bbox)
        img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
        return np.array(img)

def save_image(img, filename, folder='img'):
    """保存图像到指定文件夹"""
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = os.path.join(folder, filename)
    cv2.imwrite(path, img)

def images_are_equal(img1, img2):
    """判断两张图片是否相等"""
    difference = cv2.subtract(img1, img2)
    b, g, r = cv2.split(difference)

    if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
        return True
    else:
        return False

bbox = {'top': 350, 'left': 150, 'width': 875, 'height': 1200}  # 定义截图区域
prev_img = None

while True:
    current_img = capture_screen(bbox)
    if prev_img is not None and not images_are_equal(prev_img, current_img):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        save_image(current_img, f'screenshot_{timestamp}.png')
        # print(f"Screenshot saved at screenshot_{timestamp}.png")
    prev_img = current_img
    time.sleep(10)  # 每10秒检查一次
