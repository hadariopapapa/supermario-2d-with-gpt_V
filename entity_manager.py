import collision_manager as collisions
from utils import draw_coin_animation, update_coin_animation, draw_text
from settings import BLUE, BLACK
from enemies import Boss

class EntityManager:
    def __init__(self, boxes, enemies, powerups, door, ground_length, has_boss):
        self.boxes = boxes
        self.enemies = enemies
        self.powerups = powerups
        self.coin_animations = []
        self.door = door
        self.ground_length = ground_length
        self.has_boss = has_boss
        self.coins = 0

    def update(self, player, prev_bottom, game_over):
        # Player vs Boxes
        self.coins = collisions.check_player_box_horizontal(player, self.boxes) or self.coins
        self.coins = collisions.check_player_box_vertical(player, self.boxes, self.coins, self.coin_animations, prev_bottom)

        # Ground
        collisions.check_player_ground(player)

        # Enemies
        for e in self.enemies:
            if isinstance(e, Boss):
                e.update(self.boxes, self.ground_length, player)
            else:
                e.update(self.boxes, self.ground_length)

        # Player vs Enemies
        new_door, game_over = collisions.check_player_enemy(player, self.enemies, prev_bottom, self.ground_length, game_over)
        if new_door: self.door = new_door

        # Powerups
        collisions.check_player_powerups(player, self.powerups)

        # Fireballs
        new_door = collisions.check_fireballs(player, self.enemies, self.boxes, self.ground_length)
        if new_door: self.door = new_door

        # Coin animations
        update_coin_animation(self.coin_animations)

        return game_over

    def draw(self, screen, camera, font):
        for box in self.boxes:
            box.draw(screen, camera)

        for e in self.enemies:
            if isinstance(e, Boss):
                e.draw(screen, camera, font)
            else:
                e.draw(screen, camera)

        for pu in self.powerups:
            pu.draw(screen, camera)

        draw_coin_animation(screen, self.coin_animations, camera)

        if self.door:
            import pygame
            pygame.draw.rect(screen, BLUE, camera.apply(self.door))
            draw_text(screen, "EXIT", camera.apply_pos((self.door.x, self.door.y - 30)), BLACK, font)