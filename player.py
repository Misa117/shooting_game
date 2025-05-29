import pygame
from bullet import Bullet
from romaji_map import kana_to_romaji
from explosion import Explosion  # 爆発追加



class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/images/player.png").convert_alpha()
        self.shot_sound = pygame.mixer.Sound("assets/sounds/shot.wav")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.bullets = []
        self.current_input = ""  # ローマ字の累積入力

    def handle_typing_input(self, char, enemies, explosions, add_score_callback):
        self.current_input += char

        matched_enemy = None
        for enemy in enemies:
            if enemy.romaji.startswith(self.current_input):
                matched_enemy = enemy
                enemy.input_index = len(self.current_input)
                break

        if matched_enemy:
            if self.current_input == matched_enemy.romaji:
                explosions.append(Explosion(matched_enemy.rect.centerx, matched_enemy.rect.centery))
                add_score_callback(matched_enemy.points)
                enemies.remove(matched_enemy)
                self.current_input = ''
                if self.shot_sound:
                    self.shot_sound.play()
                
        else:
            self.current_input = ''
            for enemy in enemies:
                enemy.input_index = 0

    def update(self, enemies):
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(screen)

    def create_beam(self, x, y):
        return Bullet(x, y)
    

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        # 画面外に出ないよう制限
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:  # 画面サイズに合わせて調整
            self.rect.right = 800


    # def move(self, dx, dy):
    #     self.rect.x += dx
    #     self.rect.y += dy
    #     self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
    #     self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))