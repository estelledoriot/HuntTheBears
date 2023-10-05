"""
classe Object
"""


import pygame


class Object(pygame.sprite.Sprite):
    """Image de fond
    filename: fichier contenant l'image
    position: position initiale de l'objet
    width: largeur de l'objet
    """

    def __init__(
        self,
        filename: str,
        position: tuple[int, int],
        width: int,
    ) -> None:
        super().__init__()

        self.image: pygame.Surface = pygame.image.load(
            filename
        ).convert_alpha()
        self.image = pygame.transform.scale_by(
            self.image, width / self.image.get_width()
        )

        self.rect: pygame.Rect = self.image.get_rect(center=position)
