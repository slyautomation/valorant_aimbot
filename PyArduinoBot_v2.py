# In seconds. Any duration less than this is rounded to 0.0 to instantly move
# the mouse.
import ctypes
import math
import random
import time
import ctypes.wintypes
import serial

# Credits to: # Windows implementation of PyAutoGUI functions.
# # BSD license
# # Al Sweigart al@inventwithpython.com - https://github.com/asweigart/pyautogui
num_steps = 10
FOV = 1.0
FPS = False
# FIXES SLOW TIME.SLEEP IN WINDOWS OS
timeBeginPeriod = ctypes.windll.winmm.timeBeginPeriod #new
timeBeginPeriod(1) #new

if FPS:
    addF = (960, 540)
else:
    cursor = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
    addF = (cursor.x, cursor.y)
previousList = [addF]
lastList = 0,0
storagex = 0
adj_storagex = 0
storagey = 0
adj_storagey = 0
def linear(n):
    """
    Returns ``n``, where ``n`` is the float argument between ``0.0`` and ``1.0``. This function is for the default
    linear tween for mouse moving functions.

    This function was copied from PyTweening module, so that it can be called even if PyTweening is not installed.
    """

    # We use this function instead of pytweening.linear for the default tween function just in case pytweening couldn't be imported.
    if not 0.0 <= n <= 1.0:
        raise print("Argument must be between 0.0 and 1.0.")
    return n

def _position():
    """Returns the current xy coordinates of the mouse cursor as a two-integer
    tuple by calling the GetCursorPos() win32 function.

    Returns:
      (x, y) tuple of the current xy coordinates of the mouse cursor.
    """

    cursor = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
    return (cursor.x, cursor.y)

def get_decimal_part(number):
    # Get the decimal part using modulo operator and round it to 6 decimal places
    decimal_part = abs(number) % 1
    decimal_part = round(decimal_part, 6)  # Round to 6 decimal places
    return decimal_part


def getPointOnLine_v1(x1, y1, x2, y2, n):
    global FOV, num_steps, storagex, adj_storagex, storagey, adj_storagey
    """
    Returns an (x, y) tuple of the point that has progressed a proportion ``n`` along the line defined by the two
    ``x1``, ``y1`` and ``x2``, ``y2`` coordinates.

    This function was copied from pytweening module, so that it can be called even if PyTweening is not installed.
    """
    print("Target x:", x2 - x1)
    print("Target x FOV:", (x2 - x1) * FOV)
    print(n)
    x = (((x2 - x1) * (1 / (num_steps)))) * FOV
    y = (((y2 - y1) * (1 / (num_steps)))) * FOV
    storagex += x
    storagey += y
    print("x:", x)
    print("Storage x:", storagex)
    if x < 0:
        f_x = str(math.ceil(abs(x)) * -1)
        adj_storagex += math.ceil(abs(x)) * -1
    else:
        f_x = str(math.ceil(x))
        adj_storagex += math.ceil(x)
    if y < 0:
        f_y = str(math.ceil(abs(y)) * -1)
        adj_storagey += math.ceil(abs(y)) * -1
    else:
        f_y = str(math.ceil(y))
        adj_storagey += math.ceil(y)
    print("Adj Storage x:", adj_storagex)

    if n == num_steps - 1:
        if adj_storagex != storagex:
            if x > 0:
                f_x = str(math.ceil(abs(storagex - adj_storagex)))
            else:
                f_x = str(math.ceil(abs(storagex - adj_storagex)) * -1)
        if adj_storagey != storagey:
            if y > 0:
                f_y = str(math.ceil(abs(storagey - adj_storagey)))
            else:
                f_y = str(math.ceil(abs(storagey - adj_storagey)) * -1)
    print(f_x, f_y)
    return (f_x + ":" + f_y)

def getPointOnLine(x1, y1, x2, y2, n):
    global FOV, num_steps, storagex, adj_storagex, storagey, adj_storagey
    """
    Returns an (x, y) tuple of the point that has progressed a proportion ``n`` along the line defined by the two
    ``x1``, ``y1`` and ``x2``, ``y2`` coordinates.

    This function was copied from pytweening module, so that it can be called even if PyTweening is not installed.
    """
    print("Target x:", x2 - x1)
    print("Target x FOV:", (x2 - x1) * FOV)
    print(n)
    x = (((x2 - x1) * (1 / (num_steps)))) * FOV
    y = (((y2 - y1) * (1 / (num_steps)))) * FOV
    storagex += x
    storagey += y
    print("x:", x)
    print("Storage x:", storagex)
    if x < 0:
        f_x = str(math.ceil(abs(x)) * -1)
        adj_storagex += math.ceil(abs(x)) * -1
    else:
        f_x = str(math.ceil(x))
        adj_storagex += math.ceil(x)
    if y < 0:
        f_y = str(math.ceil(abs(y)) * -1)
        adj_storagey += math.ceil(abs(y)) * -1
    else:
        f_y = str(math.ceil(y))
        adj_storagey += math.ceil(y)
    print("Adj Storage x:", adj_storagex)
    print(f_x, f_y)
    return (f_x + ":" + f_y)

def getPoint(x1, y1, x2, y2, n):
    global FOV, num_steps
    """
    Returns an (x, y) tuple of the point that has progressed a proportion ``n`` along the line defined by the two
    ``x1``, ``y1`` and ``x2``, ``y2`` coordinates.

    This function was copied from pytweening module, so that it can be called even if PyTweening is not installed.
    """
    x = (((x2 - x1) * (1 / (num_steps)))) * FOV
    y = (((y2 - y1) * (1 / (num_steps)))) * FOV

    print("getPoint x:", x)
    return (math.ceil(x), math.ceil(y))


def _mouseMoveDrag(x, y, ard=None, winType=None):
    global previousList, lastList, num_steps, adj_storagex, storagex, storagey, adj_storagey

    adj_storagex = 0
    storagex = 0
    storagey = 0
    adj_storagey = 0
    if winType == 'FPS':
        startx, starty = (960, 540)
    else:
        startx, starty = _position()

    arduino = ard
    # If the duration is small enough, just move the cursor there instantly.
    steps = [(x, y)]
    print('num_steps:', num_steps)
    print("start:", startx, starty)
    steps = [getPointOnLine(startx, starty, x, y, n) for n in range(num_steps)]
    #print("Final Coords sent:", steps)
    # Making sure the last position is the actual destination.
    if not FPS:
        steps.pop()
        steps.pop(0)


    steps = str(steps)
    print("Final Coords sent:", steps)
    arduino.write(bytes(steps, 'utf-8'))

def getLatestStatus(ard=None):
    status = 'Nothing'
    while ard.inWaiting() > 0:
        status = ard.readline()
    return status

def arduino_mouse(x=100, y=100, ard=None, button=None, winType=None):
    #
    #print("arduino mouse is:", button)
    #if button == None:
    _mouseMoveDrag(x, y, ard=ard, winType=winType)
    time_start = time.time()
    stat = getLatestStatus(ard)
    #print(stat)
    #print(time.time() - time_start)
    if button == None:
        time.sleep(0.01)
    else:
        time.sleep(0.05)
    c = random.uniform(0.02,0.05)
    #time.sleep(0.05)
    #print("passed arduino mouse is:", button)
    if button == 'left':
        ard.write(bytes(button, 'utf-8'))
        stat = getLatestStatus(ard)
        #print(stat)
        time.sleep(c)
    if button == 'right':
        ard.write(bytes(button, 'utf-8'))
        stat = getLatestStatus(ard)
        #print(stat)
        time.sleep(c)


if __name__ == '__main__':
    port = 'COM5'
    baudrate = 115200
    arduino = serial.Serial(port=port, baudrate=baudrate, timeout=.1)
    time.sleep(5)
    #time.sleep(3.5)
    print('using arduino mouse to move')
    if FPS:
        addF = (960,540)
    else:
        cursor = ctypes.wintypes.POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
        addF = (cursor.x, cursor.y)
    print(addF)
    previousList = [addF]
    lastList = 0,0
    arduino_mouse(x=200, y=200, ard=arduino, button='right')