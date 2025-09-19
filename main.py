import pygame, sys
from settings import *
from levels import LEVELS
from scenes import GameScene, MainMenuScene, PauseMenuScene, VictoryScene

pygame.init()
FONT = pygame.font.SysFont("Arial", 30)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mario Batata")
clock = pygame.time.Clock()

current_scene = MainMenuScene(FONT)
running = True

while running:
    clock.tick(FPS)
    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    transition = current_scene.handle_events(events)

    # === Scene transitions ===
    if isinstance(current_scene, MainMenuScene):
        if transition == "GAME":
            current_scene = GameScene(LEVELS, FONT)
            continue

    elif isinstance(current_scene, GameScene):
        if transition == "PAUSE":
            current_scene = PauseMenuScene(FONT, current_scene)
            continue
        elif transition == "VICTORY":
            current_scene = VictoryScene(FONT)
            continue

    elif isinstance(current_scene, PauseMenuScene):
        if transition == "RESUME" and current_scene.game_scene:
            current_scene = current_scene.game_scene
            continue
        elif transition == "MAIN_MENU":
            current_scene = MainMenuScene(FONT)
            continue

    elif isinstance(current_scene, VictoryScene):
        if transition == "Main Menu":
            current_scene = MainMenuScene(FONT)  # fresh start
            continue

    # === Update + Draw current scene ===
    extra_command = current_scene.update(keys)
    # if a scene's update loop requests transition
    if extra_command == "VICTORY":
        current_scene = VictoryScene(FONT)
        continue

    current_scene.draw(screen)

pygame.quit()
sys.exit() 