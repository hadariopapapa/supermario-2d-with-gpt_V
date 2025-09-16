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

# Player settings
player_width, player_height = 40, 50
player_x, player_y = 100, HEIGHT - player_height - 50
player_vel = 5
jump_strength = 15
gravity = 0.8
on_ground = False

player = pygame.Rect(player_x, player_y, player_width, player_height)
y_velocity = 0

# Boxes (rect and "used" state)
boxes = [
    {"rect": pygame.Rect(300, 350, 50, 50), "used": False},
    {"rect": pygame.Rect(500, 300, 50, 50), "used": False},
    {"rect": pygame.Rect(650, 250, 50, 50), "used": False}
]

# Coins collected
coins = 0
font = pygame.font.SysFont("Arial", 30)

def draw():
    screen.fill(WHITE)  # Background
    # Draw ground
    pygame.draw.rect(screen, GREEN, (0, HEIGHT - 50, WIDTH, 50))
    # Draw player
    pygame.draw.rect(screen, BLACK, player)
    # Draw boxes
    for box in boxes:
        color = GREY if box["used"] else BROWN
        pygame.draw.rect(screen, color, box["rect"])
    # Draw score
    score_text = font.render(f"Coins: {coins}", True, GOLD)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

# Main loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Input handling ---
    keys = pygame.key.get_pressed()

    move_x = 0
    if keys[pygame.K_LEFT]:
        move_x = -player_vel
    elif keys[pygame.K_RIGHT]:
        move_x = player_vel
    else:
        move_x = 0  # instant stop, no sliding

    # Start jump
    if keys[pygame.K_SPACE] and on_ground:
        y_velocity = -jump_strength
        on_ground = False

    # --- Variable jump gravity (Hollow Knight feel) ---
    if y_velocity < 0:  # going upward
        if keys[pygame.K_SPACE]:
            y_velocity += gravity * 0.8   # hold jump = slower rise
        else:
            y_velocity += gravity * 1.0   # release = cut short
    else:
        y_velocity += gravity * 1.2       # falling feels heavier

    if y_velocity > 20:  # clamp fall speed
        y_velocity = 20

    # --- Vertical movement ---
    player.y += y_velocity
    on_ground = False

    for box in boxes:
        rect = box["rect"]
        if player.colliderect(rect):
            # Landing on top
            if y_velocity > 0 and player.bottom > rect.top and abs(player.bottom - rect.top) < 20:
                player.bottom = rect.top
                y_velocity = 0
                on_ground = True
            # Head bump from below
            elif y_velocity < 0 and player.top < rect.bottom and abs(player.top - rect.bottom) < 20:
                player.top = rect.bottom
                y_velocity = 0
                if not box["used"]:
                    coins += 1
                    box["used"] = True

    # --- Ground collision ---
    if player.bottom >= HEIGHT - 50:
        player.bottom = HEIGHT - 50
        y_velocity = 0
        on_ground = True

    # --- Horizontal movement ---
    player.x += move_x
    for box in boxes:
        rect = box["rect"]
        if player.colliderect(rect):
            if move_x > 0:
                player.right = rect.left
            elif move_x < 0:
                player.left = rect.right

    # --- Draw everything ---
    draw()

# Quit properly
pygame.quit()
sys.exit()