"""
Gestion des scènes du jeu
"""

from enum import Enum
from random import randint

import pygame

from object import Object
from bear import Bear
from text import Text
from countdown import Countdown
from button import Button
from score import Score
from filled_surface import FilledSurface


Stage = Enum("Stage", ["RUNNING", "END", "TERMINATE"])


class Game:
    """Une partie de hunt the bears"""

    def __init__(self, width: int, height: int) -> None:
        # décors
        self.background: Object = Object(
            "images/fond.png", (width // 2, height // 2), width
        )
        self.trees: Object = Object(
            "images/sapins.png", (width // 2, height * 11 // 16), width
        )
        self.opaque_surface: FilledSurface = FilledSurface(
            pygame.Color(200, 222, 237, 200)
        )

        # game elements
        self.bears: pygame.sprite.Group = pygame.sprite.Group()
        self.countdown: Countdown = Countdown(60, (width - 80, 60))
        self.score: Score = Score((80, 60))
        self.game_elements: pygame.sprite.Group = pygame.sprite.Group()
        self.game_elements.add(
            self.background,
            self.countdown,
            self.score,
            self.bears,
            self.trees,
        )

        # end elements
        self.record: int = 0
        with open("record.txt", "r", encoding="utf-8") as fichier:
            self.record = int(fichier.read())
        self.score_surface: Text = Text(
            f"Score : {self.score.score}",
            50,
            pygame.Color(28, 42, 73),
            (width // 2, 100),
        )
        self.record_surface: Text = Text(
            f"Record : {self.record}",
            50,
            pygame.Color(28, 42, 73),
            (width // 2, 170),
        )
        self.end_message: Text = Text(
            "", 100, pygame.Color(255, 255, 255), (width // 2, 350)
        )
        self.restart_button: Button = Button(
            "Rejouer", (250, 80), (width // 2, 550)
        )
        self.end_elements: pygame.sprite.Group = pygame.sprite.Group()
        self.end_elements.add(
            self.background,
            self.opaque_surface,
            self.score_surface,
            self.record_surface,
            self.end_message,
            self.restart_button,
        )

        # events
        self.new_bear_event: int = pygame.USEREVENT + 1
        pygame.time.set_timer(self.new_bear_event, 400)

        # sons
        self.clic_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            "sounds/crunch.wav"
        )
        self.clic_sound.set_volume(0.125)
        self.end_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            "sounds/Crash Cymbal.wav"
        )
        self.end_sound.set_volume(0.25)
        self.button_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            "sounds/pop.wav"
        )
        self.button_sound.set_volume(0.25)

        # stage
        self.stage: Stage = Stage.RUNNING

    @property
    def won(self) -> bool:
        """Vérifie si la partie est gagnée (le personnage touche la pokeball)"""
        return self.countdown.time_finished and self.score.score > self.record

    @property
    def lost(self) -> bool:
        """Vérifie si la partie est perdue (le temps est écoulé)"""
        return self.countdown.time_finished and self.score.score <= self.record

    def run_game(self) -> None:
        """Fait tourner le jeu"""
        # crée un ours supplémentaire
        for _ in pygame.event.get(self.new_bear_event):
            self.bears.add(Bear(randint(80, 100)))

        # ajoute un point si un ours est cliqué
        for _ in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            for ours in self.bears:
                if ours.touch_mouse():
                    self.clic_sound.play()
                    self.score.add_points(1)
                    ours.kill()

        # mise à jour des éléments du jeu
        self.game_elements.update()
        self.game_elements.empty()
        self.game_elements.add(
            self.background,
            self.countdown,
            self.score,
            self.bears,
            self.trees,
        )

        # fin du jeu
        if self.won:
            self.record = self.score.score
            with open("record.txt", "w", encoding="utf-8") as fichier:
                fichier.write(str(self.record))
        if self.won or self.lost:
            self.stage = Stage.END
            self.end_sound.play()
            self.end_message.update_text(
                "Nouveau record" if self.won else "Perdu ..."
            )
            self.score_surface.update_text(f"score: {self.score.score}")
            self.record_surface.update_text(f"record: {self.record}")

    def draw_game(self, screen: pygame.Surface) -> None:
        """Affiche les éléments du jeu"""
        self.game_elements.draw(screen)

    def run_end(self) -> None:
        """Fait tourner l'écran de fin"""
        # mise à jour des éléments de l'écran de fin
        self.end_elements.update()

        # clic sur le bouton pour commencer une nouvelle partie
        for _ in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            if self.restart_button.touch_mouse():
                self.button_sound.play()
                self.stage = Stage.TERMINATE

    def draw_end(self, screen: pygame.Surface) -> None:
        """Affiche les éléments de l'écran de fin"""
        self.end_elements.draw(screen)
