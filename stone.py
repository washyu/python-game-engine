# stone.py
import pygame
import math

class Stone:
    def __init__(self, x, y, direction_x, direction_y):
        self.size = 8
        self.color = (255, 255, 255)  # White color
        self.x = x
        self.y = y
        self.speed = 10

        # Normalize the direction vector
        length = math.hypot(direction_x, direction_y)
        if length != 0:
            self.direction_x = direction_x / length
            self.direction_y = direction_y / length
        else:
            self.direction_x = 0
            self.direction_y = 0

    def move(self):
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def is_off_screen(self, screen_width, screen_height, header_height):
        return self.x < 0 or self.x > screen_width or self.y < header_height or self.y > screen_height

    def collides_with(self, other):
        return (self.x < other.x + other.size and
                self.x + self.size > other.x and
                self.y < other.y + other.size and
                self.y + self.size > other.y)