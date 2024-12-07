import pygame
import math
import random

class Monster:
    def __init__(self, screen_width, screen_height, header_height):
        self.size = 24
        self.color = (0, 255, 0)
        self.x, self.y = self.randomize_position_off_play_area(screen_width, screen_height, header_height)
        self.speed = 2

    def randomize_position_off_play_area(self, screen_width, screen_height, header_height):
        side = random.choice(["left", "right", "top", "bottom"])
        if side == 'top':
            x = random.randint(0 , screen_width - self.size)
            y = header_height - self.size
        elif side == 'bottom':
            x = random.randint(0, screen_width - self.size)
            y = screen_height + header_height
        elif side == 'left':
            x = -self.size
            y = random.randint(header_height, screen_height - self.size)
        elif side == 'right':
            x = screen_width
            y = random.randint(header_height, screen_height - self.size)
        return x, y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def move_towards(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            dx /= distance
            dy /= distance
        self.x += dx * self.speed
        self.y += dy * self.speed
    
    def avoid_collisions(self, monsters):
        for monster in monsters:
            if monster != self:
                dx = monster.x - self.x
                dy = monster.y - self.y
                dist = math.hypot(dx, dy)
                if dist < self.size:
                    if dist != 0:
                        dx /= dist
                        dy /= dist
                    self.x -= dx * self.speed
                    self.y -= dy * self.speed