import pygame
from stone import Stone
import time

class Player:
    def __init__(self, screen_width, screen_height, header_height):
        self.size = 16
        self.color = (255, 0, 0)
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.speed = 5
        self.stones = []
        self.last_shot_time = 0
        self.shoot_cooldown = 0.5  # Cooldown in seconds
        self.deadzone = 0.2  # Deadzone threshold
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.header_height = header_height
        self.lives = 3

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

        # Ensure the player stays within screen bounds
        self.x = max(0, min(self.x, self.screen_width - self.size))
        self.y = max(self.header_height, min(self.y, self.screen_height - self.size))

    def shoot(self, direction_x, direction_y):
        current_time = time.time()
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            if abs(direction_x) > self.deadzone or abs(direction_y) > self.deadzone:
                stone = Stone(self.x + self.size // 2, self.y + self.size // 2, direction_x, direction_y)
                self.stones.append(stone)
                self.last_shot_time = current_time

    def reset_position(self):
        self.x = self.screen_width // 2
        self.y = self.screen_height // 2