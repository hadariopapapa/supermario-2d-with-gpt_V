# camera.py
from settings import WIDTH, HEIGHT

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, player_rect, level_width, level_height=HEIGHT):
        """
        Update camera offset (scroll) to follow player.
        Horizontal only for now.
        """
        self.x = max(0, min(player_rect.x - WIDTH // 2, level_width - WIDTH))
        # self.y = max(0, min(player_rect.y - HEIGHT // 2, level_height - HEIGHT))  # unlock if vertical levels

    def apply(self, rect):
        """Convert game world rect to screen coords by applying the camera offset."""
        return rect.move(-self.x, -self.y)

    def apply_pos(self, pos):
        """Convert world (x, y) into screen (x, y)."""
        return (pos[0] - self.x, pos[1] - self.y) 