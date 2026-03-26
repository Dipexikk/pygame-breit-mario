from os import name
import pygame
from config import *
from game.player import Player
from game.platform import Platform
from game.coin import Coin
from game.enemy import Enemy
from game.menu import Menu
from game.end_screen import EndScreen

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.world_shift = 0
        self.level_width = 4800  # longer level
        
        self.menu = Menu(screen)
        self.end = EndScreen(screen)

        self.in_menu = True
        self.in_game = False
        self.in_end = False

        self.collected = 0
        self.total_coins = 0
        self.won = False
        self.last_score = None

    def start_game(self, control_choice):
        # clear groups
        self.all_sprites.empty()
        self.platforms.empty()
        self.coins.empty()
        self.enemies.empty()

        # player
        self.player = Player(100, 100, controls=control_choice)
        self.all_sprites.add(self.player)

        # reset world
        self.world_shift = 0
        self.level_width = 6400  # make it even longer (harder)

        # create level (platforms, coins, enemies)
        self.create_level(harder=True)

        # score / win state
        self.collected = 0
        self.total_coins = len(self.coins)
        self.won = False

        self.in_menu = False
        self.in_game = True
        self.in_end = False

    def create_level(self, harder=False):
        # ground
        ground = Platform(0, SCREEN_HEIGHT - 40, self.level_width, 40)
        self.platforms.add(ground)
        self.all_sprites.add(ground)

        # create many platforms along the level
        x = 200
        gap = 300 if not harder else 220
        import random
        while x < self.level_width - 200:
            h = random.randint(220, 460)
            w = random.randint(100, 250)
            self.add_platform(x, h, w, 20)
            # randomly place coins on platform
            if random.random() < (0.6 if not harder else 0.8):
                self.add_coin(x + w//2, h - 40)
            # more enemies: on platform or ground
            if random.random() < (0.25 if not harder else 0.45):
                left = max(0, x-100)
                right = min(self.level_width, x+200)
                # place enemy either on top of platform or on ground near it
                if random.random() < 0.5:
                    ex = x + w//2
                    ey = h - 40  # enemy stands on platform (platform top is h)
                else:
                    ex = x
                    ey = SCREEN_HEIGHT - 80
                speed = random.randint(2,5) if harder else random.randint(1,3)
                self.add_enemy(ex, ey, left, right, speed)

            x += gap + random.randint(-80,80)

    def add_platform(self, x, y, w, h):
        p = Platform(x, y, w, h)
        self.platforms.add(p)
        self.all_sprites.add(p)

    def add_coin(self, x, y):
        c = Coin(x, y)
        self.coins.add(c)
        self.all_sprites.add(c)

    def add_enemy(self, x, y, left_limit, right_limit, speed=2):
        e = Enemy(x, y, left_limit, right_limit, speed=speed)
        self.enemies.add(e)
        self.all_sprites.add(e)

    def handle_events(self):
        for event in pygame.event.get():
            if self.in_menu:
                res = self.menu.handle_event(event)
                if res == 'start':
                    self.start_game(self.menu.control_choice)
                if event.type == pygame.QUIT:
                    self.running = False
                continue

            if self.in_game:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        return
                    if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                        evt_key = pygame.key.name(event.key)
                        print(f"{pygame.event.event_name(event.type)}: {evt_key}")
                return

            if self.in_end:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.in_menu = True
                    self.in_end = False
                    self.menu.last_score = self.last_score
                if event.type == pygame.QUIT:
                    self.running = False
                return

    def update(self):
        if self.in_menu or self.in_end:
            return

        # update sprites
        self.enemies.update()

        # update player and check fall
        game_over = self.player.update(self.platforms)
        if game_over:
            self.finish(False)
            return

        # coin collection
        coins_hit = pygame.sprite.spritecollide(self.player, self.coins, dokill=True)
        if coins_hit:
            self.collected += len(coins_hit)
            print(f"Coins collected: {self.collected}/{self.total_coins}")
            if self.collected >= self.total_coins:
                self.finish(True)
                return

        # enemy collisions: if player hits enemy from top -> kill enemy and bounce, else lose
        enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, dokill=False)
        for enemy in enemy_hits:
            if self.player.velocity_y > 0 and self.player.rect.bottom - enemy.rect.top < 20:
                # stomp
                enemy.kill()
                self.player.bounce()
            else:
                # player hit from side
                self.finish(False)
                return

        # scrolling: shift world when player reaches center-right of the screen
        if self.player.rect.centerx > SCREEN_WIDTH * 0.6 and self.world_shift > -(self.level_width - SCREEN_WIDTH):
            shift = self.player.rect.centerx - SCREEN_WIDTH * 0.6
            self.player.rect.x -= shift
            self.world_shift -= shift
            self.shift_world(-shift)

        # when player moves left near left edge, don't shift past 0
        if self.player.rect.centerx < SCREEN_WIDTH * 0.3 and self.world_shift < 0:
            shift = SCREEN_WIDTH * 0.3 - self.player.rect.centerx
            self.player.rect.x += shift
            self.world_shift += shift
            self.shift_world(shift)

    def finish(self, won):
        self.in_game = False
        self.in_end = True
        self.won = won
        self.last_score = self.collected
        self.end.result = 'YOU WIN!' if won else 'YOU LOST'
        self.end.score = self.collected

    def shift_world(self, shift_x):
        # move all world objects (platforms, coins, enemies) by shift_x
        for sprite in self.platforms:
            sprite.rect.x += shift_x
        for coin in self.coins:
            coin.rect.x += shift_x
        for enemy in self.enemies:
            enemy.rect.x += shift_x

    def draw(self):
        if self.in_menu:
            self.menu.draw()
            return
        if self.in_end:
            self.end.show()
            return

        # background (simple repeated sky + ground)
        self.screen.fill(SKY_BLUE)

        # draw all sprites
        for sprite in self.all_sprites:
            sprite.draw(self.screen)

        # HUD
        font = pygame.font.SysFont(None, 30)
        text = font.render(f"Coins: {self.collected}/{self.total_coins}", True, (0,0,0))
        self.screen.blit(text, (10,10))

        pygame.display.flip()



    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
