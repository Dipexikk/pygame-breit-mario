import pygame
import os
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, controls='both'):
        super().__init__()

        image_loaded = False

        for name in ["Cat_Mario", "cat", "player", "kocka"]:
            for ext in ["png", "jpg", "jpeg", "webp"]:
                try:
                    image_path = os.path.join("img", f"{name}.{ext}")
                    self.image = pygame.image.load(image_path).convert_alpha()
                    self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
                    print(f"Načten obrázek hráče: {image_path}")
                    image_loaded = True

                    break
                
                except (pygame.error, FileNotFoundError):
                    continue
        
        if not image_loaded:

            self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
            self.image.fill(PLAYER_COLOR)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocity_x = 0
        self.velocity_y = 0

        self.on_ground = False

        self.controls = controls

        self.max_jumps = 2
        self.jumps_left = self.max_jumps
        self.jump_held = False
    
    def update(self, platforms):
        keys = pygame.key.get_pressed()
        self.velocity_x = 0

        use_arrows = self.controls in ('arrows', 'both')
        use_wasd = self.controls in ('wasd', 'both')

        if use_arrows and keys[pygame.K_RIGHT]:
            self.velocity_x = PLAYER_SPEED
        if use_arrows and keys[pygame.K_LEFT]:
            self.velocity_x = -PLAYER_SPEED

        if use_wasd and keys[pygame.K_d]:
            self.velocity_x = PLAYER_SPEED
        if use_wasd and keys[pygame.K_a]:
            self.velocity_x = -PLAYER_SPEED

        jump_pressed = (use_arrows and keys[pygame.K_UP]) or (use_wasd and keys[pygame.K_w])
        if jump_pressed and not self.jump_held and self.jumps_left > 0:
            self.velocity_y = -JUMP_POWER
            self.jumps_left -= 1
            self.on_ground = False
            self.jump_held = True
        if not jump_pressed:
            self.jump_held = False


        self.velocity_y += GRAVITY
        if self.velocity_y > 15:
            self.velocity_y = 15
        

        self.rect.x += self.velocity_x
        if self.rect.left < 0:
            self.rect.left = 0


        self.rect.y += self.velocity_y

        self.on_ground = False

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.jumps_left = self.max_jumps
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0 

        if self.rect.top > SCREEN_HEIGHT:
            return True
        return False

    def bounce(self, power=None):
        p = power if power is not None else (JUMP_POWER / 1.5)
        self.velocity_y = -p
        self.jumps_left = self.max_jumps

    def draw(self, screen):
        screen.blit(self.image, self.rect)


