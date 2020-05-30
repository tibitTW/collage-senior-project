import pygame as pg


def pygame_init():
    pg.init()

    pg.font.init()

    font = pg.font.SysFont('Noto Sans CJK', 40)
    font_small = pg.font.SysFont('Noto Sans CJK', 24)

    W, H = 370, 272
    WIN = pg.display.set_mode((W, H))


def draw_title(text: str, color=WHITE, y=120):
    text = font.render(text, True, color)

    width = text.get_width()
    x = (W - width)//2
    WIN.blit(text, (x, y))
