import pygame as pg
import sys

pg.init()
clock = pg.time.Clock()
WIDTH, HEIGHT = 600, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))


while True:
    clock.tick(60)
    # Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # ----

    screen.fill('blue')
