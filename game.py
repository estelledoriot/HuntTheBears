"""Jeu Hunt the Bears
- les ours apparaissent au hasard dans la forêt
- clique sur les ours pour gagner des points
- tu n'as que 60 secondes pour jouer"""

import pygame

from scenes import Partie, Scene, Fin


class Jeu:
    """Jeu"""

    def __init__(self) -> None:
        pygame.init()

        # fenêtre
        self.largeur: int = 1080
        self.hauteur: int = 720
        self.fenetre: pygame.Surface = pygame.display.set_mode(
            (self.largeur, self.hauteur)
        )
        pygame.display.set_caption("Hunt the bears")
        pygame.display.set_icon(pygame.image.load("images/bear1.png"))

        # état
        self.scene_courante: Scene = Partie()
        self.clock: pygame.time.Clock = pygame.time.Clock()

    def scene_suivante(self) -> None:
        """Passe à la scène suivante"""
        if isinstance(self.scene_courante, Fin):
            self.scene_courante = Partie()
        elif isinstance(self.scene_courante, Partie):
            self.scene_courante = Fin(self.scene_courante.score.score)

    def jouer(self) -> None:
        """Lance le jeu"""
        while True:
            self.scene_courante.joue_tour()
            if self.scene_courante.passe_suivant():
                self.scene_suivante()

            # quitter
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    return

            # affichage
            self.scene_courante.affiche_scene()
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    jeu = Jeu()
    jeu.jouer()
    pygame.quit()
