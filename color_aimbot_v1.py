import math
import threading
import time

import numpy as np
import cv2
import keyboard
import serial
import win32api, win32con
from PIL import Image, ImageGrab
import scipy
from mss import mss

import PyArduinoBot_v2
from PyArduinoBot_v2 import arduino_mouse

# get the Screen resolution.
scalex = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
scaley = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

PyArduinoBot_v2.num_steps = 5
PyArduinoBot_v2.FOV = 1
PyArduinoBot_v2.FPS = True
# print("monitor scale:", scalex,scaley)

print(PyArduinoBot_v2.num_steps)

# ====== CHANGE THESE ======
port = 'COM12'
color_to_use = 'red'
# ==========================

if color_to_use == 'purple':
    lpoint = [135, 35, 20]
    upoint = [155, 255, 255]
    
if color_to_use == 'yellow':
    lpoint = [22, 46, 255]
    upoint = [38, 255, 255]

if color_to_use == 'red':
    lpoint = [0, 95, 95]
    upoint = [4, 235, 255]

monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
#monitor = {"top": 300, "left": 650, "width": 600, "height":500}
sct = mss()

#pt= (310,238) # screen center and crosshair position #win32api.GetCursorPos()
pt = (960, 538)


def sct_screenshot():
    global sct
    # screenshot = sct.shot(output=None)
    try:
        img = np.array(sct.grab(monitor))
        return img
    except:
        sct = mss()
        return print("error with image")


def adjust_to_fov():
    if keyboard.is_pressed(','):
        PyArduinoBot_v2.FOV += 0.01
        print(PyArduinoBot_v2.FOV, "Increasing FOV adjuster!!!")
    if keyboard.is_pressed('.'):
        PyArduinoBot_v2.FOV -= 0.01
        print(PyArduinoBot_v2.FOV, "Lowering FOV adjuster!!!")


def close_script():
    global bot
    bot = True
    while bot:
        #adjust_to_fov()

        if keyboard.is_pressed('capslock'):
            bot = False
            print("Color bot shutting down!")
            exit()
        time.sleep(1)


def mouse_action(x, y, button):
    global fov, arduino
    # print("mouse action:", x,y)
    # print("adjusted action:", adj_x, adj_y)
    # print(button)
    arduino_mouse(x, y, ard=arduino, button=button, winType='FPS')
    #time.sleep(0.25)


def detect_color():
    global bot, pt
    bot = True
    while bot:
        image = sct_screenshot()
        img = image
        image = cv2.rectangle(image, pt1=(1520, 335), pt2=(1920, 755), color=(0, 0, 0), thickness=-1)
        image = cv2.rectangle(image, pt1=(370, 29), pt2=(1510, 70), color=(0, 0, 0), thickness=-1)
        image = cv2.rectangle(image, pt1=(1450, 90), pt2=(1920, 220), color=(0, 0, 0), thickness=-1)
        image = cv2.circle(image, (203, 253), radius=215, color=(0, 0, 0), thickness=-1)
        try:
            # define the list of boundaries
            close_points = []
            # loop over the boundaries
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            # Define the lower and upper HSV values for the color range you want to detect
            lower = np.array(lpoint, dtype="uint8")
            upper = np.array(upoint, dtype="uint8")
            # Create a mask to detect the specified color range
            mask = cv2.inRange(image, lower, upper)
            #detected = cv2.bitwise_and(image, image, mask=mask)
            kernel = np.ones((3, 3), np.uint8)
            dilated = cv2.dilate(mask, kernel, iterations=4)
            ret, thresh = cv2.threshold(dilated, 40, 255, 0)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(img, contours, -1, (0, 255, 0), 1, cv2.LINE_AA)
            for c in contours:
                if cv2.contourArea(c) > 200:
                    # print(cv2.pointPolygonTest(c, pt, True))
                    # close_poly.append(cv2.pointPolygonTest(c, pt, True))
                    x1, y1, w1, h1 = cv2.boundingRect(c)
                    # print((x1 + (w1 / 2)), (y1 + (h1 / 2)))
                    close_points.append((round(x1 + (w1 / 2)), round(y1 + (h1 / 9))))


            # print("closest point:", min(close_poly))
            if len(contours) != 0:

                # print("pt x and y:", pt)
                closest = close_points[scipy.spatial.KDTree(close_points).query(pt)[1]]
                cv2.circle(img, (closest[0], closest[1]), radius=3, color=(0, 0, 255), thickness=-1)
                cv2.line(img, pt, (closest[0], closest[1]), (255, 0, 0), 2)

                if keyboard.is_pressed("shift"):
                    #print("desintation:", closest[0], closest[1])
                    #mouse_action(closest[0], closest[1], button=None)
                    mouse_action(closest[0], closest[1], button='left')
        except:
            pass
        cv2.imshow("images", img)
        cv2.waitKey(5)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    global arduino, port
    port = 'COM5'
    baudrate = 115200
    arduino = serial.Serial(port=port, baudrate=baudrate, timeout=.1)
    print("Starting aimbot!!!")
    #time.sleep(5)
    threading.Thread(target=close_script).start()
    print("Aimbot On!!!")
    detect_color()  # aim lab blue ball
    print("done!!")
