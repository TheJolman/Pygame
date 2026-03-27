import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test")
clock = pygame.time.Clock()
FPS = 60


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(FPS)

        screen.fill("aqua")

        pygame.display.flip()


if __name__ == "__main__":
    main()
