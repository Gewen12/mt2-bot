import numpy as np
from pyautogui import *
import keyboard
import random
import win32api, win32con
from mss import mss
from PIL import Image
import cv2


def left_click(x, y):
    win32api.SetCursorPos((x, y))
    time.sleep(random.randint(10, 100) / 1000)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(random.randint(10, 100) / 1000)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def right_click(x, y):
    win32api.SetCursorPos((x, y))
    time.sleep(random.randint(10, 100) / 100)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    time.sleep(random.randint(10, 100) / 1000)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

def match_template(img, template, threshold=0.9):
        """
        Matches template image in a target grayscaled image
        """
        #print(img)
        #print(template)
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        matches = np.where(res >= threshold)
        return matches

def find_template( name, threshold=0.9):
    image = take_screenshot(monitor)

    return match_template(
        image,
        templates[name],
        threshold
    )

def scaled_find_template(name, image=None, threshold=0.9, scales=[1.0, 0.9, 1.1]):
    image = take_screenshot(monitor)

    initial_template = templates[name]
    for scale in scales:
        scaled_template = cv2.resize(initial_template, (0,0), fx=scale, fy=scale)
        matches = match_template(
            image,
            scaled_template,
            threshold
        )
        if np.shape(matches)[1] >= 1:
            return matches
    return matches


def can_see_object(template, threshold=0.9):
        matches = find_template(template, threshold=threshold)
        return np.shape(matches)[1] >= 1

def click_object( template, offset=(0, 0)):
    if can_see_object(template):
        matches = find_template(template)

        x = matches[1][0] + offset[0]
        y = matches[0][0] + offset[1]

        left_click(x,y)

        time.sleep(0.5)

def convert_rgb_to_bgr(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def take_screenshot(monitor):
    ememes = mss()
    sct_img = ememes.grab(monitor)
    img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
    img = np.array(img)
    img = convert_rgb_to_bgr(img)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img_gray

def sleepen():
    time.sleep(random.randint(30, 60) / 10)

def sleepen_low():
    time.sleep(random.randint(5, 15) / 10)

chars=[(130,272),(140,316),(132,358),(150,402),(112,442)]
static_templates = {
    'event_button': 'assets/seher/event_button.png',
    'seherwettstreit': 'assets/seher/seherwettstreit.png',
    'start': 'assets/seher/start.png',
    'ja': 'assets/seher/ja.png',
    '1': 'assets/seher/1.png',
    '2': 'assets/seher/2.png',
    '3': 'assets/seher/3.png',
    '4': 'assets/seher/4.png',
    '5': 'assets/seher/5.png',
    '6': 'assets/seher/6.png',
    '7': 'assets/seher/7.png',
    '8': 'assets/seher/8.png',
    '0': 'assets/seher/0.png',
}

templates = { k: cv2.imread(v, 0) for (k, v) in static_templates.items() }
monitor = {'top': 0, 'left': 0, 'width': 1680, 'height': 1050}
while keyboard.is_pressed('q') == False:
    screen = take_screenshot(monitor)
    #cv2.imwrite("spende.png", take_screenshot(monitor))
    while not can_see_object('seherwettstreit'):
        click_object('event_button')
    while not can_see_object('start'):
        click_object('seherwettstreit')
    while not can_see_object('ja'):
        click_object('start')
    while not can_see_object('1'):
        click_object('ja')
    for i in range(0,9):
        while can_see_object(str(i)):
            click_object(str(i))
            sleepen()



