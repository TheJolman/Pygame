import pygame as pg
import sys

pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()

SPEED = 5
GRAVITY = 2
JUMP_FORCE = 10


class Player:
    def __init__(self, x, y):
        self.pos = pg.Vector2(x, y)
        self.vel = pg.Vector2(0, 0)
        self.rect = pg.Rect(x, y, 40, 40)

    def handle_input(self, events):
        self.vel = pg.Vector2(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.vel.y -= JUMP_FORCE
        if keys[pg.K_a]:
            self.vel.x -= SPEED
        if keys[pg.K_d]:
            self.vel.x += SPEED

        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    self.vel.y = JUMP_FORCE

    def update(self):
        self.vel.y += GRAVITY
        self.pos += self.vel

    def _resolve_collisions(self, platforms):
        for plat in platforms:
            if self.rect.colliderect(plat):
                self.rect.bottom

    def draw(self, screen):
        pg.draw.circle(screen, "red", self.pos, 40)


platforms = [
    pg.Rect(0, 650, 1280, 70),
    # pg.Rect(300, 500, 200, 20),
    # pg.Rect(700, 400, 200, 20),
]

player = Player(screen.get_width() / 2, screen.get_height() / 2)

while True:
    clock.tick(60)
    player_velocity = pg.Vector2(0, 0)

    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit(0)

    player.handle_input(events)
    player.update()

    # ---- Draw ----
    screen.fill("purple")
    player.draw(screen)
    pg.display.flip()
