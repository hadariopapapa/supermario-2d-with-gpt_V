# level.py
import pygame
from settings import *
from enemies import Enemy, Boss, FlyingEnemy
from objects import Box, PowerUp

def load_level(level_map, height=HEIGHT):
    """
    Parse an ASCII level map into objects/entities.
    
    Legend:
      B = Box
      P = PowerUp
      E = Enemy (floor walking)
      F = Flying Enemy
      D = Door (exit)
      Q = Boss Enemy
      . or X = empty/ground space
    """
    boxes = []
    enemies = []
    powerups = []
    door = None
    ground_length = len(level_map[0]) * TILE_SIZE
    has_boss = False

    for row_index, row in enumerate(level_map):
        for col_index, cell in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE

            if cell == "B":
                boxes.append(Box(x, y))

            elif cell == "E":
                # Floor enemy, placed slightly above ground or box top
                enemies.append(Enemy(x, y + (TILE_SIZE - 40)))

            elif cell == "F":
                # Flying enemy (hovering patrol)
                enemies.append(FlyingEnemy(x, y))

            elif cell == "P":
                # PowerUp placed above ground line
                powerups.append(PowerUp(x, height - 60))

            elif cell == "D":
                # Exit door
                door = pygame.Rect(x, height - 120, 60, 70)

            elif cell == "Q":
                # Boss Enemy
                enemies.append(Boss(x, height - 130))
                has_boss = True

            # '.' and 'X' mean open air / ground, ignored here
    
    # If there is a boss, hide the door until boss is defeated
    if has_boss:
        door = None

    return boxes, enemies, powerups, door, ground_length, has_boss