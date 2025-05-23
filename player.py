import pygame
import os
from bullet import Bullet

class Player:
    def __init__(self, x, y):
        # プレイヤー画像を読み込む（透過対応）
        self.image = pygame.image.load(os.path.join("assets", "images", "player.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.bullets = []

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if self.rect.left < 0:
                self.rect.left = 0
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if self.rect.right > 800:  # 画面幅800想定
                self.rect.right = 800
        if keys[pygame.K_SPACE]:
            # 発射制限：同時に5発まで
            if len(self.bullets) < 5:
                # 弾はプレイヤーの中央上から発射
                bullet_x = self.rect.centerx
                bullet_y = self.rect.top
                self.bullets.append(Bullet(bullet_x, bullet_y))

    def update(self):
        self.handle_input()
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(screen)
