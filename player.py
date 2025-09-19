import pygame
from settings import *
from config import PLAYER_SPEED, PLAYER_JUMP_FORCE, PLAYER_MAX_HP, PLAYER_FIREBALL_LIMIT, COYOTE_TIME, JUMP_BUFFER_TIME
from config import FIREBALL_SPEED, FIREBALL_MAX_DIST

class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, HEIGHT - 50 - 50, 40, 50)

        # Physics
        self.y_vel = 0
        self.on_ground = False

        # Facing
        self.facing_right = True
        self.has_fire = False
        self.fireballs = []

        # Stats
        self.hp = PLAYER_MAX_HP
        self.hurt_cd = 0
        self.hit_flash_timer = 0

        # Jump leniency
        self.coyote_time = COYOTE_TIME
        self.coyote_timer = 0
        self.jump_buffer_time = JUMP_BUFFER_TIME
        self.jump_buffer_timer = 0

    def handle_input(self, keys):
        dx = 0
        if keys[pygame.K_LEFT]:
            dx = -PLAYER_SPEED
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            dx = PLAYER_SPEED
            self.facing_right = True

        if keys[pygame.K_SPACE]:
            self.jump_buffer_timer = self.jump_buffer_time
        return dx

    def apply_gravity(self, keys):
        if self.y_vel < 0:
            self.y_vel += GRAVITY * (0.8 if keys[pygame.K_SPACE] else 1.0)
        else:
            self.y_vel += GRAVITY * 1.2
        if self.y_vel > 20:
            self.y_vel = 20

    def jump_if_possible(self):
        if self.jump_buffer_timer > 0 and self.coyote_timer > 0:
            self.y_vel = -PLAYER_JUMP_FORCE
            self.on_ground = False
            self.coyote_timer = 0
            self.jump_buffer_timer = 0

    def shoot_fireball(self):
        if self.has_fire and len(self.fireballs) < PLAYER_FIREBALL_LIMIT:
            r = pygame.Rect(self.rect.centerx, self.rect.centery, 20, 20)
            self.fireballs.append({"rect": r, "dir": 1 if self.facing_right else -1, "dist": 0})

    def update_fireballs(self, ground_length):
        for fb in self.fireballs[:]:
            fb["rect"].x += fb["dir"] * FIREBALL_SPEED
            fb["dist"] += FIREBALL_SPEED
            if fb["dist"] > FIREBALL_MAX_DIST or fb["rect"].right < 0 or fb["rect"].left > ground_length:
                self.fireballs.remove(fb)

    def update_timers(self):
        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= 1
        if self.hurt_cd > 0:
            self.hurt_cd -= 1
        if self.jump_buffer_timer > 0:
            self.jump_buffer_timer -= 1 / FPS
        if self.coyote_timer > 0:
            self.coyote_timer -= 1 / FPS

    def draw(self, screen, camera):
        pygame.draw.rect(screen, BLACK, camera.apply(self.rect))
        for fb in self.fireballs:
            r = camera.apply(fb["rect"])
            pygame.draw.circle(screen, ORANGE, r.center, r.width // 2) 