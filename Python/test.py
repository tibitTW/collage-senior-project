#!/usr/bin/env python3

import pygame as pg
from time import sleep

pg.init()

W, H = 800, 600
WIN = pg.display.set_mode((W, H))

a = 0
while a < 1000:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE): pg.quit()

    WIN.fill((0, 0, 0))
    pg.draw.rect(WIN, (255, 0, 255), (100, 100, 200, 200))

    pg.display.update()
    a += 1

pg.quit()