#! /usr/bin/env python3

import pygame as pg
from time import time, sleep
from modbus import plc
import os
from datetime import datetime
from time import time

# modules for imgae processing and machine learning
import cv2 as cv
import numpy as np
# from sklearn.linear_model import LinearRegression

# import constants and colors(for convenience)
from constant import TORCH_SPEED_VALUE, SOLDER_SPEED_VALUE
from constant import MENUAL_MODE, AUTO_MODE
# from constant import GUN_VOLTAGE, GUN_AMP
from constant import SET_GUN_SPEED, SET_SOLDER_SPEED

log = open('./log.txt', 'a')


def get_time_now():  # get current time(for log)
    timenow = datetime.now()
    return f'[{timenow.year}/{timenow.month:02d}/{timenow.day:02d} ' + \
        '{timenow.hour:02d}:{timenow.minute:02d}:' + \
        '{timenow.second:02d}:{timenow.microsecond}] '


# initialize camera
try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray

    camera_resolution = (1600, 1200)
    camera = PiCamera()
    camera.resolution = camera_resolution
    camera.brightness = 25
    camera.exposure_mode = 'backlight'
    camera.contrast = 25
    rawCapture = PiRGBArray(camera, size=camera_resolution)
    log.write(get_time_now() + 'Camera initialized success.\n')
except:
    log.write(get_time_now() + 'Camera initialized failed.\n')

#   initialize keyboard   #
try:
    import kb
    kb.init()
    log.write(get_time_now() + 'Keyboard initialize success.\n')
except:
    pass

# ------------------------------------------------------------------- #
# |                          system window                          | #
# |                                                                 | #

# colors #
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


def _draw_title(text: str, color=WHITE, y=260):
    text = title_font.render(text, True, color)

    width = text.get_width()
    x = (W - width)//2
    WIN.blit(text, (x, y))


def _draw_text(text: str, position: int, line: bool = 0, color=YELLOW):
    if type(text) != str:
        return

    if not line:
        text = title_font.render(text, True, color)
        y = 400
    else:
        text = regular_font.render(text, True, color)
        y = 480

    width = text.get_width()
    x = W//6 * (position*2 - 1) - width//2
    WIN.blit(text, (x, y))


def draw_menual_window():

    WIN.fill(BLACK)
    _draw_title('MANUAL MODE', y=180)
    color = RED if torch_speed_value_mm_per_min > 2000 else WHITE

    _draw_text(str(torch_speed_value_mm_per_min), 1, color=color)
    _draw_text('mm/min', 1, 1)
    _draw_text(str(solder_speed_value_mm_per_min), 2)
    _draw_text('mm/min', 2, 1)
    _draw_text(f'{str(v_value)}/{str(a_value)}', 3)
    _draw_text('V/A', 3, 1)
    pg.display.update()


def draw_message_window(msg: str, color: list = WHITE, bgcolor: list = RED):
    WIN.fill(bgcolor)
    _draw_title(msg, color)
    pg.display.update()


def draw_setting_value_window(id: int, value: str):
    title_font_color = WHITE
    WIN.fill(BLACK)
    if id == TORCH_SPEED_VALUE:
        if value != '' and int(value) > 2000:
            title_font_color = RED
        _draw_title('SETTING TORCH', y=40)
    elif id == SOLDER_SPEED_VALUE:
        _draw_title('SETTING SOLDER', y=40)
    _draw_title('SPEED VALUE', y=90)
    val = title_font.render(value, True, title_font_color)
    width = val.get_width()
    x = W//2 - width//2
    WIN.blit(val, (x, 180))
    pg.display.update()


def close():
    try:
        pg.quit()
        kb.close()
        plc_main.disconnect()
    finally:
        exit()

#                                                                     #
#                                                                     #
# ------------------------------------------------------------------- #


def set_val(id: int):
    kb_locked = False
    temp = ''
    while True:
        key = kb.scan()

        if plc_main.setting_value_end():
            if temp != '':
                if id == TORCH_SPEED_VALUE:
                    temp = int(temp)
                    global torch_speed_value_mm_per_min
                    torch_speed_value_mm_per_min = temp
                    plc_main.write_value(id, temp)
                elif id == SOLDER_SPEED_VALUE:
                    temp = float(temp)
                    global solder_speed_value_mm_per_min
                    solder_speed_value_mm_per_min = temp
                    plc_main.write_value(id, temp)
            else:
                pass
            return

        if key == '#':
            temp = temp[:-1]
        elif key == '*':
            if id == SOLDER_SPEED_VALUE:
                temp += '.'
        elif key != 0:
            if not kb_locked:
                temp += key
                if id == TORCH_SPEED_VALUE:
                    temp = '4000' if int(temp) > 4000 else temp
                elif id == SOLDER_SPEED_VALUE:
                    temp = '1000' if float(temp) > 1000 else temp
                kb_locked = True

        else:
            kb_locked = False

        draw_setting_value_window(id, temp)
        pg.display.update()

        sleep(0.1)


# def get_puddle_contour(mask):

#     contour_point = [hsv_image.shape[1], 0]

#     y = 0
#     for row in contour_mask:
#         x = 0
#         for point in row:
#             if x < contour_point[0]:
#                 contour_point = [x, y]
#             x += 1
#         y += 1

#     return contour_point


# def get_middle_line_parameters(mask):
#     X, Y = [], []
#     y = 0
#     for row in mask:
#         x = 0
#         for point in row:
#             if point:
#                 X.append([x])
#                 Y.append(y)
#             x += 1
#         y += 1
#     lr_model = LinearRegression().fit(X, Y)
#     return lr_model.coef_, lr_model.intercept_


hsv_color_bottom = np.array([48, 23, 44])
hsv_color_top = np.array([103, 113, 138])
line_color_bottom = np.array([102, 91, 134])
line_color_top = np.array([112, 215, 146])
# values can be controled
torch_speed_value_mm_per_min = 200
solder_speed_value_mm_per_min = 350
# values will read from PLC
gun_height_value = 0
v_value, a_value = 0, 0

# initialize interface(pygame)
pg.init()
pg.font.init()
# initialize font(pygame)
title_font = pg.font.SysFont('Noto Sans CJK', 80)
regular_font = pg.font.SysFont('Noto Sans CJK', 40)

W, H = 720, 560
# WIN = pg.display.set_mode((W, H))
WIN = pg.display.set_mode((W, H), pg.FULLSCREEN)

# initialize modbus connect
plc_main = plc()
if plc_main.is_connected:
    log.write(get_time_now() + 'PLC connect success.\n')
    plc_main.write_value(TORCH_SPEED_VALUE, torch_speed_value_mm_per_min)
    plc_main.write_value(SOLDER_SPEED_VALUE, solder_speed_value_mm_per_min)
else:
    log.write(get_time_now() +
              'PLC connection error, please check PLC and ethernet cable.\n')

connect_check_record_time = time()
while True:  # main struct

    # quit scrpit(for keyboard)
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                close()
        elif event.type == pg.QUIT:
            close()

    if plc_main.connect():
        mode = plc_main.get_mode_status()
        # auto mode
        if mode == AUTO_MODE:
            # image processing
            if plc_main.send_start_autorun():
                print('Image processing start.')
                # i = 0  # control

                # current_time = time()
                # while True:
                #     if i > 10:
                #         break
                #     if plc_main.reset():
                #         break
                #     image = camera.capture()
                #     hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
                #     contour_mask = cv.inRange(
                #         hsv_image, hsv_color_bottom, hsv_color_top)
                #     # get welding puddle contour
                #     contour_point = get_puddle_contour(contour_mask)
                #     line_mask = cv.inRange(
                #         hsv_image, line_color_bottom, line_color_top)
                #     line_coef, line_intercept = get_middle_line_parameters(
                #         line_mask)

                #     pointA = (
                #         contour_point[0],
                #         contour_point[0] * line_coef + line_intercept)
                #     pointB = (
                #         (contour_point[1] - line_intercept)/line_coef,
                #         contour_point[1])

                #     ab_distance = ((pointA[0] - pointB[0]) ** 2 +
                #                    (pointA[1] - pointB[1]) ** 2) ** 0.5

                #     puddle_width = ab_distance * \
                #         line_coef / (line_coef ** 2 + 1)

                #     print('width:', puddle_width,
                #           ', measure_time:', time() - current_time)

                #     current_time = time()
                #     i += 1

            draw_message_window('AUTO MODE', bgcolor=BLACK)

        # menual mode
        elif mode == MENUAL_MODE:
            try:
                if plc_main.setting_value():
                    print('Setting Value')
                    if plc_main.is_setting_value(SET_GUN_SPEED):
                        set_val(TORCH_SPEED_VALUE)
                        print(torch_speed_value_mm_per_min)
                    elif plc_main.is_setting_value(SET_SOLDER_SPEED):
                        set_val(SOLDER_SPEED_VALUE)
                        print(solder_speed_value_mm_per_min)
                    else:
                        pass

                if plc_main.send_start_autorun():
                    print('start recording ...')
                    time_now = datetime.now()

                    camera.start_recording(
                        './record' + get_time_now() + '.h264')
                    camera.start_preview()
                    camera.wait_recording(60)
                    camera.stop_recording()
                    camera.stop_preview()
                    print('recorded success.')

            except Exception as e:
                log.write(get_time_now() + e)
                print(e)

            draw_menual_window()

        elif mode == 14234423:  # reset
            draw_message_window('RESETING...', bgcolor=BLACK)

    # connection error/failed
    else:
        if (time() - connect_check_record_time) // 5:
            connect_check_record_time = time()
            log.write(get_time_now() + 'PLC connection error.')
            print('PLC connection error, please check PLC and ethernet cable.')

        draw_message_window('Connection Error')

    # plc send shutdown command
    if plc_main.send_shutdown():
        log.write(get_time_now() + 'System shutdown.')
        print('system shutdown...')

        os.system('sudo shutdown now')

    sleep(0.1)


close()
