#! /usr/bin/env python3

# --- import constants (for convenience) --- #
# from constant import GUN_VOLTAGE, GUN_AMP
from constant import TORCH_SPEED_VALUE, SOLDER_SPEED_VALUE
from constant import MENUAL_MODE, AUTO_MODE
from constant import SET_GUN_SPEED, SET_SOLDER_SPEED
from constant import MAX_TORCH_SPEED_MM_PER_MIN, MAX_SOLDER_SPEED_MM_PER_MIN

# --- import PLC for commutation with PLC --- #
from modbus import PLC

import pygame as pg
from time import time
import os

# --- logging setting --- #
import logging
logging.basicConfig(filename='worklog.log',
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    level=logging.DEBUG)


# --- initialize keyboard --- #
try:
    import kb
    kb.init()
    logging.info('Keyboard initialize success')
except Exception:
    logging.error('Keyboard error', exc_info=True)


# --- colors --- #
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# ---------------------------------- #
# --- functions to render screen --- #
# ---------------------------------- #
def draw_title(text: str, color=WHITE, y=260):
    text = title_font.render(text, True, color)

    width = text.get_width()
    x = (W - width)//2
    WIN.blit(text, (x, y))


def draw_text(text: str, position: int, line: bool = 0, color=YELLOW):
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
    draw_title('MANUAL MODE', y=180)
    color = RED if torch_speed_value_mm_per_min > 2000 else WHITE

    draw_text(str(torch_speed_value_mm_per_min), 1, color=color)
    draw_text('mm/min', 1, 1)
    draw_text(str(solder_speed_value_mm_per_min), 2)
    draw_text('mm/min', 2, 1)
    draw_text(f'{str(v_value)}/{str(a_value)}', 3)
    draw_text('V/A', 3, 1)
    pg.display.update()


def draw_message_window(msg: str, color: list = WHITE, bgcolor: list = RED):
    WIN.fill(bgcolor)
    draw_title(msg, color)
    pg.display.update()


def draw_setting_value_window(id: int, value: str):
    title_font_color = WHITE
    WIN.fill(BLACK)
    if id == TORCH_SPEED_VALUE:
        if value != '' and int(value) > 2000:
            title_font_color = RED
        draw_title('SETTING TORCH', y=40)
    elif id == SOLDER_SPEED_VALUE:
        draw_title('SETTING SOLDER', y=40)
    draw_title('SPEED VALUE', y=90)
    val = title_font.render(value, True, title_font_color)
    width = val.get_width()
    x = W//2 - width//2
    WIN.blit(val, (x, 180))
    pg.display.update()
# ---------------------------------- #
# ---------------------------------- #
# ---------------------------------- #


# --- exit program --- #
def close():
    try:
        logging.info('Exit Program.')
        pg.quit()
        kb.close()
        plc_main.disconnect()
    finally:
        exit()


# --- setting value function --- #
def set_value(id: int):
    temp = ''

    # --- avoid keyboard input repeatly --- #
    kb_is_locked = False

    # --- check if value is flaot --- #
    value_is_float = False

    entering_value = True
    while entering_value:

        # --------------------------------------------- #
        # --- event for keyboard on welding machine --- #
        # --------------------------------------------- #
        key = kb.scan()

        # --- delete last number or point --- #
        if key == '#':
            if temp[-1] == '.':
                value_is_float = False
            temp = temp[:-1]
            if temp == '0':
                temp = ''

        # --- input point --- #
        if key == '*':
            if id == SOLDER_SPEED_VALUE:
                if not value_is_float:
                    if temp == '':
                        temp = '0'
                    temp += '.'
                    value_is_float = True

        # --- input number --- #
        if key not in ('#', '*', -1):
            if not kb_is_locked:
                temp += key
                if id == TORCH_SPEED_VALUE:
                    if int(temp) > MAX_TORCH_SPEED_MM_PER_MIN:
                        temp = str(MAX_TORCH_SPEED_MM_PER_MIN)
                elif id == SOLDER_SPEED_VALUE:
                    if int(temp) > MAX_SOLDER_SPEED_MM_PER_MIN:
                        temp = str(MAX_SOLDER_SPEED_MM_PER_MIN)

                kb_is_locked = True

        # --- input nothing --- #
        if key == -1:
            kb_is_locked = False

        # --------------------------------------------- #
        # --------------------------------------------- #
        # --------------------------------------------- #

        # ----------------------------------- #
        # --- event for computer keyboard --- #
        # ----------------------------------- #
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:

                # --- delete last number or point --- #
                if event.key == pg.K_BACKSPACE:
                    if temp:
                        if temp[-1] == '.':
                            value_is_float = False
                        temp = temp[:-1]
                        if temp == '0':
                            temp = ''

                # --- input point --- #
                elif event.key == pg.K_PERIOD:
                    if id == SOLDER_SPEED_VALUE:
                        if not value_is_float:
                            if temp == '':
                                temp = '0'
                            temp += '.'
                            value_is_float = True

                elif event.key in (pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4,
                                   pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9,
                                   pg.K_KP0, pg.K_KP1,
                                   pg.K_KP2, pg.K_KP3,
                                   pg.K_KP4, pg.K_KP5,
                                   pg.K_KP6, pg.K_KP7,
                                   pg.K_KP8, pg.K_KP9):
                    if event.key == pg.K_0 or event.key == pg.K_KP0:
                        temp += '0'
                    if event.key == pg.K_1 or event.key == pg.K_KP1:
                        temp += '1'
                    if event.key == pg.K_2 or event.key == pg.K_KP2:
                        temp += '2'
                    if event.key == pg.K_3 or event.key == pg.K_KP3:
                        temp += '3'
                    if event.key == pg.K_4 or event.key == pg.K_KP4:
                        temp += '4'
                    if event.key == pg.K_5 or event.key == pg.K_KP5:
                        temp += '5'
                    if event.key == pg.K_6 or event.key == pg.K_KP6:
                        temp += '6'
                    if event.key == pg.K_7 or event.key == pg.K_KP7:
                        temp += '7'
                    if event.key == pg.K_8 or event.key == pg.K_KP8:
                        temp += '8'
                    if event.key == pg.K_9 or event.key == pg.K_KP9:
                        temp += '9'

                    if id == TORCH_SPEED_VALUE:
                        if int(temp) > MAX_TORCH_SPEED_MM_PER_MIN:
                            temp = str(MAX_TORCH_SPEED_MM_PER_MIN)
                    elif id == SOLDER_SPEED_VALUE:
                        if int(temp) > MAX_SOLDER_SPEED_MM_PER_MIN:
                            temp = str(MAX_SOLDER_SPEED_MM_PER_MIN)
        # ----------------------------------- #
        # ----------------------------------- #
        # ----------------------------------- #

        # --- write value to plc and end function --- #
        if plc_main.setting_value_end():
            if temp == '':
                return

            if id == TORCH_SPEED_VALUE:
                temp = int(temp)
                global torch_speed_value_mm_per_min
                torch_speed_value_mm_per_min = temp
                plc_main.write_value(id, temp)

            if id == SOLDER_SPEED_VALUE:
                temp = float(temp)
                global solder_speed_value_mm_per_min
                solder_speed_value_mm_per_min = temp
                plc_main.write_value(id, temp)

            return

        draw_setting_value_window(id, temp)
        pg.display.update()
        pg.time.delay(100)


# --- changeable values --- #
torch_speed_value_mm_per_min = 200
solder_speed_value_mm_per_min = 350
# values will read from PLC
gun_height_value = 0
v_value, a_value = 0, 0

# --- initialize interface(pygame) --- #
pg.init()
pg.font.init()

# --- initialize font(pygame) --- #
title_font = pg.font.SysFont('Noto Sans CJK', 80)
regular_font = pg.font.SysFont('Noto Sans CJK', 40)

W, H = 720, 560
WIN = pg.display.set_mode((W, H))
# WIN = pg.display.set_mode((W, H), pg.FULLSCREEN)

# --- initialize modbus connect --- #
plc_main = PLC()
if plc_main.is_connect():
    logging.info('PLC connect success')
    plc_main.write_value(TORCH_SPEED_VALUE, torch_speed_value_mm_per_min)
    plc_main.write_value(SOLDER_SPEED_VALUE, solder_speed_value_mm_per_min)
else:
    logging.error('PLC connection error, please check PLC and ethernet cable.')

connect_check_record_time = time()
# --- main structure --- #
running = True
while running:

    # --- quit scrpit(just for keyboard) --- #
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                running = False
        elif event.type == pg.QUIT:
            running = False

    if plc_main.is_connect():
        mode = plc_main.get_mode_status()
        # auto mode
        if mode == AUTO_MODE:
            draw_message_window('AUTO MODE', bgcolor=BLACK)

        # menual mode
        elif mode == MENUAL_MODE:
            try:
                if plc_main.setting_value():
                    print('Setting Value')
                    if plc_main.is_setting_value(SET_GUN_SPEED):
                        set_value(TORCH_SPEED_VALUE)
                        print(torch_speed_value_mm_per_min)
                    if plc_main.is_setting_value(SET_SOLDER_SPEED):
                        set_value(SOLDER_SPEED_VALUE)
                        print(solder_speed_value_mm_per_min)

                if plc_main.send_start_autorun():
                    pass

            except Exception as e:
                logging.error(e)
                print(e)

            draw_menual_window()

        elif mode == 14234423:  # reset
            draw_message_window('RESETING...', bgcolor=BLACK)

        # --- plc send shutdown command --- #
        if plc_main.send_shutdown():
            logging.info('System shutdown.')
            print('system shutdown...')

            os.system('sudo shutdown now')

    # ---  connection error/failed --- #
    else:
        if (time() - connect_check_record_time) // 5:
            connect_check_record_time = time()
            print('PLC connection error, please check PLC and ethernet cable.')

        draw_message_window('Connection Error')

    pg.time.delay(100)


close()
