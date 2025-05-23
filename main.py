import pygame
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("シューティングゲーム")
    clock = pygame.time.Clock()
    game = Game(screen)

    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(60)

        # ゲームオーバーなら少し待ってから終了
        if game.game_over:
            pygame.time.wait(2000)  # 2秒待つ
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
