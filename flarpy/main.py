import pygame as pg
import sys
import random

pg.init()

WIDTH, HEIGHT = 400, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Flappy Bird")
clock = pg.time.Clock()
FPS = 60

# Physics
GRAVITY = 0.5
JUMP_VEL = -9
BIRD_X = 80

# Pipes
PIPE_WIDTH = 60
PIPE_GAP = 160
PIPE_SPEED = 3
PIPE_INTERVAL = 1500  # ms between spawns

# Colors
SKY = (113, 197, 207)
GROUND = (222, 216, 149)
GREEN = (78, 154, 6)
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)

GROUND_Y = HEIGHT - 80


class Bird:
    RADIUS = 18

    def __init__(self):
        self.y = HEIGHT // 2
        self.vel = 0

    def jump(self):
        self.vel = JUMP_VEL

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel
        self.y = max(self.RADIUS, self.y)  # don't go above screen

    def draw(self, surf):
        cx, cy = BIRD_X, int(self.y)
        # body
        pg.draw.circle(surf, YELLOW, (cx, cy), self.RADIUS)
        pg.draw.circle(surf, BLACK, (cx, cy), self.RADIUS, 2)
        # eye
        pg.draw.circle(surf, BLACK, (cx + 8, cy - 5), 4)
        pg.draw.circle(surf, WHITE, (cx + 9, cy - 6), 2)
        # beak
        pg.draw.polygon(
            surf,
            (255, 140, 0),
            [
                (cx + 14, cy + 2),
                (cx + 22, cy),
                (cx + 14, cy - 2),
            ],
        )

    def get_rect(self):
        r = self.RADIUS - 4  # slightly forgiving hitbox
        return pg.Rect(BIRD_X - r, int(self.y) - r, r * 2, r * 2)


class Pipe:
    def __init__(self):
        gap_center = random.randint(150, GROUND_Y - 150)
        self.top_rect = pg.Rect(WIDTH, 0, PIPE_WIDTH, gap_center - PIPE_GAP // 2)
        self.bottom_rect = pg.Rect(
            WIDTH, gap_center + PIPE_GAP // 2, PIPE_WIDTH, HEIGHT
        )
        self.passed = False

    def update(self):
        self.top_rect.x -= PIPE_SPEED
        self.bottom_rect.x -= PIPE_SPEED

    def draw(self, surf):
        for rect in (self.top_rect, self.bottom_rect):
            pg.draw.rect(surf, GREEN, rect)
            pg.draw.rect(surf, BLACK, rect, 2)
            # cap
            cap = pg.Rect(
                rect.x - 4,
                rect.bottom - 20 if rect.top == 0 else rect.top,
                PIPE_WIDTH + 8,
                20,
            )
            pg.draw.rect(surf, GREEN, cap)
            pg.draw.rect(surf, BLACK, cap, 2)

    def off_screen(self):
        return self.top_rect.right < 0

    def collides(self, bird_rect):
        return bird_rect.colliderect(self.top_rect) or bird_rect.colliderect(
            self.bottom_rect
        )


def main():
    bird = Bird()
    pipes = []
    score = 0
    state = "waiting"
    last_pipe = 0
    font = pg.font.SysFont(None, 48)
    small_font = pg.font.SysFont(None, 28)

    while True:
        clock.tick(FPS)

        # --- Events ---
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_SPACE, pg.K_UP):
                    if state == "waiting":
                        state = "playing"
                        bird.jump()
                    elif state == "playing":
                        bird.jump()
                    elif state == "dead":
                        # restart
                        bird = Bird()
                        pipes = []
                        score = 0
                        state = "waiting"
                        last_pipe = 0

        # --- Update ---
        if state == "playing":
            bird.update()

            now = pg.time.get_ticks()
            if now - last_pipe > PIPE_INTERVAL:
                pipes.append(Pipe())
                last_pipe = now

            for pipe in pipes:
                pipe.update()
                if not pipe.passed and pipe.top_rect.right < BIRD_X:
                    pipe.passed = True
                    score += 1

            pipes = [p for p in pipes if not p.off_screen()]

            bird_rect = bird.get_rect()
            hit_ground = bird.y + bird.RADIUS >= GROUND_Y
            hit_pipe = any(p.collides(bird_rect) for p in pipes)

            if hit_ground or hit_pipe:
                state = "dead"

        # --- Draw ---
        screen.fill(SKY)

        for pipe in pipes:
            pipe.draw(screen)

        # ground
        pg.draw.rect(screen, GROUND, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
        pg.draw.line(screen, BLACK, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)

        bird.draw(screen)

        # HUD
        score_surf = font.render(str(score), True, WHITE)
        screen.blit(score_surf, (WIDTH // 2 - score_surf.get_width() // 2, 30))

        if state == "waiting":
            msg = small_font.render("Press SPACE to start", True, WHITE)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 + 40))

        if state == "dead":
            msg1 = font.render("Game Over", True, RED)
            msg2 = small_font.render("Press SPACE to restart", True, WHITE)
            screen.blit(msg1, (WIDTH // 2 - msg1.get_width() // 2, HEIGHT // 2 - 30))
            screen.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, HEIGHT // 2 + 20))

        pg.display.flip()


if __name__ == "__main__":
    main()
