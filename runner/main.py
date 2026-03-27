import pygame as pg
import sys
import random
from enum import Enum
# from dataclasses import dataclass


pg.init()
clock = pg.time.Clock()
WIDTH, HEIGHT = 800, 800
screen = pg.display.set_mode((WIDTH, HEIGHT))

LANES = [275, 400, 525]
OBSTACLE_INTERVAL = 1000


class Player:
    MOVE_SPEED = 12

    def __init__(self):
        self.lane = 1
        self.x = LANES[self.lane]
        self.target_x = self.x
        self.y = 600
        self.rect = pg.Rect(self.x - 20, self.y - 30, 40, 60)

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.target_x = LANES[self.lane]

    def move_right(self):
        if self.lane < len(LANES) - 1:
            self.lane += 1
            self.target_x = LANES[self.lane]

    def draw(self, surface):
        pg.draw.rect(surface, "red", self.get_rect())

    def update(self):
        diff = self.target_x - self.x
        if abs(diff) < self.MOVE_SPEED:
            self.x = self.target_x
        else:
            self.x += self.MOVE_SPEED * (1 if diff > 0 else -1)

    def get_rect(self):
        return pg.Rect(self.x - 20, self.y - 30, 40, 60)


class Obstacle:
    MOVE_SPEED = 10

    def __init__(self):
        self.lane = random.randint(0, 2)
        self.x = LANES[self.lane]
        self.rect = pg.Rect(self.x - 40, 0, 80, 40)

    def update(self):
        self.rect.y += self.MOVE_SPEED

    def draw(self, surface):
        pg.draw.rect(surface, "green", self.rect)

    def is_off_screen(self):
        return self.rect.y > HEIGHT

    def collides(self, player_rect):
        return player_rect.colliderect(self.rect)


class State(Enum):
    PLAYING = 0
    DEAD = 1


class GameState:
    player: Player = Player()
    state: State = State.PLAYING
    obstacles: list = []
    last_obstacle: int = 0

    def reset(self):
        self.state = State.PLAYING
        self.obstacles = []
        self.last_obstacle = 0


def input_handler(key, gs):
    match gs.state:
        case State.PLAYING:
            match key:
                case pg.K_LEFT:
                    gs.player.move_left()
                case pg.K_RIGHT:
                    gs.player.move_right()

        case State.DEAD:
            match key:
                case pg.K_SPACE:
                    gs.reset()


def main():
    gs = GameState()
    last_obstacle = 0
    font = pg.font.SysFont(None, 48)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                input_handler(event.key, gs)

        clock.tick(60)
        screen.fill("aquamarine")
        map_rect = pg.Rect(WIDTH / 4, 0, WIDTH / 2, HEIGHT)
        pg.draw.rect(screen, "burlywood", map_rect)

        match gs.state:
            case State.PLAYING:
                gs.player.draw(screen)
                gs.player.update()

                now = pg.time.get_ticks()
                if now - last_obstacle > OBSTACLE_INTERVAL:
                    gs.obstacles.append(Obstacle())
                    last_obstacle = now
                for obstacle in gs.obstacles:
                    obstacle.draw(screen)
                    obstacle.update()
                obstacles = [
                    obstacle
                    for obstacle in gs.obstacles
                    if not obstacle.is_off_screen()
                ]

                timer = font.render(str(now / 1000), True, "white")
                screen.blit(timer, (WIDTH // 2 - timer.get_width() // 2, 30))

                player_rect = gs.player.get_rect()
                if any(o.collides(player_rect) for o in obstacles):
                    gs.state = State.DEAD

            case State.DEAD:
                message = font.render("YOU DIED", True, "white")
                screen.blit(
                    message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - 30)
                )

        pg.display.flip()


if __name__ == "__main__":
    main()
    pg.quit()
