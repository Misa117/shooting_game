import pygame
import json
from datetime import datetime
from game import Game
import os

pygame.mixer.init()
pygame.mixer.init()  # ミキサーの初期化（必須）
shot_sound = pygame.mixer.Sound("assets/sounds/shot.wav")
explosion_sound = pygame.mixer.Sound("assets/sounds/shotlong.wav")
type_sound = pygame.mixer.Sound("assets/sounds/type.wav")
pygame.mixer.music.load("assets/sounds/bgm.mp3")  # 任意のBGMファイル
pygame.mixer.music.set_volume(0.5)  # 音量（0.0～1.0）
pygame.mixer.music.play(-1)  # -1 = 無限ループで再生

SCORES_FILE = "scores.json"
FONT_PATH = os.path.join(os.path.dirname(__file__), "k8x12.ttf")


def save_score(name, score):
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            scores = json.load(f)
    except FileNotFoundError:
        scores = []

    existing = next((s for s in scores if s["name"] == name), None)

    if existing:
        if score > existing["score"]:
            existing["score"] = score
            existing["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        scores.append({
            "name": name,
            "score": score,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    scores = sorted(scores, key=lambda x: x["score"], reverse=True)

    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)

def load_scores():
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def draw_text(screen, text, x, y, font, color=(255, 255, 255), center=False):
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("シューティングゲーム")
    clock = pygame.time.Clock()

    # フォント読み込み
    if os.path.exists(FONT_PATH):
        font = pygame.font.Font(FONT_PATH, 35)
    else:
        print("⚠ フォントが見つかりません。k8x12.ttf をプロジェクトフォルダに置いてください。")
        return

    # 効果音の読み込み
    type_sound = pygame.mixer.Sound("assets/sounds/type.wav")

    state = 'home'
    input_name = ""
    game = None
    score = 0

    while True:
        dt = clock.tick(60)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if state == 'home':
                    if event.key == pygame.K_BACKSPACE:
                        input_name = input_name[:-1]
                    elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        if input_name.strip() != "":
                            type_sound.play()
                            state = 'rules'
                    else:
                        if len(input_name) < 10:
                            input_name += event.unicode
                elif state == 'rules':
                    if event.key == pygame.K_SPACE:
                        type_sound.play()
                        game = Game(screen)
                        state = 'playing'
                elif state == 'result':
                    if event.key == pygame.K_SPACE:
                        type_sound.play()
                        state = 'home'
                        input_name = ""
                        score = 0
                        game = None


        screen.fill((0, 0, 0))

        if state == 'home':
            player_img = pygame.image.load("assets/images/player.png").convert_alpha()
            player_img = pygame.transform.scale(player_img, (150, 150))
            img_rect = player_img.get_rect()
            img_rect.bottomright = (screen.get_width() - 20, screen.get_height() - 20)
            screen.blit(player_img, img_rect)

            draw_text(screen, "名前を入力してください:", 50, 100, font)
            draw_text(screen, input_name + "|", 50, 150, font)
            draw_text(screen, "EnterまたはSpaceで決定", 50, 200, font)

        elif state == 'rules':
            title_font = pygame.font.Font(FONT_PATH, 28)
            draw_text(screen, "★ ルール説明 ★", screen.get_width() // 2, 40, title_font, (255, 255, 255), center=True)

            rules = [
                "敵に表示されたひらがな3文字を正確にタイプして撃破！",
                "スコア50以上で10秒間のフィーバーモード突入！",
                "フィーバー中は←→キーで移動、自動ビーム攻撃！",
                "20体逃すとゲームオーバーになります。",
            ]

            for i, line in enumerate(rules):
                draw_text(screen, line, screen.get_width() // 2, 100 + i * 40, font, (255, 255, 255), center=True)

            draw_text(screen, "スペースキーでゲーム開始！", screen.get_width() // 2, 300, font, (255, 255, 0), center=True)

        elif state == 'playing':
            game.handle_events(events)
            game.update(dt)
            game.draw()

            if game.state == 'gameover':
                score = game.score
                save_score(input_name, score)
                state = 'result'

        elif state == 'result':
            draw_text(screen, f"ゲーム終了！ {input_name} さんの今回の撃退point…　（{score}）", 50, 50, font)
            draw_text(screen, "みんなの成績:", 50, 100, font)
            scores = load_scores()
            for i, s in enumerate(scores[:10]):
                text = f"{i+1}. {s['name']} - {s['score']}P ({s['date']})"
                draw_text(screen, text, 50, 130 + i * 30, font)
            draw_text(screen, "Spaceキーでホームに戻る", 50, 500, font)

        pygame.display.flip()


if __name__ == "__main__":
    main()
