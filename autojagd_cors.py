import ctypes

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

PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0,
                        ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


chars=[(130,272),(140,316),(132,358),(150,402),(112,442)]
static_templates = {
    'aura': 'assets/cors/aura.png',
    'pot': 'assets/cors/pot.png',
    'splitter': 'assets/cors/splitter.png',
    'start': 'assets/cors/start.png',
    'tapfi': 'assets/cors/tapfi.png',
    'start_not_pressed': 'assets/cors/start_not_pressed.png',
    'start_pressed': 'assets/cors/start_pressed.png',
    'stop_not_pressed': 'assets/cors/stop_not_pressed.png',
    'stop_pressed': 'assets/cors/stop_pressed.png',
    'restart': 'assets/cors/restart.png',
}
templates = { k: cv2.imread(v, 0) for (k, v) in static_templates.items() }
monitor = {'top': 0, 'left': 0, 'width': 1680, 'height': 1060}
while keyboard.is_pressed('q') == False:
    screen = take_screenshot(monitor)
    cv2.imwrite("spende.png", take_screenshot(monitor))
    if __name__ == '__main__':
        time.sleep(3)
        PressKey(0x04)
        sleepen_low()
        ReleaseKey(0x04)
        PressKey(0x02)
        sleepen_low()
        ReleaseKey(0x02)
        sleepen_low()
        if can_see_object('start_pressed'):
            click_object('start_pressed')
        while keyboard.is_pressed('q') == False:
            if can_see_object('restart'):
                click_object('restart')
            if(random.randint(1,5) == 5):
                PressKey(0x02)
                sleepen_low()
                ReleaseKey(0x02)
            if can_see_object('splitter'):
                if can_see_object('stop_not_pressed'):
                    click_object('stop_not_pressed')
                while can_see_object('splitter'):
                    if can_see_object('splitter'):
                        1click_object('splitter')
                if can_see_object('start_not_pressed'):
                    click_object('start_not_pressed')



