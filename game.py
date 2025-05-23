import pygame
from player import Player
from enemy import Enemy
import random

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player(375, 500)
        self.enemies = []
        self.font = pygame.font.SysFont(None, 60)
        self.game_over = False

        self.stars = [Star(800, 600) for _ in range(50)]  # 星50個生成

    def update(self):
        if self.game_over:
            return

        self.player.update()

        for star in self.stars:
            star.update()

        # 敵の追加
        if random.randint(1, 30) == 1:
            self.enemies.append(Enemy())

        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.rect.top > 600:
                self.enemies.remove(enemy)

        # 弾と敵の当たり判定
        for bullet in self.player.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    self.player.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    break

        # 敵とプレイヤーの当たり判定（ゲームオーバー）
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.game_over = True

    def draw(self):
        self.screen.fill((0, 0, 0))

        for star in self.stars:
            star.draw(self.screen)

        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)

        if self.game_over:
            text = self.font.render("GAME OVER", True, (255, 0, 0))
            rect = text.get_rect(center=(400, 300))
            self.screen.blit(text, rect)

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
        self.speed = random.uniform(0.2, 0.8)  # 上に動く速さ

    def update(self):
        self.y -= self.speed
        if self.y < 0:
            self.x = random.randint(0, self.screen_width)
            self.y = self.screen_height
            self.radius = random.randint(1, 3)
            self.speed = random.uniform(0.2, 0.8)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius)
