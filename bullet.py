import pygame

class Bullet:
    def __init__(self, x, y, key=None):
        self.x = x
        self.y = y
        self.key = key
        self.speed = -5  # 弾を上に移動させる速度（負の値）
        self.rect = pygame.Rect(self.x, self.y, 5, 10)  # 弾のサイズを設定

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), self.rect)
