#! /usr/bin/env python3

import pygame as pg

from constant import *
from modbus import plc
import kb

from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2 as cv

####### color map #######
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
##### control value #####
turch_speed_value = 0
solder_speed_value = 0
gun_height_value = 0
v_value, a_value = 0, 0
#########################

######## iniaialize interface(pygame) ########
pg.init()
pg.font.init()

font = pg.font.SysFont('Noto Sans CJK', 40)
font_small = pg.font.SysFont('Noto Sans CJK', 24)

W, H = 370, 272
# WIN = pg.display.set_mode((W, H))
WIN = pg.display.set_mode((W, H), pg.FULLSCREEN)

### initialize modbus connect and keyboard ###
plc_main = plc()
print(plc_main.connect())
kb.init()

### initialize camera, including parameters ###
camera_resolution = (640, 480)
camera = PiCamera()
camera.resolution = camera_resolution
camera.brightness = 25
rawCapture = PiRGBArray(camera, size=camera_resolution)

####### functions #######


def print_title(text: str, color=WHITE):
    text = font.render(text, True, color)

    width = text.get_width()
    x = (W - width)//2
    WIN.blit(text, (x, 120))


def print_text(text: str, position: int, line: bool = 0, color=YELLOW):
    if type(text) != str:
        print('Text type must be string.')
        return

    if not line:
        text = font.render(text, True, color)
        y = 210
    else:
        text = font_small.render(text, True, color)
        y = 240

    width = text.get_width()
    x = W//8 * (position*2 - 1) - width//2
    WIN.blit(text, (x, y))


def draw_main_screen():
    WIN.fill(BLACK)

    try:
        turch_speed_value = plc_main.read_value(TORCH_SPEED_VALUE)
        solder_speed_value = plc_main.read_value(SOLDER_SPEED_VALUE)
        v_value = plc_main.read_value(GUN_VOLTAGE)
        a_value = plc_main.read_value(GUN_AMP)

        if plc_main.read_value(AUTO_MODE):
            print_title('AUTO MODE')
        elif plc_main.read_value(MENUAL_MODE):
            print_title('MANUAL MODE')

        print_text(str(turch_speed_value * 1.5), 1)
        print_text('mm/min', 1, 1)
        print_text(str(solder_speed_value), 2)
        print_text('mm/min', 2, 1)
        print_text(str(gun_height_value), 3)
        print_text('mm', 3, 1)
        print_text(f'{str(v_value)}/{str(a_value)}', 4)
        print_text('V/A', 4, 1)
    except:
        pass


def set_val(id: int):
    if id == TORCH_SPEED_VALUE:
        address = 10
        default_val = turch_speed_value
    elif id == SOLDER_SPEED_VALUE:
        address = 12
        default_val = solder_speed_value

    locked = False
    temp = ''
    while True:
        key = kb.scan()
        if key == '#':
            break
        elif key == '*':
            pass
        elif key != 0:
            if not locked:
                temp += key
                locked = key

        else:
            locked = False

        if int(temp) >= 2000:
            temp = '2000'

    if temp != '':
        if id == TORCH_SPEED_VALUE:
            plc_main.write_value(id, int(temp))
        plc_main.write_value(id, int(temp))
        return

    else:
        plc_main.write_value(id, default_val)
        return


def close():
    pg.quit()
    kb.close()
    plc_main.disconnect()
    exit()


#########　main loop #########
while True:
    for event in pg.event.get():
        # quit script
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            close()

    if not plc_main.is_connected:
        plc_main.connect()

    ############ plc buttons status #############
    # manual mode, at plc S4
    if plc_main.read_value(MENUAL_MODE):
        k = kb.scan()
        if k == '*':

            # read plc coil M13
            if plc_main.read_value(SET_GUN_SPEED):
                set_val(TORCH_SPEED_VALUE)

            # read plc coil M14
            elif plc_main.read_value(SET_SOLDER_SPEED):
                set_val(SOLDER_SPEED_VALUE)
            else:
                pass

    # automode
    elif plc_main.read_value(AUTO_MODE):
        if plc_main.read_value(AUTO_START):

            # camera detect
            for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
                image = frame.array
                cv.imshow('frame', image)

                rawCapture.truncate(0)

    draw_main_screen()

    pg.display.update()
    pg.time.delay(100)

close()
