import pygame
from settings import *
from player import Player
from enemies import Boss
from camera import Camera
from level import load_level
from entity_manager import EntityManager
from utils import draw_hit_flash
from hud import draw_hud, draw_end_messages
import collision_manager as collisions   # ✅ switch from physics to collisions


# =======================================
#   SCENE BASE CLASS
# =======================================
class Scene:
    def handle_events(self, events): pass
    def update(self, keys): pass
    def draw(self, screen): pass


# =======================================
#   GAME SCENE
# =======================================
class GameScene(Scene):
    def __init__(self, levels, font):
        self.font = font
        self.levels = levels
        self.current_level_index = 0
        self.reset_level()

    def reset_level(self):
        """Reset current level state."""
        self.player = Player()
        self.camera = Camera()
        boxes, enemies, powerups, door, ground_length, has_boss = load_level(
            self.levels[self.current_level_index]
        )
        self.entities = EntityManager(boxes, enemies, powerups, door, ground_length, has_boss)
        self.game_over = False
        self.victory = False

    def load_next_level(self):
        """Go to next level or exit if none left."""
        self.current_level_index += 1
        if self.current_level_index < len(self.levels):
            self.reset_level()
        else:
            pygame.quit()
            exit()

    # ---------------------------
    # Handle Inputs / Events
    # ---------------------------
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if self.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_level()

            if self.victory and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_level()
                if event.key == pygame.K_n:
                    self.load_next_level()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                self.player.shoot_fireball()

    # ---------------------------
    # Game Update Loop
    # ---------------------------
    def update(self, keys):
        if self.game_over or self.victory:
            return

        prev_bottom = self.player.rect.bottom
        move_x = self.player.handle_input(keys)
        self.player.apply_gravity(keys)
        self.player.update_timers()

        # === Movement Splits ===
        # Horizontal move
        self.player.rect.x += move_x
        collisions.check_player_box_horizontal(self.player, self.entities.boxes)

        # Vertical move
        self.player.rect.y += self.player.y_vel
        self.entities.coins = collisions.check_player_box_vertical(
            self.player,
            self.entities.boxes,
            self.entities.coins,
            self.entities.coin_animations,
            prev_bottom,
        )

        # Ground/Enemies/Powerups/Fireballs + coin anims managed by entity manager
        self.game_over = self.entities.update(self.player, prev_bottom, self.game_over)

        # Handle jump (buffer + coyote)
        self.player.jump_if_possible()

        # === Victory Check at Door ===
        if self.entities.door and self.player.rect.colliderect(self.entities.door):
            boss_alive = any(isinstance(e, Boss) and e.alive for e in self.entities.enemies)
            if not boss_alive:
                self.victory = True

        # Update camera to follow player
        self.camera.update(self.player.rect, self.entities.ground_length)

    # ---------------------------
    # Draw Everything
    # ---------------------------
    def draw(self, screen):
        screen.fill(WHITE)

        # Draw ground
        ground_rect = pygame.Rect(0, HEIGHT - 50, self.entities.ground_length, 50)
        pygame.draw.rect(screen, GREEN, self.camera.apply(ground_rect))

        # Player
        if not self.game_over and not self.victory:
            self.player.draw(screen, self.camera)

        # Entities (boxes, enemies, powerups, coins, door)
        self.entities.draw(screen, self.camera, self.font)

        # HUD
        draw_hud(screen, self.player, self.entities.coins, self.font)

        # Red flash when hurt
        draw_hit_flash(screen, self.player.hit_flash_timer)

        # End messages
        draw_end_messages(screen, self.font, self.game_over, self.victory)

        pygame.display.flip()