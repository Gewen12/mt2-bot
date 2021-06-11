import numpy as np
from pyautogui import *
import keyboard
import random
import win32api,win32con
from mss import mss
from PIL import Image
import cv2

def convert_rgb_to_bgr(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def take_screenshot(monitor):
    screen = mss()
    sct_img = screen.grab(monitor)
    img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
    img = np.array(img)
    img = convert_rgb_to_bgr(img)
    #img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

while True:
    monitor_komplekt = {'top': 80, 'left': 100, 'width': 70, 'height': 15}
    window_fishing = take_screenshot(monitor_komplekt)
    print(window_fishing[12,60])
    time.sleep(1)

