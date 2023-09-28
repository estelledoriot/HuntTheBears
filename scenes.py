"""
Gestion des scènes du jeu
"""

from typing import Protocol
from random import randint

import pygame

from objet import Objet
from ours import Ours
from texte import Texte
from countdown import Countdown
from bouton import Bouton
from score import Score


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
        self.new_bear: int = pygame.USEREVENT + 1
        pygame.time.set_timer(self.new_bear, 500)

        self.countdown: Countdown = Countdown(60)
        self.score: Score = Score()

        self.son_clic: pygame.mixer.Sound = pygame.mixer.Sound("sounds/crunch.wav")
        self.son_clic.set_volume(0.125)

    def affiche_scene(self) -> None:
        """Affiche les éléments du jeu"""
        fenetre = pygame.display.get_surface()

        fenetre.blit(self.decors.image, self.decors.rect)
        self.ours.draw(fenetre)
        fenetre.blit(self.sapins.image, self.sapins.rect)
        self.countdown.draw()
        self.score.draw()

    def joue_tour(self) -> None:
        """Joue un tour du jeu"""

        # crée un ours supplémentaire
        for event in pygame.event.get(self.new_bear):
            if event.type == self.new_bear:
                self.ours.add(Ours(randint(80, 100)))

        # ajoute un point si un ours est cliqué
        if any(ours.est_clique() for ours in self.ours):
            self.son_clic.play()
            self.score.ajoute_points(1)

        # supprime les ours au bout d'un certain temps
        self.ours.update()

        # mise à jour des compteurs
        self.countdown.update()
        self.score.update()

    def passe_suivant(self) -> bool:
        """Renvoie si la partie est terminée"""
        return self.countdown.temps_restant <= 0


class Fin:
    """Scène de fin"""

    def __init__(self) -> None:
        victoire = False
        largeur, hauteur = pygame.display.get_window_size()

        self.decors: Objet = Objet("images/jungle.png", largeur // 2, hauteur, largeur)
        self.message_fin: Texte = (
            Texte("Gagné !", "font/Avdira.otf", 100)
            if victoire
            else Texte("Perdu ...", "font/Avdira.otf", 100)
        )
        self.bouton_rejouer: Bouton = Bouton(Texte("Rejouer", "font/Avdira.otf", 50))

    def affiche_scene(self) -> None:
        """Affiche la scène de fin"""
        fenetre = pygame.display.get_surface()
        largeur, _ = pygame.display.get_window_size()

        fenetre.blit(self.decors.image, self.decors.rect)
        couleur_message = pygame.Color(255, 255, 255)
        self.message_fin.draw(couleur_message, largeur // 2, 150)
        couleur_texte = (
            pygame.Color(101, 172, 171)
            if self.bouton_rejouer.touche_souris()
            else pygame.Color(240, 240, 240)
        )
        couleur_fond = (
            pygame.Color(80, 80, 80)
            if self.bouton_rejouer.touche_souris()
            else pygame.Color(50, 50, 50)
        )
        self.bouton_rejouer.draw(couleur_texte, couleur_fond, largeur // 2, 400)

    def joue_tour(self) -> None:
        """Rien"""

    def passe_suivant(self) -> bool:
        """Vérifie si le bouton rejouer est cliqué"""
        return self.bouton_rejouer.est_clique()
