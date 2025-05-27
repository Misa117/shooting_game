# explosion.py

import pygame
import random

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.particles = []
        self.x = x
        self.y = y
        self.lifetime = 30  # フレーム数

        for _ in range(20):  # 粒の数
            dx = random.uniform(-2, 2)
            dy = random.uniform(-2, 2)
            size = random.randint(2, 4)
            color = random.choice([(255, 255, 0), (255, 100, 0), (255, 200, 50)])
            self.particles.append([x, y, dx, dy, size, color])

        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            return False  # アニメーション終了を示す

        # 新しい画像生成（透明背景）
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)

        for particle in self.particles:
            particle[0] += particle[2]
            particle[1] += particle[3]
            pygame.draw.rect(
                self.image,
                particle[5],
                pygame.Rect(particle[0] - self.x + 20, particle[1] - self.y + 20, particle[4], particle[4])
            )
        return True  # 継続中
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    