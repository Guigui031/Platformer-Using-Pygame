# platforms pour Platformer
import pygame as pg
from random import choice
from engine.constants import *


class Brick(pg.sprite.Sprite):
    def __init__(self, jeu, x, y):
        self.groups = jeu.all_sprites, jeu.colliders
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = choice(jeu.brick_images)
        self.rect = pg.Rect((0, 0, TILE_SIZE, TILE_SIZE))
        self.img_rect = self.image.get_rect(midbottom=self.rect.midbottom)
        # multiplier par le w et h
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

    def update(self):
        self.img_rect.midbottom = self.rect.midbottom

    def draw(self, surface, pos):
        surface.blit(self.image, pos)
