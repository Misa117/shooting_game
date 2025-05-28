import pygame
import random
import sys
import os
from star import Star
from explosion import Explosion
from player import Player
from enemy import Enemy

K8X12_FONT_PATH = os.path.join(os.path.dirname(__file__), "k8x12.ttf")
NOTO_FONT_PATH = os.path.join(os.path.dirname(__file__), "NotoSansJP.ttf")

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(K8X12_FONT_PATH, 30)
        self.noto_font = pygame.font.Font(NOTO_FONT_PATH, 34)
        self.noto_font.set_bold(True)


        self.score = 0
        self.player = Player(375, 500)
        self.enemies = []
        self.bullets = []
        self.explosions = []
        self.state = 'home'
        self.down_count = 0
        self.last_shot_time = 0  
        self.fever_mode = False
        self.fever_start_time = None
        self.fever_duration = 10000  # ミリ秒（10秒）
        self.saved_player_pos = None
        self.fever_used = False  # フィーバー再発動制限用フラグ
        self.stars = [Star(screen.get_width(), screen.get_height()) for _ in range(100)]
        self.spawn_timer = 0  # 敵スポーンのタイマー
        self.game_over = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # 安全に終了

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if self.state == 'playing' and 700 <= x <= 770 and 10 <= y <= 40:
                    # プレイ中に戻るボタンを押すとホーム画面へ
                    self.state = 'home'
                    self.enemies.clear()
                    self.score = 0
                    self.down_count = 0
                    self.fever_mode = False
                    self.fever_used = False  # ゲーム中止でフィーバー再発動可能に
                    self.player.current_input = ''

            elif event.type == pygame.KEYDOWN:
                if self.state == 'home':
                    # ホーム画面でスペースを押すとゲーム開始
                    if event.key == pygame.K_SPACE:
                        self.state = 'playing'
                        self.score = 0
                        self.enemies.clear()
                        self.down_count = 0
                        self.fever_mode = False
                        self.fever_used = False  # ゲーム開始時にリセット
                        self.player.current_input = ''

                elif self.state == 'playing':
                    if not self.fever_mode:
                        if event.key == pygame.K_BACKSPACE:
                            self.player.current_input = self.player.current_input[:-1]
                            for enemy in self.enemies:
                                enemy.input_index = 0
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                            self.player.current_input = ''
                            for enemy in self.enemies:
                                enemy.input_index = 0
                        else:
                            char = event.unicode
                            if char:
                                self.player.handle_typing_input(char, self.enemies, self.explosions, self.add_score)

                    else:
                        # フィーバーモード中は十字キーで移動可能
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_LEFT]:
                            self.player.move(-self.player.speed, 0)
                        if keys[pygame.K_RIGHT]:
                            self.player.move(self.player.speed, 0)


    def update(self, dt):
        if self.state == 'playing':
            for star in self.stars:
                star.update()

            # ★ 長押しによるプレイヤー移動（フィーバー中のみ）
            if self.fever_mode:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.player.move(-self.player.speed, 0)
                if keys[pygame.K_RIGHT]:
                    self.player.move(self.player.speed, 0)

            # 敵スポーンのタイマー更新
            self.spawn_timer += dt
            # if self.spawn_timer > 2000:  # 2秒ごとに敵を出現させる
            #     enemy_type = random.choice([1, 2, 3, 4])
            #     self.enemies.append(Enemy(enemy_type, self.screen.get_width(), self.screen.get_height()))
            #     self.spawn_timer = 0
            # スコアに応じて敵の出現間隔を短縮（最小500ms）
            spawn_interval = max(500, 2000 - self.score * 10)

            if self.spawn_timer > spawn_interval:
                enemy_type = random.choice([1, 2, 3, 4])
                self.enemies.append(Enemy(enemy_type, self.screen.get_width(), self.screen.get_height()))
                self.spawn_timer = 0

            # 敵の更新処理
            for enemy in self.enemies[:]:
                enemy.update(2)
                if enemy.rect.top > 600:
                    self.enemies.remove(enemy)
                    self.down_count += 1
                    if self.down_count >= 20:
                        self.state = 'gameover'
                        self.game_over = True
                        self.fever_used = False  # ゲームオーバー時にフィーバー再発動可能に

            # プレイヤーの更新
            self.player.update(self.enemies)

            # フィーバーモード判定・ビーム発射
            if self.score >= 50 and not self.fever_mode and not self.fever_used:
                self.fever_mode = True
                self.fever_start_time = pygame.time.get_ticks()
                self.fever_used = True  # 一度使ったら再発動禁止

                self.saved_player_pos = self.player.rect.center  # プレイヤーの位置を保存
                self.player.rect.center = (400, 550)  # 画面下部に移動（任意）

            if self.fever_mode:
                current_time = pygame.time.get_ticks()

                # フィーバー継続判定
                if current_time - self.fever_start_time <= self.fever_duration:
                    keys = pygame.key.get_pressed()
                    if current_time - self.last_shot_time >= 200:
                        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                            bullet_x = self.player.rect.centerx
                            bullet_y = self.player.rect.top
                            self.player.bullets.append(self.player.create_beam(bullet_x, bullet_y))
                            self.last_shot_time = current_time
                else:
                    self.fever_mode = False
                    self.player.rect.topleft = (375, 500)


            # 弾と敵の当たり判定
            for bullet in self.player.bullets[:]:
                for enemy in self.enemies[:]:
                    if bullet.rect.colliderect(enemy.rect):
                        if bullet.key is None:
                            self.score += enemy.points
                            self.explosions.append(Explosion(enemy.rect.centerx, enemy.rect.centery))
                            self.enemies.remove(enemy)
                            self.player.bullets.remove(bullet)
                            break
                        elif 0 <= enemy.input_index < len(enemy.text):
                            expected_char = enemy.romaji[enemy.input_index].lower()
                            if bullet.key == expected_char:
                                enemy.input_index += 1
                                if enemy.input_index >= len(enemy.romaji):
                                    self.score += enemy.points
                                    self.explosions.append(Explosion(enemy.rect.centerx, enemy.rect.centery))
                                    self.enemies.remove(enemy)
                                self.player.bullets.remove(bullet)
                                break
                        else:
                            self.player.bullets.remove(bullet)
                            break

            # 爆発アニメーション更新
            for explosion in self.explosions[:]:
                if not explosion.update():
                    self.explosions.remove(explosion)

    def draw(self):
        self.screen.fill((0, 0, 0))  # 通常時は黒

            # フィーバーモード中は星の速度を8倍に
        speed_mult = 8 if self.fever_mode else 1

        for star in self.stars:
            star.update(speed_mult)
            star.draw(self.screen)

        for star in self.stars:
            star.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen, self.font)

        self.player.draw(self.screen)

        for bullet in self.player.bullets:
            bullet.draw(self.screen)

        for explosion in self.explosions:
            explosion.draw(self.screen)

        # スコア表示（k8x12.ttf）
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 0))
        self.screen.blit(score_text, (10, 10))

        # ホームテキスト表示（k8x12.ttf）
        home_text = self.font.render("ホーム", True, (0, 255, 255))
        self.screen.blit(home_text, (700, 10))

        # ★ 白背景の矩形を画面幅いっぱいに描画（高さはテキストの高さに合わせて少し余裕を持たせる）
        background_height = 50
        background_rect = pygame.Rect(0, self.screen.get_height() - background_height, self.screen.get_width(), background_height)
        pygame.draw.rect(self.screen, (255, 255, 255), background_rect)

        # ★ テキストを左寄せで表示（左端に10pxの余白、縦は白背景の中央あたり）
        input_text = f"入力文字：{self.player.current_input}"
        input_surface = self.noto_font.render(input_text, True, (0, 0, 0))  # 黒文字、背景なし
        input_rect = input_surface.get_rect()
        input_rect.topleft = (10, self.screen.get_height() - background_height + (background_height - input_surface.get_height()) // 2)
        self.screen.blit(input_surface, input_rect)

        # ★ 「落ちた数」カウントを白背景の上あたり、右下に配置
        down_text = self.font.render(f"落ちた数: {self.down_count}/20", True, (255, 100, 100))
        down_rect = down_text.get_rect()
        # 画面右端から10px内側、白背景の上（10px上）に配置
        down_rect.bottomright = (self.screen.get_width() - 10, self.screen.get_height() - background_height - 10)
        self.screen.blit(down_text, down_rect)

        # フィーバーモードか通常入力中かを表示（k8x12.ttf）
        if self.fever_mode:
            # 点滅のオンオフ（500msごとに切り替え）
            if self.fever_mode:
                if (pygame.time.get_ticks() // 500) % 2 == 0:  # 0.5秒ごとに点滅
                    fever_text = self.font.render("フィーバーモード！ 十字キーでビーム発射！", True, (255, 0, 0))
                    fever_rect = fever_text.get_rect(center=(self.screen.get_width() // 2, 120))
                    self.screen.blit(fever_text, fever_rect)
            else:
                input_status_text = self.font.render("エイリアンを倒せ…！", True, (255, 255, 255))
                input_status_rect = input_status_text.get_rect(center=(self.screen.get_width() // 2, 80))
                self.screen.blit(input_status_text, input_status_rect)

        # # 宇宙人が落ちていった数カウント（k8x12.ttf）
        # down_text = self.font.render(f"落ちた数: {self.down_count}/20", True, (255, 100, 100))
        # down_rect = down_text.get_rect(bottomright=(self.screen.get_width() - 10, self.screen.get_height() - 10))
        # self.screen.blit(down_text, down_rect)

        # ルール説明やゲームオーバー画面（k8x12.ttf）
        if self.state == 'home':
            lines = [
                "【ルール説明】",
                "敵に表示されたひらがな3文字を正確にタイピングすると撃破！",
                "スコア50以上で10秒間のフィーバーモードに突入！",
                "フィーバー中は←→キーで移動、敵を自動でビーム攻撃！",
                "20体逃すとゲームオーバーになります。",
                "スペースキーでゲーム開始！"
            ]
            for i, line in enumerate(lines):
                text_surface = self.font.render(line, True, (255, 255, 255))
                self.screen.blit(text_surface, (50, 100 + i * 30))

        elif self.state == 'gameover':
            over_text = self.font.render("GAME OVER", True, (255, 0, 0))
            self.screen.blit(over_text, (
                self.screen.get_width() // 2 - over_text.get_width() // 2,
                self.screen.get_height() // 2 - over_text.get_height() // 2
            ))

            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 0))
            self.screen.blit(score_text, (
                self.screen.get_width() // 2 - score_text.get_width() // 2,
                self.screen.get_height() // 2 - score_text.get_height() // 2 + 30
            ))

    def add_score(self, points):
        self.score += points
