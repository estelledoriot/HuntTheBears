"""
classe Ours
"""

from random import randint

import pygame


class Ours(pygame.sprite.Sprite):
    """Ours sur lesquels il faut cliquer
    taille: taille du personnage
    """

    def __init__(self, taille: int) -> None:
        super().__init__()
        largeur, hauteur = pygame.display.get_window_size()

        self.image: pygame.Surface = pygame.image.load(
            f"images/bear{randint(1, 3)}.png"
        ).convert_alpha()
        self.image = pygame.transform.scale_by(
            self.image, taille / self.image.get_width()
        )

        self.rect: pygame.Rect = self.image.get_rect(
            center=(
                randint(
                    self.image.get_width() // 2, largeur - self.image.get_width() // 2
                ),
                randint(hauteur // 2, hauteur - self.image.get_height() // 2),
            )
        )

        self.start_time: int = pygame.time.get_ticks()

    def touche_souris(self) -> bool:
        """Détermine si on clique sur le bouton"""
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def update(self) -> None:
        """Disparition de l'ours"""
        if pygame.time.get_ticks() - self.start_time > 800:
            self.kill()
