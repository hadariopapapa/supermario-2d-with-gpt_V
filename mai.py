import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("1stP")

clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (150, 75, 0)
GREY = (160, 160, 160)
GOLD = (255, 215, 0)
GREEN = (50, 200, 50)
RED = (200, 50, 50)
BLUE = (50, 50, 200)

# Player settings
player_width, player_height = 40, 50
player_spawn_x, player_spawn_y = 100, HEIGHT - player_height - 50
player_vel = 5
jump_strength = 15
gravity = 0.8

player = pygame.Rect(player_spawn_x, player_spawn_y, player_width, player_height)
y_velocity = 0
on_ground = False

# Level length & ground
ground_length = 2000  # wider than screen

# Boxes (coin blocks)
boxes = [
    {"rect": pygame.Rect(300, 350, 50, 50), "used": False},
    {"rect": pygame.Rect(900, 300, 50, 50), "used": False},
    {"rect": pygame.Rect(1400, 250, 50, 50), "used": False}
]

coins = 0
font = pygame.font.SysFont("Arial", 30)

# Movement timers
coyote_time = 0.1
coyote_timer = 0
jump_buffer_time = 0.1
jump_buffer_timer = 0

# Coin animations
coin_animations = []

# Enemies
enemies = [
    {"rect": pygame.Rect(600, HEIGHT - 90, 40, 40), "dir": -1, "alive": True},
    {"rect": pygame.Rect(1200, HEIGHT - 90, 40, 40), "dir": 1, "alive": True}
]

# --- NEW: Door at end of level ---
door = pygame.Rect(ground_length - 80, HEIGHT - 120, 60, 70)

# Game state
game_over = False
victory = False

# Camera
camera_x = 0

def reset_game():
    global player, y_velocity, on_ground, coins, coin_animations
    global game_over, victory, enemies, camera_x
    player.x = player_spawn_x
    player.y = player_spawn_y
    y_velocity = 0
    on_ground = False
    coins = 0
    coin_animations = []
    for box in boxes:
        box["used"] = False
    enemies = [
        {"rect": pygame.Rect(600, HEIGHT - 90, 40, 40), "dir": -1, "alive": True},
        {"rect": pygame.Rect(1200, HEIGHT - 90, 40, 40), "dir": 1, "alive": True}
    ]
    game_over = False
    victory = False
    camera_x = 0

def draw():
    screen.fill(WHITE)
    # ground
    pygame.draw.rect(screen, GREEN, (0 - camera_x, HEIGHT - 50, ground_length, 50))

    if not game_over and not victory:
        pygame.draw.rect(screen, BLACK, (player.x - camera_x, player.y, player.width, player.height))

    # Boxes
    for box in boxes:
        color = GREY if box["used"] else BROWN
        pygame.draw.rect(screen, color, (box["rect"].x - camera_x, box["rect"].y, box["rect"].width, box["rect"].height))

    # Enemies
    for enemy in enemies:
        if enemy["alive"]:
            pygame.draw.rect(screen, RED, (enemy["rect"].x - camera_x, enemy["rect"].y, enemy["rect"].width, enemy["rect"].height))

    # Coin pops
    for anim in coin_animations:
        pygame.draw.circle(screen, GOLD, (int(anim["x"] - camera_x), int(anim["y"])), 10)

    # Door
    pygame.draw.rect(screen, BLUE, (door.x - camera_x, door.y, door.width, door.height))

    # --- NEW: Door label ---
    door_font = pygame.font.SysFont("Arial", 24, bold=True)
    door_text = door_font.render("EXIT", True, BLACK)
    door_x = door.x - camera_x + (door.width // 2 - door_text.get_width() // 2)
    door_y = door.y - 30  # just above door
    screen.blit(door_text, (door_x, door_y))

    # Score
    score_text = font.render(f"Coins: {coins}", True, GOLD)
    screen.blit(score_text, (10, 10))

    # --- GAME OVER ---
    if game_over:
        go_font = pygame.font.SysFont("Arial", 60, bold=True)
        restart_font = pygame.font.SysFont("Arial", 36)
        go_text = go_font.render("GAME OVER", True, RED)
        screen.blit(go_text, (WIDTH//2 - go_text.get_width()//2, HEIGHT//2 - 100))
        restart_text = restart_font.render("Press R to Restart", True, BLACK)
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2))

    # --- VICTORY ---
    if victory:
        win_font = pygame.font.SysFont("Arial", 60, bold=True)
        restart_font = pygame.font.SysFont("Arial", 36)
        win_text = win_font.render("YOU WIN!", True, GREEN)
        screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 100))
        restart_text = restart_font.render("Press R to Restart", True, BLACK)
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2))

    pygame.display.flip()

# MAIN LOOP
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if (game_over or victory) and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset_game()

    if game_over or victory:
        draw()
        continue

    keys = pygame.key.get_pressed()
    move_x = 0
    if keys[pygame.K_LEFT]:
        move_x = -player_vel
    elif keys[pygame.K_RIGHT]:
        move_x = player_vel

    # Timers
    coyote_timer -= 1/FPS
    jump_buffer_timer -= 1/FPS
    if keys[pygame.K_SPACE]:
        jump_buffer_timer = jump_buffer_time

    # Gravity
    if y_velocity < 0:
        if keys[pygame.K_SPACE]:
            y_velocity += gravity * 0.8
        else:
            y_velocity += gravity * 1.0
    else:
        y_velocity += gravity * 1.2
    if y_velocity > 20:
        y_velocity = 20

    # Vertical
    player.y += y_velocity
    on_ground = False
    for box in boxes:
        rect = box["rect"]
        if player.colliderect(rect):
            if y_velocity > 0 and player.bottom > rect.top and abs(player.bottom - rect.top) < 20:
                player.bottom = rect.top
                y_velocity = 0
                on_ground = True
                coyote_timer = coyote_time
            elif y_velocity < 0 and player.top < rect.bottom and abs(player.top - rect.bottom) < 20:
                player.top = rect.bottom
                y_velocity = 0
                if not box["used"]:
                    coins += 1
                    box["used"] = True
                    coin_animations.append({"x": rect.centerx, "y": rect.top - 10, "life": 30})

    # Ground
    if player.bottom >= HEIGHT - 50:
        player.bottom = HEIGHT - 50
        y_velocity = 0
        on_ground = True
        coyote_timer = coyote_time

    # Jump
    if jump_buffer_timer > 0 and coyote_timer > 0:
        y_velocity = -jump_strength
        on_ground = False
        coyote_timer = 0
        jump_buffer_timer = 0

    # Horizontal move
    player.x += move_x
    for box in boxes:
        rect = box["rect"]
        if player.colliderect(rect):
            if move_x > 0: player.right = rect.left
            elif move_x < 0: player.left = rect.right

    # Camera follows
    camera_x = player.x - WIDTH//2
    if camera_x < 0:
        camera_x = 0
    if camera_x > ground_length - WIDTH:
        camera_x = ground_length - WIDTH

    # Enemies
    for enemy in enemies:
        if not enemy["alive"]: continue
        enemy["rect"].x += enemy["dir"] * 2
        if enemy["rect"].left <= 0 or enemy["rect"].right >= ground_length:
            enemy["dir"] *= -1
        for box in boxes:
            if enemy["rect"].colliderect(box["rect"]):
                if enemy["dir"] > 0: enemy["rect"].right = box["rect"].left
                else: enemy["rect"].left = box["rect"].right
                enemy["dir"] *= -1
        if player.colliderect(enemy["rect"]):
            if y_velocity > 0 and player.bottom <= enemy["rect"].top + 15:
                enemy["alive"] = False
                y_velocity = -jump_strength * 0.7
            else:
                game_over = True

    # Coin anims
    for anim in coin_animations[:]:
        anim["y"] -= 2
        anim["life"] -= 1
        if anim["life"] <= 0: coin_animations.remove(anim)

    # --- Victory check: touching door triggers win ---
    if player.colliderect(door):
        victory = True

    draw()

pygame.quit()
sys.exit()