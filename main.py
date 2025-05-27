import pygame
import json
from datetime import datetime
from game import Game
import os

SCORES_FILE = "scores.json"
FONT_PATH = "C:/Windows/Fonts/meiryo.ttc"  # 日本語対応フォントパス

def save_score(name, score):
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            scores = json.load(f)
    except FileNotFoundError:
        scores = []

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

def draw_text(screen, text, x, y, font, color=(255, 255, 255)):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("シューティングゲーム")
    clock = pygame.time.Clock()

    # メイリオなど日本語フォントを指定（存在しない場合は置き換えてください）
    if os.path.exists(FONT_PATH):
        font = pygame.font.Font(FONT_PATH, 32)
    else:
        print("⚠ 日本語フォントが見つかりません。msgothic.ttc など別のフォントを指定してください。")
        return

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
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if input_name.strip() != "":
                            state = 'rules'
                    else:
                        if len(input_name) < 10:
                            input_name += event.unicode
                elif state == 'rules':
                    if event.key == pygame.K_SPACE:
                        game = Game(screen)
                        state = 'playing'
                elif state == 'result':
                    if event.key == pygame.K_SPACE:
                        state = 'home'
                        input_name = ""
                        score = 0
                        game = None

        screen.fill((0, 0, 0))

        if state == 'home':
            draw_text(screen, "名前を入力してください:", 50, 100, font)
            draw_text(screen, input_name + "|", 50, 150, font)
            draw_text(screen, "EnterまたはSpaceで決定", 50, 200, font)

        elif state == 'rules':
            draw_text(screen, "ルール説明：タイピングで敵を倒そう！", 50, 100, font)
            draw_text(screen, "Spaceキーでゲームスタート", 50, 150, font)

        elif state == 'playing':
            game.handle_events(events)
            game.update(dt)
            game.draw()

            if game.state == 'gameover':
                score = game.score
                save_score(input_name, score)
                state = 'result'

        elif state == 'result':
            draw_text(screen, f"ゲーム終了！ {input_name} さんのスコア: {score}", 50, 50, font)

            draw_text(screen, "みんなの成績:", 50, 100, font)
            scores = load_scores()
            for i, s in enumerate(scores[:10]):
                text = f"{i+1}. {s['name']} - {s['score']}点 ({s['date']})"
                draw_text(screen, text, 50, 130 + i*30, font)

            draw_text(screen, "Spaceキーでホームに戻る", 50, 500, font)

        pygame.display.flip()

if __name__ == "__main__":
    main()
