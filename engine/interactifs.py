# tout ce que le player peut interagir avec pour Platformer
import pygame as pg
from random import choice
from engine.constants import *


class Arrive(pg.sprite.Sprite):
    def __init__(self, jeu, x, y):
        self.groups = jeu.all_sprites, jeu.interactifs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.list_images = jeu.arrive_images
        self.image = self.list_images[0]  # ferme, lorsque ouvre, animation + self.image = list_img[1]
        self.rect = pg.Rect((0, 0, 1/2*TILE_SIZE, TILE_SIZE))
        self.img_rect = self.image.get_rect(midbottom=self.rect.midbottom)
        self.type = "Arrive"  # en ajouter pour tous les interactifs

        # pos de depart
        self.rect.midbottom = pg.math.Vector2(x, y) * TILE_SIZE + (TILE_SIZE/2, TILE_SIZE)

    def update(self):
        self.img_rect.midbottom = self.rect.midbottom

    def draw(self, surface, pos):
        surface.blit(self.image, pos)


class Debut(Arrive):
    def __init__(self, jeu, x, y):
        Arrive.__init__(self, jeu, x, y)
        self.list_images = jeu.debut_images
        self.image = self.list_images[1]  # ferme, lorsque ouvre, animation + self.image = list_img[1]
        self.type = "Debut"
        self.ouvert = False

    def update(self):
        Arrive.update(self)
        if self.ouvert is True:
            self.image = self.list_images[0]


class Pouvoir(pg.sprite.Sprite):
    # class de base pour tous les joueurs
    def __init__(self, jeu, x, y):
        self.groups = jeu.all_sprites, jeu.interactifs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.list_images = jeu.pouvoir_img
        self.niveau_player = jeu.niveau

        # determine quel pouvoir en fonction du niveau
        """
        if self.niveau_player == 1:
            self.image = self.list_images[0]
        elif self.niveau_player == 2:
            self.image = self.list_images[1]
        """
        self.image = self.list_images[self.niveau_player - 1]

        self.rect = pg.Rect((0, 0, 1 / 2 * TILE_SIZE, 1 / 2 * TILE_SIZE))
        self.img_rect = self.image.get_rect(center=self.rect.center)
        self.type = "Pouvoir"

        # pos de depart
        self.rect.center = pg.math.Vector2(x, y) * TILE_SIZE + (TILE_SIZE / 2, TILE_SIZE / 2)

    def update(self):
        self.img_rect.center = self.rect.center

    def draw(self, surface, pos):
        surface.blit(self.image, pos)


class PlayerAtkProche(pg.sprite.Sprite):
    # class pour l'attaque de proche du joeur
    def __init__(self, jeu, x, y):
        self._layer = PLAYER_ATK_PROCHE_LAYER
        self.groups = jeu.all_sprites, jeu.interactifs
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = choice(jeu.img_player_atk)
        self.rect = pg.Rect((0, 0, 1/2*TILE_SIZE, 1/2*TILE_SIZE))  # hit box, a changer au besoin
        self.img_rect = self.image.get_rect(center=self.rect.center)
        self.type = "Player_atk_proche"  # en ajouter pour tous les interactifs

        # pos de depart
        self.rect.center = (x, y)

        # variables
        self.temps_passe = pg.time.get_ticks()

    def update(self, *args):
        self.img_rect.center = self.rect.center

        now = pg.time.get_ticks()
        if now - self.temps_passe > 100:
            self.kill()

    def draw(self, surface, pos):
        surface.blit(self.image, pos)
