import pygame, sys
from settings import *
from levels import LEVELS
from scenes import GameScene   # import GameScene definition

# --- INIT ---
pygame.init()
FONT = pygame.font.SysFont("Arial", 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mario Clone")
clock = pygame.time.Clock()

# === SCENE MANAGEMENT ===
current_scene = GameScene(LEVELS, FONT)

# === MAIN LOOP ===
running = True
while running:
    clock.tick(FPS)
    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    current_scene.handle_events(events)
    current_scene.update(keys)
    current_scene.draw(screen)

pygame.quit()
sys.exit()