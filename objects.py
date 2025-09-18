# objects.py
import pygame
from settings import *

class Box:
    """Solid box, gives a coin when hit. Turns grey when empty."""
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.used = False

    def hit(self, coins, coin_animations):
        if not self.used:
            coins += 1
            self.used = True
            coin_animations.append({
                "x": self.rect.centerx,
                "y": self.rect.top - 10,
                "life": 30
            })
        return coins

    def draw(self, screen, camera):
        color = GREY if self.used else BROWN
        pygame.draw.rect(screen, color, camera.apply(self.rect))


class PowerUp:
    """A collectible power-up."""
    def __init__(self, x, y):
        self.rect = pygame.Rect(x+10, y, 30, 30)

    def draw(self, screen, camera):
        pygame.draw.rect(screen, PURPLE, camera.apply(self.rect))