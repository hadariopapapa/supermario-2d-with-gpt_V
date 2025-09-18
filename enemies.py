import pygame
from settings import *
import collision_manager as collisions
from config import ENEMY_SPEED, ENEMY_SIZE, FLYING_ENEMY_SPEED, FLYING_VERTICAL_RANGE
from config import BOSS_HP, BOSS_SPEED, BOSS_TURN_DELAY, BOSS_SIZE

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, *ENEMY_SIZE)
        self.speed = ENEMY_SPEED
        self.dir = -1
        self.alive = True

    def update(self, boxes, ground_length):
        if not self.alive: return
        collisions.check_enemy_box(self, boxes, HEIGHT - 50)

    def draw(self, screen, camera):
        if self.alive:
            pygame.draw.rect(screen, RED, camera.apply(self.rect))


class Boss(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, *BOSS_SIZE)
        self.hp = BOSS_HP
        self.cooldown = 0
        self.speed = BOSS_SPEED
        self.dir = -1
        self.turn_cooldown = 0
        self.turn_delay = BOSS_TURN_DELAY

    def update(self, boxes, ground_length, player=None):
        if not self.alive: return

        if player and self.turn_cooldown == 0:
            if player.rect.centerx < self.rect.centerx and self.dir != -1:
                self.dir = -1
                self.turn_cooldown = self.turn_delay
            elif player.rect.centerx > self.rect.centerx and self.dir != 1:
                self.dir = 1
                self.turn_cooldown = self.turn_delay

        self.rect.x += self.dir * self.speed

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > ground_length: self.rect.right = ground_length

        if self.cooldown > 0: self.cooldown -= 1
        if self.turn_cooldown > 0: self.turn_cooldown -= 1

    def draw(self, screen, camera, font):
        if self.alive:
            pygame.draw.rect(screen, DARK_RED, camera.apply(self.rect))
            hp_text = font.render(f"Boss HP: {self.hp}", True, RED)
            screen.blit(hp_text, (self.rect.x - camera.x, self.rect.y - 25))


class FlyingEnemy:
    def __init__(self, x, y, vertical_range=FLYING_VERTICAL_RANGE):
        self.rect = pygame.Rect(x, y, *ENEMY_SIZE)
        self.speed = FLYING_ENEMY_SPEED
        self.dir = -1
        self.alive = True
        self.base_y = y
        self.vertical_range = vertical_range
        self.y_dir = 1

    def update(self, boxes, ground_length):
        if not self.alive: return
        self.rect.x += self.dir * self.speed
        if self.rect.left <= 0 or self.rect.right >= ground_length:
            self.dir *= -1
        self.rect.y += self.y_dir * 2
        if self.rect.y > self.base_y + self.vertical_range:
            self.y_dir = -1
        elif self.rect.y < self.base_y - self.vertical_range:
            self.y_dir = 1

    def draw(self, screen, camera):
        if self.alive:
            pygame.draw.rect(screen, BLUE, camera.apply(self.rect))