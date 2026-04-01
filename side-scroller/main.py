import pygame as pg
import sys

pg.init()
pg.font.init()
font = pg.font.SysFont('monospace', 20)
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()

SPEED = 5
GRAVITY = 0.5
JUMP_FORCE = -10


class Player:
    def __init__(self, x, y):
        self.on_ground = False
        self.pos = pg.Vector2(x, y)
        self.vel = pg.Vector2(0, 0)
        self.rect = pg.Rect(x, y, 40, 60)

    def handle_input(self, events):
        # ---- Continuous inputs ----
        self.vel.x = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.vel.x -= SPEED
        if keys[pg.K_d]:
            self.vel.x += SPEED

        # ---- Discrete inputs ----
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and self.on_ground:
                    self.vel.y = JUMP_FORCE
                    self.on_ground = False

    def update(self):
        self.vel.y += GRAVITY
        self.pos += self.vel
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

        self._resolve_collisions(platforms)

    def _resolve_collisions(self, platforms):
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vel.y > 0:
                    self.rect.bottom = plat.top
                    self.pos.y = self.rect.y
                    self.vel.y = 0
                    self.on_ground = True

    def draw(self, screen):
        pg.draw.rect(screen, "red", self.rect, 40)


platforms = [
    pg.Rect(0, 650, 1280, 70),
    pg.Rect(300, 500, 200, 20),
    pg.Rect(700, 400, 200, 20),
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
    text = font.render(f'on_ground: {player.on_ground}', False, "red")
    screen.blit(text, (1, 1))
    player.draw(screen)
    for plat in platforms:
        pg.draw.rect(screen, "white", plat)

    pg.display.flip()
