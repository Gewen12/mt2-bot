import winsound

import numpy as np
from pyautogui import *
import keyboard
import random
import win32api, win32con
from mss import mss
from PIL import Image
import cv2
import pytesseract
import imutils


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
    time.sleep(random.randint(10, 30))

def sleepen_low():
    time.sleep(random.randint(5, 15) / 10)

def change_window_from_to(window1,window2):
    if can_see_object(window1):
        click_object(window1)
        time.sleep(2)
        if can_see_object(window2):
            click_object(window2)
            time.sleep(2)
            if can_see_object('suchen'):
                left_click(123,488)


x=200
y=200
monitor = {'top': 0, 'left': 0, 'width': 800, 'height': 620}
items = {'top': x, 'left': y, 'width': 500, 'height': 25}
static_templates = {
            'diamant': 'assets/markt/diamant.png',
            'granat': 'assets/markt/granat.png',
            'jade': 'assets/markt/jade.png',
            'onyx': 'assets/markt/onyx.png',
            'rubin': 'assets/markt/rubin.png',
            'saphir': 'assets/markt/saphir.png',
            'suchen': 'assets/markt/suchen.png',
}
templates = { k: cv2.imread(v, 0) for (k, v) in static_templates.items() }
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

while keyboard.is_pressed('q') == False:
    screen = take_screenshot(monitor)
    gray = take_screenshot(items)
    data = pytesseract.image_to_string(gray)
    item = data.split()
    change_window_from_to('rubin','jade')
    if len(item) >= 2:
        if item[1].find('jade'):
            if len(item) >= 6:
                print(item[5])
                price = item[5].replace(',', '')
                price = int(price.replace('.', ''))
                if(70000000 <= price <= 9000000):
                    winsound.Beep(3500, 1500)
    change_window_from_to('jade', 'onyx')
    screen = take_screenshot(monitor)
    gray = take_screenshot(items)
    data = pytesseract.image_to_string(gray)
    item = data.split()
    if len(item) >= 2:
        print(item[0], item[1])
        if item[1].find('onyx'):
            if len(item) >= 6:
                print(item[5])
                price = item[5].replace(',', '')
                price = int(price.replace('.', ''))
                if (20000000 <= price <= 5000000):
                    winsound.Beep(1500, 1500)
    change_window_from_to('onyx', 'rubin')
    screen = take_screenshot(monitor)
    gray = take_screenshot(items)
    data = pytesseract.image_to_string(gray)
    item = data.split()
    if len(item) >= 2:
        if item[1].find('rubin'):
            if len(item) >= 6:
                print(item[5])
                price = item[5].replace(',', '')
                price = int(price.replace('.', ''))
                if (70000000 <= price <= 9000000):
                    winsound.Beep(2500, 1500)
    sleepen()