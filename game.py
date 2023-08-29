import pygame

from scenes import Partie, Scene


class Fenetre:
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
        # if isinstance(self.scene_courante, Fin):
        #     self.scene_courante = Partie()
        # elif isinstance(self.scene_courante, Partie) and self.scene_courante.perdu:
        #     self.scene_courante = Fin(False)
        # elif isinstance(self.scene_courante, Partie) and self.scene_courante.gagne:
        #     self.scene_courante = Fin(True)

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
    jeu = Fenetre()
    jeu.jouer()
    pygame.quit()