"""
Gestion des scènes du jeu
"""

from typing import Protocol

import pygame

from elements import Objet, Ours

# from texte import Bouton, Message


class Scene(Protocol):
    """Scène du jeu"""

    def affiche_scene(self) -> None:
        ...

    def joue_tour(self) -> None:
        ...

    def passe_suivant(self) -> bool:
        ...


class Partie:
    """Partie de Hunt the bears"""

    def __init__(self) -> None:
        largeur, hauteur = pygame.display.get_window_size()

        self.decors: Objet = Objet(
            "images/fond.png", largeur // 2, hauteur // 2, largeur
        )
        self.sapins: Objet = Objet(
            "images/sapins.png", largeur // 2, hauteur * 11 // 16, largeur
        )
        self.ours: pygame.sprite.Group = pygame.sprite.Group()
        for _ in range(3):
            self.ours.add(Ours(100))
        self.pilliers: list[pygame.Rect] = []

        self.points: int = 0
        # self.temps: int = 60

    def affiche_scene(self) -> None:
        """Affiche les éléments du jeu"""
        fenetre = pygame.display.get_surface()

        fenetre.blit(self.decors.image, self.decors.rect)
        self.ours.draw(fenetre)
        fenetre.blit(self.sapins.image, self.sapins.rect)

    def joue_tour(self) -> None:
        """Joue un tour du jeu"""
        self.ours.update()

    def passe_suivant(self) -> bool:
        """Renvoie si la partie est terminée"""
        return False


# class Fin:
#     """Scène de fin"""

#     def __init__(self, victoire: bool) -> None:
#         largeur, hauteur = pygame.display.get_window_size()

#         self.decors: Objet = Objet("images/jungle.png", largeur // 2, hauteur, largeur)
#         self.message_fin: Message = (
#             Message("Gagné !", "font/Avdira.otf", 100)
#             if victoire
#             else Message("Perdu ...", "font/Avdira.otf", 100)
#         )
#         self.bouton_rejouer: Bouton = Bouton(Message("Rejouer", "font/Avdira.otf", 50))

#     def affiche_scene(self) -> None:
#         """Affiche la scène de fin"""
#         fenetre = pygame.display.get_surface()
#         largeur, _ = pygame.display.get_window_size()

#         fenetre.blit(self.decors.image, self.decors.rect)
#         couleur_message = pygame.Color(255, 255, 255)
#         self.message_fin.affiche(couleur_message, largeur // 2, 150)
#         couleur_texte = (
#             pygame.Color(101, 172, 171)
#             if self.bouton_rejouer.touche_souris()
#             else pygame.Color(240, 240, 240)
#         )
#         couleur_fond = (
#             pygame.Color(80, 80, 80)
#             if self.bouton_rejouer.touche_souris()
#             else pygame.Color(50, 50, 50)
#         )
#         self.bouton_rejouer.affiche(couleur_texte, couleur_fond, largeur // 2, 400)

#     def joue_tour(self) -> None:
#         """Rien"""

#     def passe_suivant(self) -> bool:
#         """Vérifie si le bouton rejouer est cliqué"""
#         return self.bouton_rejouer.est_clique()
