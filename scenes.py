import pygame
from settings import *
from player import Player
from enemies import Boss
from camera import Camera
from level import load_level
from entity_manager import EntityManager
from utils import draw_hit_flash
from hud import draw_hud, draw_end_messages
import collision_manager as collisions


# =======================================
#   SCENE BASE CLASS
# =======================================
class Scene:
    def handle_events(self, events): pass
    def update(self, keys): pass
    def draw(self, screen): pass


# =======================================
#   MAIN MENU SCENE
# =======================================
class MainMenuScene(Scene):
    def __init__(self, font):
        self.font = font
        self.selected = 0
        self.options = ["PLAY", "QUIT"]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.options[self.selected] == "PLAY":
                        return "GAME"
                    elif self.options[self.selected] == "QUIT":
                        pygame.quit(); exit()
        return None

    def update(self, keys): pass

    def draw(self, screen):
        screen.fill(BLACK)
        title = self.font.render("SUPER MARIO Batata", True, GOLD)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))

        for i, option in enumerate(self.options):
            color = GREEN if i == self.selected else WHITE
            text = self.font.render(option, True, color)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 + i*50))

        pygame.display.flip()


# =======================================
#   PAUSE MENU SCENE
# =======================================
class PauseMenuScene(Scene):
    def __init__(self, font, game_scene):
        self.font = font
        self.game_scene = game_scene
        self.selected = 0
        self.options = ["RESUME", "MAIN MENU", "QUIT"]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.options[self.selected] == "RESUME":
                        return "RESUME"
                    elif self.options[self.selected] == "MAIN MENU":
                        self.game_scene = None
                        return "MAIN_MENU"
                    elif self.options[self.selected] == "QUIT":
                        pygame.quit(); exit()
        return None

    def update(self, keys): pass

    def draw(self, screen):
        if self.game_scene:
            self.game_scene.draw_world(screen)

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        pause_text = self.font.render("PAUSED", True, GOLD)
        screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//4))

        for i, option in enumerate(self.options):
            color = GREEN if i == self.selected else WHITE
            text = self.font.render(option, True, color)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 + i*50))

        pygame.display.flip()


# =======================================
#   VICTORY SCENE
# =======================================
class VictoryScene(Scene):
    def __init__(self, font):
        self.font = font
        self.selected = 0
        self.options = ["Main Menu", "QUIT"]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.options[self.selected] == "Main Menu":
                        return "Main Menu"
                    elif self.options[self.selected] == "QUIT":
                        pygame.quit(); exit()
        return None

    def update(self, keys): pass

    def draw(self, screen):
        screen.fill(BLACK)

        title = self.font.render("YOU FINISHED THE GAME!", True, GOLD)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))

        for i, option in enumerate(self.options):
            color = GREEN if i == self.selected else WHITE
            text = self.font.render(option, True, color)
            screen.blit(text, (WIDTH//2 - text.get_width()//2,
                               HEIGHT//2 + i*60))

        pygame.display.flip()


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
        self.player = Player()
        self.camera = Camera()
        boxes, enemies, powerups, door, ground_length, has_boss = load_level(
            self.levels[self.current_level_index]
        )
        self.entities = EntityManager(boxes, enemies, powerups, door, ground_length, has_boss)
        self.game_over = False
        self.victory = False

    def load_next_level(self):
        self.current_level_index += 1
        if self.current_level_index < len(self.levels):
            self.reset_level()
        else:
            return "VICTORY"   # 🔥 Game completed signal

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit(); exit()

            if self.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_level()

            if self.victory and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_level()
                elif event.key == pygame.K_n:
                    return self.load_next_level()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                self.player.shoot_fireball()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "PAUSE"
        return None

    def update(self, keys):
        if self.game_over or self.victory: return None

        prev_bottom = self.player.rect.bottom
        move_x = self.player.handle_input(keys)
        self.player.apply_gravity(keys)
        self.player.update_timers()

        self.player.rect.x += move_x
        collisions.check_player_box_horizontal(self.player, self.entities.boxes)

        self.player.rect.y += self.player.y_vel
        self.entities.coins = collisions.check_player_box_vertical(
            self.player, self.entities.boxes, self.entities.coins,
            self.entities.coin_animations, prev_bottom
        )

        self.game_over = self.entities.update(self.player, prev_bottom, self.game_over)
        self.player.jump_if_possible()

        if self.entities.door and self.player.rect.colliderect(self.entities.door):
            boss_alive = any(isinstance(e, Boss) and e.alive for e in self.entities.enemies)
            if not boss_alive:
                if self.current_level_index == len(self.levels) - 1:
                    return "VICTORY"
                else:
                    self.victory = True

        self.camera.update(self.player.rect, self.entities.ground_length)
        return None

    def draw_world(self, screen):
        screen.fill(WHITE)
        ground_rect = pygame.Rect(0, HEIGHT - 50, self.entities.ground_length, 50)
        pygame.draw.rect(screen, GREEN, self.camera.apply(ground_rect))

        if not self.game_over and not self.victory:
            self.player.draw(screen, self.camera)

        self.entities.draw(screen, self.camera, self.font)
        draw_hud(screen, self.player, self.entities.coins, self.font)
        draw_hit_flash(screen, self.player.hit_flash_timer)
        draw_end_messages(screen, self.font, self.game_over, self.victory)

    def draw(self, screen):
        self.draw_world(screen)
        pygame.display.flip()