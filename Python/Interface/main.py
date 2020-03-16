import pygame as pg

from modbus import *

# color map
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255 ,255, 0)

# control value
gun_speed = 0
solder_speed = 0
gun_height = 0
v, a = 0, 0

pg.init()
pg.font.init()

font = pg.font.SysFont('Noto Sans CJK', 40)
W, H = 370, 272
WIN = pg.display.set_mode((W, H), pg.FULLSCREEN)

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE): run = False

        # key event listener
        if event.type == pg.KEYDOWN and event.key == pg.K_q: pass
        if event.type == pg.KEYDOWN and event.key == pg.K_w: pass
        if event.type == pg.KEYDOWN and event.key == pg.K_e: pass
        if event.type == pg.KEYDOWN and event.key == pg.K_r: pass
        if event.type == pg.KEYDOWN and event.key == pg.K_t: pass

    WIN.fill(BLACK)

    gun_speed_text = font.render(str(gun_speed), True, YELLOW)
    width = gun_speed_text.get_width()
    x = W//8 - width//2
    y = 220
    WIN.blit(gun_speed_text, (x, y))

    solder_speed_text = font.render(str(solder_speed), True, YELLOW)
    width = solder_speed_text.get_width()
    x = W//8 * 3 - width//2
    WIN.blit(solder_speed_text, (x, y))

    gun_height_text = font.render(str(gun_height), True, YELLOW)
    width = gun_height_text.get_width()
    x = W//8 * 5 - width//2
    WIN.blit(gun_height_text, (x, y))

    v_a_text = font.render(str(v) + '/' + str(a), True, YELLOW)
    width = v_a_text.get_width()
    x = W//8 * 7 - width//2
    WIN.blit(v_a_text, (x, y))

    pg.display.update()

pg.quit()