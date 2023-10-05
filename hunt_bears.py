"""Jeu Hunt the Bears
- les ours apparaissent au hasard dans la forêt
- clique sur les ours pour gagner des points
- tu n'as que 60 secondes pour jouer"""

import pygame

from game import Game, Stage


class HuntBears:
    """Jeu"""

    def __init__(self) -> None:
        pygame.init()

        # fenêtre
        self.width: int = 1080
        self.height: int = 720
        self.screen: pygame.Surface = pygame.display.set_mode(
            (self.width, self.height)
        )
        pygame.display.set_caption("Hunt the bears")
        pygame.display.set_icon(pygame.image.load("images/bear1.png"))

        # état
        self.game: Game = Game(self.width, self.height)
        self.clock: pygame.time.Clock = pygame.time.Clock()

    def run(self) -> None:
        """Lance le jeu"""
        while True:
            if self.game.stage == Stage.TERMINATE:
                self.game = Game(self.width, self.height)

            if self.game.stage == Stage.RUNNING:
                self.game.run_game()
                self.game.draw_game(self.screen)

            if self.game.stage == Stage.END:
                self.game.run_end()
                self.game.draw_end(self.screen)

            # quitter
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    return

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    jeu = HuntBears()
    jeu.run()
    pygame.quit()
