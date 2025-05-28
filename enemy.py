import pygame
import os
import random
from romaji_map import kana_to_romaji

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Enemy:
    HIRAGANA_WORDS_2 = ['いぬ', 'ねこ', 'りす', 'あり', 'くき', 'さけ', 'くま', 'はな', 'たこ', 'みず', 'かぜ', 'そら']
    HIRAGANA_WORDS_3 = [
        'うどん', 'ひらめ', 'あずき', 'こたつ', 'ごりら', 'いちご', 'さくら', 'すいか', 'りゅう', 'みかん', 'らっこ',
        'たまご', 'はなび', 'まくら', 'らっぱ', 'わらび', 'あさひ', 'くるま'
    ]

    def __init__(self, enemy_type, screen_width, screen_height):
        self.type = enemy_type
        self.screen_width = screen_width
        self.screen_height = screen_height

        # 表示用のひらがな
        if enemy_type in [1, 2]:
            self.text = random.choice(Enemy.HIRAGANA_WORDS_2)
            self.points = 2
        elif enemy_type in [3, 4]:
            self.text = random.choice(Enemy.HIRAGANA_WORDS_3)
            self.points = 5
        else:
            self.text = "？？"
            self.points = 1

        # 入力＆判定用のローマ字に変換
        self.romaji = kana_to_romaji(self.text)

        # タイピング進捗管理
        self.input_index = 0

        # 画像と初期位置設定
        image_path = os.path.join(BASE_DIR, "assets", "images", f"enemy{enemy_type}.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, max(0, screen_width - self.rect.width))
        self.rect.y = -self.rect.height

    def draw(self, screen, font):
        screen.blit(self.image, self.rect)

        # 文字の縁取り描画
        center = self.rect.center
        text_color = (255, 255, 0)
        outline_color = (0, 0, 0)
        outline_thickness = 2
        offsets = [(-outline_thickness, -outline_thickness), (-outline_thickness, 0),
                   (-outline_thickness, outline_thickness), (0, -outline_thickness),
                   (0, outline_thickness), (outline_thickness, -outline_thickness),
                   (outline_thickness, 0), (outline_thickness, outline_thickness)]

        for ox, oy in offsets:
            outline_surf = font.render(self.text, True, outline_color)
            outline_rect = outline_surf.get_rect(center=(center[0] + ox, center[1] + oy))
            screen.blit(outline_surf, outline_rect)

        # 本体のテキスト
        text_surf = font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=center)
        screen.blit(text_surf, text_rect)

    def update(self, speed):
        self.rect.y += speed
