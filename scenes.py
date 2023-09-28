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
        pygame.time.set_timer(self.new_bear, 400)

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
        for _ in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            for ours in self.ours:
                if ours.touche_souris():
                    self.son_clic.play()
                    self.score.ajoute_points(1)
                    ours.kill()

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

    def __init__(self, score: int) -> None:
        largeur, hauteur = pygame.display.get_window_size()

        self.decors: Objet = Objet(
            "images/fond.png", largeur // 2, hauteur // 2, largeur
        )

        record: int = 0
        with open("record.txt", "r", encoding="utf-8") as fichier:
            record: int = int(fichier.read())

        if score > record:
            record = score
            self.message_fin: Texte = Texte("Nouveau record", "font/Avdira.otf", 100)
            with open("record.txt", "w", encoding="utf-8") as fichier:
                fichier.write(str(score))
        else:
            self.message_fin: Texte = Texte("Perdu ...", "font/Avdira.otf", 100)

        self.texte_score: Texte = Texte(f"Score : {score}", "font/Avdira.otf", 50)
        self.texte_record: Texte = Texte(f"Record : {record}", "font/Avdira.otf", 50)

        self.son_fin: pygame.mixer.Sound = pygame.mixer.Sound("sounds/Crash Cymbal.wav")
        self.son_fin.set_volume(0.25)
        self.son_fin.play()

        self.bouton_rejouer: Bouton = Bouton(Texte("Rejouer", "font/Avdira.otf", 50))
        self.son_bouton: pygame.mixer.Sound = pygame.mixer.Sound("sounds/pop.wav")
        self.son_bouton.set_volume(0.25)
        self.next: bool = False

    def affiche_scene(self) -> None:
        """Affiche la scène de fin"""
        fenetre = pygame.display.get_surface()
        largeur, _ = pygame.display.get_window_size()

        fenetre.blit(self.decors.image, self.decors.rect)
        couleur_score = pygame.Color(28, 42, 73)
        couleur_message = pygame.Color(255, 255, 255)
        self.texte_score.draw(couleur_score, largeur // 2, 100)
        self.texte_record.draw(couleur_score, largeur // 2, 170)
        self.message_fin.draw(couleur_message, largeur // 2, 350)
        couleur_texte = (
            pygame.Color(225, 238, 248)
            if self.bouton_rejouer.touche_souris()
            else pygame.Color(240, 240, 240)
        )
        couleur_fond = (
            pygame.Color(28, 64, 100)
            if self.bouton_rejouer.touche_souris()
            else pygame.Color(28, 42, 73)
        )
        self.bouton_rejouer.draw(couleur_texte, couleur_fond, largeur // 2, 550)

    def joue_tour(self) -> None:
        """Rien"""
        for _ in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            if self.bouton_rejouer.touche_souris():
                self.son_bouton.play()
                self.next = True

    def passe_suivant(self) -> bool:
        """Vérifie si le bouton rejouer est cliqué"""
        return self.next
