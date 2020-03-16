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
gun_speed = 0
solder_speed = 0
gun_height = 0
v, a = 0, 0
#########################

####### iniaialize interface(pygame) #########
pg.init()
pg.font.init()

font = pg.font.SysFont('Noto Sans CJK', 40)
W, H = 370, 272
WIN = pg.display.set_mode((W, H))
# WIN = pg.display.set_mode((W, H), pg.FULLSCREEN)

####### functions #######
def print_text(text:str, position:int, color = YELLOW):
    if type(text) != str: 
        print('Text type must be string.')
        return

    text = font.render(text, True, color)
    width = text.get_width()
    x = W//8 * (position*2 - 1) - width//2
    WIN.blit(text, (x, 220))

#########　main loop #########
run = True
while run:
    for event in pg.event.get():
        # quit
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE): run = False

        # value_key event listener
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q: gun_speed += 1
            if event.key == pg.K_a: gun_speed -= 1
            if event.key == pg.K_w: solder_speed += 1
            if event.key == pg.K_s: solder_speed -= 1
            if event.key == pg.K_e: gun_height += 1
            if event.key == pg.K_d: gun_height -= 1
            if event.key == pg.K_r: v += 1
            if event.key == pg.K_f: v -= 1
            if event.key == pg.K_t: a += 1
            if event.key == pg.K_g: a -= 1

    WIN.fill(BLACK)

    print_text(str(gun_speed), 1)
    print_text(str(solder_speed), 2)
    print_text(str(gun_height), 3)
    print_text(f'{str(v)}/{str(a)}', 4)

    pg.display.update()

pg.quit()