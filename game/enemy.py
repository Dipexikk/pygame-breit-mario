import pygame
import os
from config import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, left_limit, right_limit, speed=2):
        super().__init__()
        self.frames = []
        possible = ['enemy.png', 'enemy1.png', 'goomba.png', 'enemy_walk1.png', 'enemy_walk.png']
        for name in possible:
            path = os.path.join('img', name)
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (40, 40))
                self.frames.append(img)
            except Exception:
                continue

        if not self.frames:
            surf = pygame.Surface((40,40), pygame.SRCALPHA)
            surf.fill((0,100,0))
            self.frames = [surf]

        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 8 

        self.base_image = self.frames[self.frame_index]
        self.image = self.base_image

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.left_limit = left_limit
        self.right_limit = right_limit
        self.speed = speed
        self.direction = 1

        self.facing_left = False

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x < self.left_limit:
            self.rect.x = self.left_limit
            self.direction = 1
        if self.rect.x > self.right_limit:
            self.rect.x = self.right_limit
            self.direction = -1

        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.base_image = self.frames[self.frame_index]

        if self.direction < 0:
            self.image = pygame.transform.flip(self.base_image, True, False)
        else:
            self.image = self.base_image

    def draw(self, screen):
        screen.blit(self.image, self.rect)
