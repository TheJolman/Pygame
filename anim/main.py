import pygame as pg
import sys

pg.init()
screen = pg.display.set_mode((600, 600))
clock = pg.time.Clock()

anim_frames = [
    pg.image.load("./assets/frame1.png"),
    pg.image.load("./assets/frame2.png"),
]

for i in range(len(anim_frames)):
    anim_frames[i] = pg.transform.scale(anim_frames[i], (100, 100))


current_frame = 0
anim_timer = 0.0
anim_speed = 0.12  # seconds per frame

player_x = 100
player_y = 300
player_speed = 200

while True:
    dt = clock.tick(60) / 1000

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    keys = pg.key.get_pressed()
    moving = False

    if keys[pg.K_LEFT]:
        player_x -= player_speed * dt
        moving = True
    if keys[pg.K_RIGHT]:
        player_x += player_speed * dt
        moving = True

    if moving:
        anim_timer += dt
        if anim_timer >= anim_speed:
            anim_timer = 0.0
            current_frame = (current_frame + 1) % len(anim_frames)
    else:
        current_frame = 0  # idling

    screen.fill("blue")
    screen.blit(anim_frames[current_frame], (player_x, player_y))

    pg.display.flip()
