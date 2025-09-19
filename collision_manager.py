import pygame
from settings import *
from config import PLAYER_JUMP_FORCE, FIREBALL_SPEED, FIREBALL_MAX_DIST


# ======================================================
#   PLAYER vs BOXES
# ======================================================

def check_player_box_horizontal(player, boxes):
    """Ensure player can't walk through boxes horizontally."""
    for box in boxes:
        if player.rect.colliderect(box.rect):
            if player.rect.centerx < box.rect.centerx:
                player.rect.right = box.rect.left
            else:
                player.rect.left = box.rect.right


def check_player_box_vertical(player, boxes, coins, coin_animations, prev_bottom):
    """
    Handle vertical collisions:
    - landing on top of boxes
    - bumping bottom of boxes
    """
    player.on_ground = False
    for box in boxes:
        if player.rect.colliderect(box.rect):
            # Standing on top of box
            if player.y_vel > 0 and prev_bottom <= box.rect.top:
                player.rect.bottom = box.rect.top
                player.y_vel = 0
                player.on_ground = True
                player.coyote_timer = player.coyote_time

            # Hitting box from underneath
            elif player.y_vel < 0 and player.rect.top <= box.rect.bottom:
                player.rect.top = box.rect.bottom + 1
                player.y_vel = 0
                coins = box.hit(coins, coin_animations)

    return coins


# ======================================================
#   PLAYER vs GROUND
# ======================================================

def check_player_ground(player):
    """Keep the player clamped above the green ground strip."""
    if player.rect.bottom >= HEIGHT - 50:
        player.rect.bottom = HEIGHT - 50
        player.y_vel = 0
        player.on_ground = True
        player.coyote_timer = player.coyote_time


# ======================================================
#   PLAYER vs ENEMIES
# ======================================================

def check_player_enemy(player, enemies, prev_bottom, ground_length, game_over):
    """Check player collision with enemies (normal + boss)."""
    from enemies import Boss   # to avoid circular imports

    global_door = None
    for e in enemies:
        if not e.alive:
            continue

        if player.rect.colliderect(e.rect):
            # ----- Boss logic -----
            if isinstance(e, Boss):
                # Player stomps boss
                if player.y_vel > 0 and prev_bottom <= e.rect.top:
                    player.y_vel = -PLAYER_JUMP_FORCE * 0.7
                    if player.hurt_cd == 0 and not game_over:
                        player.hp -= 1
                        player.hit_flash_timer = FPS // 3
                        player.hurt_cd = FPS
                        if player.hp <= 0:
                            game_over = True
                else:  # Side hit hurts player
                    if e.cooldown == 0 and player.hurt_cd == 0 and not game_over:
                        player.hp -= 1
                        player.hit_flash_timer = FPS // 3
                        player.hurt_cd = FPS
                        e.cooldown = FPS
                        # knockback
                        if player.rect.centerx < e.rect.centerx:
                            player.rect.right = e.rect.left
                            player.rect.x -= 10
                        else:
                            player.rect.left = e.rect.right
                            player.rect.x += 10
                        player.y_vel = -5
                        if player.hp <= 0:
                            game_over = True

            # ----- Normal enemy logic -----
            else:
                if player.y_vel > 0 and prev_bottom <= e.rect.top:
                    e.alive = False
                    player.y_vel = -PLAYER_JUMP_FORCE * 0.7
                elif player.hurt_cd == 0 and not game_over:
                    player.hp -= 1
                    player.hit_flash_timer = FPS // 3
                    player.hurt_cd = FPS
                    if player.rect.centerx < e.rect.centerx:
                        player.rect.right = e.rect.left
                        player.rect.x -= 10
                    else:
                        player.rect.left = e.rect.right
                        player.rect.x += 10
                    player.y_vel = -5
                    if player.hp <= 0:
                        game_over = True

    return global_door, game_over


# ======================================================
#   PLAYER vs POWERUPS
# ======================================================

def check_player_powerups(player, powerups):
    for pu in powerups[:]:
        if player.rect.colliderect(pu.rect):
            player.has_fire = True
            powerups.remove(pu)


# ======================================================
#   FIREBALLS vs BOXES/ENEMIES
# ======================================================

def check_fireballs(player, enemies, boxes, ground_length):
    """Fireballs vanish on boxes; kill enemies; damage boss."""
    from enemies import Boss
    global_door = None

    for fb in player.fireballs[:]:
        fb["rect"].x += fb["dir"] * FIREBALL_SPEED
        fb["dist"] += FIREBALL_SPEED

        # Out of range
        if fb["dist"] > FIREBALL_MAX_DIST or fb["rect"].right < 0 or fb["rect"].left > ground_length:
            player.fireballs.remove(fb)
            continue

        # Hit box
        if any(fb["rect"].colliderect(box.rect) for box in boxes):
            if fb in player.fireballs:
                player.fireballs.remove(fb)
            continue

        # Hit enemy
        for e in enemies:
            if e.alive and fb["rect"].colliderect(e.rect):
                if isinstance(e, Boss):
                    e.hp -= 1
                    if e.hp <= 0:
                        e.alive = False
                        global_door = pygame.Rect(ground_length - 100, HEIGHT - 120, 60, 70)
                else:
                    e.alive = False
                if fb in player.fireballs:
                    player.fireballs.remove(fb)
                break

    return global_door


# ======================================================
#   ENEMIES vs BOXES
# ======================================================

def check_enemy_box(enemy, boxes, ground_height=HEIGHT-50):
    """
    Enemies patrol left/right:
    - Snap to ground
    - Stand on boxes
    - Reverse on wall hit
    """
    enemy.rect.bottom = ground_height
    for box in boxes:
        if enemy.rect.colliderect(box.rect) and enemy.rect.centery < box.rect.centery:
            enemy.rect.bottom = box.rect.top

    enemy.rect.x += enemy.dir * enemy.speed
    for box in boxes:
        if enemy.rect.colliderect(box.rect):
            if enemy.dir > 0:
                enemy.rect.right = box.rect.left
            else:
                enemy.rect.left = box.rect.right
            enemy.dir *= -1
            break 