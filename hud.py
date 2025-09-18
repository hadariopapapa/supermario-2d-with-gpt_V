# hud.py
from utils import draw_text
from settings import WIDTH, HEIGHT, GOLD, ORANGE, RED, GREEN, BLACK

def draw_hud(screen, player, coins, font):
    """
    Draws the main HUD (coins, fire ability, lives).
    """
    draw_text(screen, f"Coins: {coins}", (10, 10), GOLD, font)
    draw_text(screen, f"Fire: {'YES' if player.has_fire else 'NO'}", (WIDTH - 200, 10), ORANGE, font)
    draw_text(screen, f"Lives: {player.hp}", (WIDTH - 200, 40), RED, font)

def draw_end_messages(screen, font, game_over, victory):
    """
    Draws messages like GAME OVER or YOU WIN.
    """
    if game_over:
        draw_text(screen, "GAME OVER", (WIDTH//2, HEIGHT//2 - 100), RED, font, center=True)
        draw_text(screen, "Press R to Restart", (WIDTH//2, HEIGHT//2), BLACK, font, center=True)
    elif victory:
        draw_text(screen, "YOU WIN!", (WIDTH//2, HEIGHT//2 - 100), GREEN, font, center=True)
        draw_text(screen, "Press N for Next Level", (WIDTH//2, HEIGHT//2), BLACK, font, center=True)