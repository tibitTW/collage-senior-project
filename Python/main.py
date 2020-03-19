import pygame as pg

from modbus import *

####### color map #######
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255 ,255, 0)
##### control value #####
gun_speed_value = 0
solder_speed_value = 0
gun_height_value = 0
v_value, a_value = 0, 0
#########################

####### iniaialize interface(pygame) #########
pg.init()
pg.font.init()

font = pg.font.SysFont('Noto Sans CJK', 40)
font_small = pg.font.SysFont('Noto Sans CJK', 24)

W, H = 370, 272
WIN = pg.display.set_mode((W, H))
# WIN = pg.display.set_mode((W, H), pg.FULLSCREEN)
########### initialize connect ###############
plc_main = plc()

####### functions #######
def print_text(text:str, position:int, line:bool = 0, color = YELLOW):
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

#########　main loop #########
run = True
while run:
    for event in pg.event.get():
        # quit
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE): run = False

        # value_key event listener
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q: gun_speed_value += 1
            if event.key == pg.K_w: solder_speed_value += 1
            if event.key == pg.K_e: gun_height_value += 1
            if event.key == pg.K_r: v_value += 1
            if event.key == pg.K_t: a_value += 1
            if event.key == pg.K_a: gun_speed_value -= 1
            if event.key == pg.K_s: solder_speed_value -= 1
            if event.key == pg.K_d: gun_height_value -= 1
            if event.key == pg.K_f: v_value -= 1
            if event.key == pg.K_g: a_value -= 1

    WIN.fill(BLACK)

    print_text(str(gun_speed_value), 1)
    print_text('mm/min', 1, 1)
    print_text(str(solder_speed_value), 2)
    print_text('mm/min', 2, 1)
    print_text(str(gun_height_value), 3)
    print_text('mm', 3, 1)
    print_text(f'{str(v_value)}/{str(a_value)}', 4)
    print_text('V/A', 4, 1)

    pg.display.update()
    pg.time.delay(100)

pg.quit()