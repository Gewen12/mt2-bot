import numpy as np
from pyautogui import *
import keyboard
import random
import win32api, win32con
from mss import mss
from PIL import Image
import cv2
import winsound


def left_click(x, y):
    win32api.SetCursorPos((x, y))
    time.sleep(random.randint(10, 100) / 10000)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(random.randint(10, 100) / 10000)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def right_click(x, y):
    win32api.SetCursorPos((x, y))
    time.sleep(random.randint(10, 100) / 100)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    time.sleep(random.randint(10, 100) / 100)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

def convert_rgb_to_bgr(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def take_screenshot(monitor):
    ememes = mss()
    sct_img = ememes.grab(monitor)
    img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
    img = np.array(img)
    img = convert_rgb_to_bgr(img)
    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def choose_wurmchen():
    leiste = take_screenshot(monitor_leiste)
    if leiste[15, 25, 0] == 173:
        print("Wurm on slot 1")
        right_click(15 + 310, 607)
    elif leiste[15, 57, 0] == 173:
        print("Wurm on slot 2")
        right_click(47 + 310, 608)
    elif leiste[15, 89, 0] == 173:
        print("Wurm on slot 3")
        right_click(79 + 310, 609)
    elif leiste[15, 121, 0] == 173:
        print("Wurm on slot 4")
        right_click(111 + 310, 610)
    elif leiste[15,121,0] == 0:
        left_click(404,295)
    else:
        while True:
            print("Keine Würmers mehr")
            winsound.Beep(1500, 1500)
            sys.exit()


def start_fishing():
    right_click(471, 608)
    #time.sleep(3)


def is_fishing(window_fishing):
    if window_fishing[12, 60, 0] == 10 and window_fishing[12, 60, 1] == 30:
        return True
    else:
        return False


a = 134
monitor_komplekt = {'top': 80, 'left': 100, 'width': 70, 'height': 15}
monitor1 = {'top': 150, 'left': 174, 'width': a, 'height': a}
monitor_leiste = {'top': 593, 'left': 310, 'width': 135, 'height': 30}
invi = {'top': 250, 'left': 640, 'width': 150, 'height': 320}
circle = (255, 173, 199)
fish = (56, 91, 123)
fish2 = (56, 96, 128)
fishing_open = False
while keyboard.is_pressed('q') == False:
    inventar = take_screenshot(invi)
    if inventar[289,12,0] != 11:
        print(inventar[289,12,0])
        print("piep")
        winsound.Beep(1500, 1500)
    cv2.imwrite("invi.png",inventar)
    screen = take_screenshot(monitor1)
    choose_wurmchen()
    start_fishing()
    window_fishing = take_screenshot(monitor_komplekt)
    fishing_open = is_fishing(window_fishing)
    time.sleep(2)
    while fishing_open:
        screen = take_screenshot(monitor1)
        fishing_open = is_fishing(window_fishing)
        window_fishing = take_screenshot(monitor_komplekt)
        for i in range(0, a, 4):
            for j in range(0, a, 4):
                # <= screen[i + 1, j] <= 90 and 80 <= screen[i, j + 1] <= 90 and 80 <= screen[i + 1, j + 1] <= 90 \
                if 95 <= screen[i, j][1] <= 103 and 95 <= screen[i + 1, j][1] <= 103 and 95 <= screen[i, j + 1][
                    1] <= 103 and 95 <= screen[i + 1, j + 1][1] <= 103 \
                        and 120 <= screen[i, j][0] <= 128 and 120 <= screen[i + 1, j][0] <= 128 and 120 <= \
                        screen[i, j + 1][0] <= 128 and 120 <= screen[i + 1, j + 1][0] <= 128:
                    #screen2 = take_screenshot(monitor1)
                    # if screen[i,j] == screen2[i,j] and screen[i+1,j] == screen2[i+1,j] and screen[i,j+1] == screen2[i,j+1] and screen[i+1,j+1] == screen2[i+1,j+1]:
                    win32api.SetCursorPos((j + 174, i + 150))
                    if (screen[60, 128][0] == 222 and screen[60, 128][1] == 157 and screen[60, 128][2] == 88): #and \
                           # (screen2[i, j][1] == screen[i, j][1] and screen2[i + 1, j][1] == screen[i + 1, j][1] and
                            # screen2[i, j + 1][1] == screen[i, j + 1][1] and screen2[i + 1, j + 1][1] ==
                            # screen[i + 1, j + 1][1]):
                        # and 120 <= screen2[i,j][0] <= 128 and  120 <= screen2[i+1,j][0] <= 128 and  120 <= screen2[i,j+1][0] <= 128 and  120 <= screen2[i+1,j+1][0] <= 128) :
                        print("click fish")
                        left_click(j +1+ 174, i+1 + 150)
                        time.sleep(0.8)
                    fishing_open = is_fishing(window_fishing)
                    screen = take_screenshot(monitor1)
