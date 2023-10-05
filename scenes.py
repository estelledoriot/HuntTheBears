"""
Gestion des scènes du jeu
"""

from typing import Protocol
from random import randint

import pygame

from object import Object
from bear import Bear
from text import Text
from countdown import Countdown
from button import Button
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

        self.decors: Object = Object(
            "images/fond.png", (largeur // 2, hauteur // 2), largeur
        )
        self.sapins: Object = Object(
            "images/sapins.png", (largeur // 2, hauteur * 11 // 16), largeur
        )
        self.ours: pygame.sprite.Group = pygame.sprite.Group()
        self.new_bear: int = pygame.USEREVENT + 1
        pygame.time.set_timer(self.new_bear, 400)

        self.countdown: Countdown = Countdown(60, (largeur - 80, 60))
        self.score: Score = Score((80, 60))

        self.son_clic: pygame.mixer.Sound = pygame.mixer.Sound(
            "sounds/crunch.wav"
        )
        self.son_clic.set_volume(0.125)

    def affiche_scene(self) -> None:
        """Affiche les éléments du jeu"""
        fenetre = pygame.display.get_surface()

        fenetre.blit(self.decors.image, self.decors.rect)
        self.ours.draw(fenetre)
        fenetre.blit(self.sapins.image, self.sapins.rect)
        fenetre.blit(self.countdown.image, self.countdown.rect)
        fenetre.blit(self.score.image, self.score.rect)

    def joue_tour(self) -> None:
        """Joue un tour du jeu"""

        # crée un ours supplémentaire
        for event in pygame.event.get(self.new_bear):
            if event.type == self.new_bear:
                self.ours.add(Bear(randint(80, 100)))

        # ajoute un point si un ours est cliqué
        for _ in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            for ours in self.ours:
                if ours.touch_mouse():
                    self.son_clic.play()
                    self.score.add_points(1)
                    ours.kill()

        # supprime les ours au bout d'un certain temps
        self.ours.update()

        # mise à jour des compteurs
        self.countdown.update()
        self.score.update()

    def passe_suivant(self) -> bool:
        """Renvoie si la partie est terminée"""
        return self.countdown.remaining_time <= 0


class Fin:
    """Scène de fin"""

    def __init__(self, score: int) -> None:
        largeur, hauteur = pygame.display.get_window_size()

        self.decors: Object = Object(
            "images/fond.png", (largeur // 2, hauteur // 2), largeur
        )

        record: int = 0
        with open("record.txt", "r", encoding="utf-8") as fichier:
            record: int = int(fichier.read())

        if score > record:
            record = score
            self.message_fin: Text = Text(
                "Nouveau record",
                100,
                pygame.Color(255, 255, 255),
                (largeur // 2, 350),
            )
            with open("record.txt", "w", encoding="utf-8") as fichier:
                fichier.write(str(score))
        else:
            self.message_fin: Text = Text(
                "Perdu ...",
                100,
                pygame.Color(255, 255, 255),
                (largeur // 2, 350),
            )

        self.texte_score: Text = Text(
            f"Score : {score}",
            50,
            pygame.Color(28, 42, 73),
            (largeur // 2, 100),
        )
        self.texte_record: Text = Text(
            f"Record : {record}",
            50,
            pygame.Color(28, 42, 73),
            (largeur // 2, 170),
        )

        self.son_fin: pygame.mixer.Sound = pygame.mixer.Sound(
            "sounds/Crash Cymbal.wav"
        )
        self.son_fin.set_volume(0.25)
        self.son_fin.play()

        self.bouton_rejouer: Button = Button(
            "Rejouer", (250, 80), (largeur // 2, 550)
        )
        self.son_bouton: pygame.mixer.Sound = pygame.mixer.Sound(
            "sounds/pop.wav"
        )
        self.son_bouton.set_volume(0.25)
        self.next: bool = False

    def affiche_scene(self) -> None:
        """Affiche la scène de fin"""
        fenetre = pygame.display.get_surface()

        fenetre.blit(self.decors.image, self.decors.rect)
        fenetre.blit(self.message_fin.image, self.message_fin.rect)
        fenetre.blit(self.texte_score.image, self.texte_score.rect)
        fenetre.blit(self.texte_record.image, self.texte_record.rect)
        fenetre.blit(self.bouton_rejouer.image, self.bouton_rejouer.rect)

    def joue_tour(self) -> None:
        """Rien"""
        self.bouton_rejouer.update()
        for _ in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            if self.bouton_rejouer.touch_mouse():
                self.son_bouton.play()
                self.next = True

    def passe_suivant(self) -> bool:
        """Vérifie si le bouton rejouer est cliqué"""
        return self.next
