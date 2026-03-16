import pygame
from config import *

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load('img/coin.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (24,24))
        except Exception:
            self.image = pygame.Surface((24,24), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255,215,0), (12,12), 10)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)
