# utils.py
import pygame
from settings import *

def draw_text(screen, text, pos, color=BLACK, font=None, center=False):
    if font is None:
        raise ValueError("Must pass a font")
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center: rect.center = pos
    else: rect.topleft = pos
    screen.blit(surf, rect)

def draw_coin_animation(screen, anims, camera):
    for anim in anims:
        pos = camera.apply_pos((anim["x"], anim["y"]))
        pygame.draw.circle(screen, GOLD, pos, 10)

def update_coin_animation(anims):
    for anim in anims[:]:
        anim["y"] -= 2
        anim["life"] -= 1
        if anim["life"] <= 0:
            anims.remove(anim)

def draw_hit_flash(screen, duration):
    if duration > 0:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 0, 0, 80))
        screen.blit(overlay, (0, 0))