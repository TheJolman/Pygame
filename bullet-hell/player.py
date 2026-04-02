import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pg.Surface((40, 40))
        self.image.fill('red')
        self.rect = self.image.get_rect(center=pos)

    def draw(self, surface):
        surface.blit(surface, self.image)
