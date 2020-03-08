import pygame as pg

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

# initialize
pg.init()
pg.font.init()

font = pg.font.SysFont('Noto Sans CJK', 40)
W, H = 370, 272
WIN = pg.display.set_mode((W, H))

e = W//8

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE): run = False

        if event.type == pg.KEYDOWN and event.key == pg.K_q: gun_speed += 1
        if event.type == pg.KEYDOWN and event.key == pg.K_a: gun_speed -= 1
        if event.type == pg.KEYDOWN and event.key == pg.K_w: solder_speed += 1
        if event.type == pg.KEYDOWN and event.key == pg.K_s: solder_speed -= 1
        if event.type == pg.KEYDOWN and event.key == pg.K_e: gun_height += 1
        if event.type == pg.KEYDOWN and event.key == pg.K_d: gun_height -= 1
        if event.type == pg.KEYDOWN and event.key == pg.K_r: v += 1
        if event.type == pg.KEYDOWN and event.key == pg.K_f: v -= 1
        if event.type == pg.KEYDOWN and event.key == pg.K_t: a += 1
        if event.type == pg.KEYDOWN and event.key == pg.K_f: a -= 1

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