import pygame
import random
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Enemy:
    _images = None  # クラス変数として画像リストを保持（初期はNone）

    @classmethod
    def load_images(cls):
        if cls._images is None:
            cls._images = [
                pygame.image.load(os.path.join(BASE_DIR, "assets", "images", f"enemy{i}.png")).convert_alpha()
                for i in range(1, 5)
            ]

    def __init__(self):
        # 画像が読み込まれてなければ読み込む
        self.load_images()
        self.image = random.choice(self._images)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 750)
        self.rect.y = -50
        self.speed = random.uniform(1.5, 4.0)

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
