import pygame
from config import *

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        pygame.key.set_repeat(300, 50)

        self.keypress_interval = 50  # ms
        self.last_keypress_time = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                print(f"KEYDOWN: ID = {event.key}, název = {pygame.key.name(event.key)}")

                if event.key == pygame.K_ESCAPE:
                    self.running = False

            if event.type == pygame.KEYUP:
                print(f"KEYUP: ID = {event.key}, název = {pygame.key.name(event.key)}")

        now = pygame.time.get_ticks()
        if now - self.last_keypress_time >= self.keypress_interval:
            self.last_keypress_time = now

            keys = pygame.key.get_pressed()
            for key_id, pressed in enumerate(keys):
                if pressed:
                    print(f"DRŽÍŠ: ID = {key_id}, název = {pygame.key.name(key_id)}")

    def update(self):
        pass

    def draw(self):
        self.screen.fill(SKY_BLUE)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
