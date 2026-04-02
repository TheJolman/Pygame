import pygame as pg
import sys

from player import Player

pg.init()
clock = pg.time.Clock()
WIDTH, HEIGHT = 600, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))

all_sprites = pg.sprite.Group()
all_sprites.add(Player((300, 100)))

while True:
    clock.tick(60)
    # Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    # ----

    screen.fill("blue")
    all_sprites.draw(screen)
