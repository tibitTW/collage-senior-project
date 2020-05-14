#! /usr/bin/env python3

import pygame as pg
from time import time, sleep
import cv2 as cv

from constant import *
from color import *

try:
    from modbus import plc
    print('Modbus module import success.')
except:
    print('Modbus module import failed.')
    exit()

try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
    print('Camera module import success.')
except:
    print('Camera module import failed.')

### initialize keyboard ###
try:
    import kb
    kb.init()
    print('Keyboard initialize success.')

except:
    pass

##### values can be controled #####
torch_speed_value_mm_per_min = 200
solder_speed_value_v = 2
## values will read from PLC ##
gun_height_value = 0
v_value, a_value = 0, 0

######## iniaialize interface(pygame) ########
pg.init()
pg.font.init()

font = pg.font.SysFont('Noto Sans CJK', 40)
font_small = pg.font.SysFont('Noto Sans CJK', 24)

W, H = 370, 272
WIN = pg.display.set_mode((W, H))
# WIN = pg.display.set_mode((W, H), pg.FULLSCREEN)
### initialize modbus connect ###
plc_main = plc()
if plc_main.is_connected:
    print('PLC connected.')
else:
    print('PLC connection error, please check PLC and ethernet cable.')

### initialize camera, including parameters ###
# try:
#     camera_resolution = (640, 480)
#     camera = PiCamera()
#     camera.resolution = camera_resolution
#     camera.brightness = 25
#     rawCapture = PiRGBArray(camera, size=camera_resolution)
# except:
#     print('Camera cannot be used.')
####### functions #######


def draw_title(text: str, color=WHITE):
    text = font.render(text, True, color)

    width = text.get_width()
    x = (W - width)//2
    WIN.blit(text, (x, 120))


def draw_text(text: str, position: int, line: bool = 0, color=YELLOW):
    if type(text) != str:
        return

    if not line:
        text = font.render(text, True, color)
        y = 210
    else:
        text = font_small.render(text, True, color)
        y = 240

    width = text.get_width()
    x = W//6 * (position*2 - 1) - width//2
    WIN.blit(text, (x, y))


def draw_automode_window():
    WIN.fill(BLACK)
    draw_title('AUTO MODE')


def draw_menual_window():

    draw_title('MANUAL MODE')

    WIN.fill(BLACK)
    draw_text(str(torch_speed_value_mm_per_min), 1)
    draw_text('mm/min', 1, 1)
    draw_text(str(solder_speed_value_v), 2)
    draw_text('mm/min', 2, 1)
    draw_text(f'{str(v_value)}/{str(a_value)}', 3)
    draw_text('V/A', 3, 1)


def draw_error_window(message):
    WIN.fill(RED)
    draw_title(message, WHITE)


def draw_message_window(message: str, msg_color: list = WHITE, bgcolor: list = RED):
    WIN.fill(bgcolor)
    draw_title(message, msg_color)


def set_val(id: int):
    kb_locked = False
    temp = ''
    while True:
        key = kb.scan()

        if key == '#':
            if temp != '':
                if id == TORCH_SPEED_VALUE:
                    temp = int(temp)
                    temp = 2000 if temp >= 2000 else temp
                    global torch_speed_value_mm_per_min
                    torch_speed_value_mm_per_min = temp
                    plc_main.write_value(id, temp*2//3)
                elif id == SOLDER_SPEED_VALUE:
                    temp = int(temp)
                    temp = 10 if temp >= 10 else temp
                    global solder_speed_value_v
                    solder_speed_value_v = temp
                    plc_main.write_value(id, temp*400)
            else:
                pass
            return

        elif key == '*':
            pass
        elif key != 0:
            if not kb_locked:
                temp += key
                kb_locked = True

        else:
            kb_locked = False

        sleep(0.1)


def close():
    try:
        pg.quit()
        kb.close()
        plc_main.disconnect()
    finally:
        exit()


connect_check_record_time = time()
# main struct
while True:
    # quit scrpit(for keyboard)
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and (event.key == pg.K_ESCAPE or pg.K_q)):
            close()

    if plc_main.connect():
        mode = plc_main.get_status()
        # 自動模式
        if mode == AUTO_MODE:
            # 影像辨識
            if plc_main.read_value(AUTO_START):
                pass
            draw_automode_window()

        # 手動模式
        elif mode == MENUAL_MODE:
            try:
                k = kb.scan()
                if k == '*':
                    print('Setting Value')
                    if plc_main.setting_value(SET_GUN_SPEED):
                        set_val(TORCH_SPEED_VALUE)
                        print(torch_speed_value_mm_per_min)
                    elif plc_main.setting_value(SET_SOLDER_SPEED):
                        set_val(SOLDER_SPEED_VALUE)
                        print(solder_speed_value_v)
                    else:
                        pass
            except Exception as e:
                print(e)

            draw_menual_window()

        else:
            draw_message_window('RESETING...', bgcolor=BLACK)

    # 連線錯誤
    else:
        if (time() - connect_check_record_time) // 5:
            connect_check_record_time = time()
            print('PLC connection error, please check PLC and ethernet cable.')

        draw_message_window('Connection Error')

    pg.display.update()
    sleep(0.1)

close()
