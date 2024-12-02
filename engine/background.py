# background pour Platformer
import pygame as pg
from engine.constants import *
import random
from math import copysign


class Particle(pg.sprite.Sprite):
    def __init__(self, jeu, pos, player_vit, direction):
        self.groups = jeu.all_sprites, jeu.background_objects
        pg.sprite.Sprite.__init__(self, self.groups)

        self.anim_img = jeu.anim_particles
        self.image = self.anim_img[0]
        self.rect = self.image.get_rect(center=pos)
        self.img_rect = self.rect

        self.frame = 0
        self.timer = pg.time.get_ticks()

        # selon vit...
        self.vit = direction * pg.math.Vector2(abs(player_vit.x)/2, abs(player_vit.y)/2)
        self.vit.x += copysign(random.randint(0, 2), self.vit.x)
        self.vit.y -= copysign(random.randint(4, 7), player_vit.y)
        self.acc = pg.math.Vector2(0, GRAVITY)

    def update(self):
        now = pg.time.get_ticks()
        self.vit += self.acc
        self.rect.center += self.vit

        # kill lorsque arrive au bout
        if self.frame >= len(self.anim_img):
            self.kill()
        elif now - self.timer > 25:
            self.image = self.anim_img[self.frame]
            self.frame += 1
            self.timer = pg.time.get_ticks()

    def draw(self, surface, pos):
        surface.blit(self.image, pos)


class Wall(pg.sprite.Sprite):
    def __init__(self, jeu, x, y):
        self.groups = jeu.all_sprites, jeu.background_objects
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = jeu.imgs_wall
        self.rect = pg.Rect((0, 0, TILE_SIZE, TILE_SIZE))
        self.img_rect = self.image.get_rect(center=self.rect.center)
        # multiplier par le w et h
        self.rect.centerx = x * TILE_SIZE + TILE_SIZE/2
        self.rect.centery = y * TILE_SIZE + TILE_SIZE/2

    def update(self):
        self.img_rect.center = self.rect.center

    def draw(self, surface, pos):
        surface.blit(self.image, pos)
