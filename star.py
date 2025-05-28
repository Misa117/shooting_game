import pygame
import random

class Star:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset()

    def reset(self):
        self.x = random.randint(0, self.screen_width)
        self.y = random.randint(0, self.screen_height)
        self.radius = random.randint(1, 3)
        self.speed = random.uniform(0.2, 0.8)

    def update(self, speed_multiplier=1):
        self.y -= self.speed * speed_multiplier
        if self.y < 0:
            self.reset()

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius)

