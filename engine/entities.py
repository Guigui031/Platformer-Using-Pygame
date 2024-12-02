# enemies pour Platformer

import pygame as pg
from engine.constants import *
vecteur = pg.math.Vector2


class Monstre(pg.sprite.Sprite):
    # base class for enemies
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

    def update(self, *args):
        pass


class Zombie(pg.sprite.Sprite):
    def __init__(self, jeu, x, y):
        self.groups = jeu.all_sprites, jeu.mobs
        pg.sprite.Sprite.__init__(self, self.groups)

        # load images
        self.anim_immobile_G = jeu.anim_zombie_immobile
        self.anim_immobile_D = self.load_inverse(self.anim_immobile_G)
        self.anim_bouge_G = jeu.anim_zombie_bouge
        self.anim_bouge_D = self.load_inverse(self.anim_bouge_G)

        # setup
        self.image = self.anim_immobile_G[0]
        self.rect = pg.Rect((0, 0, 1 / 2 * TILE_SIZE, 1 / 2 * TILE_SIZE))
        self.img_rect = self.image.get_rect(midbottom=self.rect.midbottom)

        # pos de depart
        self.rect.midbottom = vecteur(x, y) * TILE_SIZE + vecteur(TILE_SIZE / 2, TILE_SIZE)

        # utilitaires
        self.vit = vecteur(0, 0)
        self.acc = vecteur(0, GRAVITY)
        self.state = IMMOBILE
        self.frame_index = 0
        self.ticks = 0
        self.current_anim = self.anim_immobile_G
        self.old_anim = self.anim_immobile_G
        self.direction = GAUCHE

    def load_inverse(self, list_anim):
        list_anim_g = []
        for img in list_anim:
            img = pg.transform.flip(img, True, False)
            list_anim_g.append(img)
        return list_anim_g

    def update(self):
        self.acc.x += self.vit.x * PLAYER_FRICTION  # plus il va vite, plus la friction est grande
        self.vit += self.acc
        self.animation()
        self.img_rect.midbottom = self.rect.midbottom

    def animation(self):
        # jouer animation en fct de la vit
        if abs(self.vit.x) >= 2:
            k = 1 / abs(self.vit.x)
        else:
            k = .25
        # print(k)
        if self.current_anim != self.old_anim:
            self.image = self.current_anim[0]
        if self.ticks % round(k * 50) == 0:
            # bottom = self.rect.bottom
            self.frame_index = (self.frame_index + 1) % len(self.current_anim)
            self.image = self.current_anim[self.frame_index]
            # self.rect = self.image.get_rect()
            # self.rect.bottom = bottom
        self.ticks += 1

    def gestion_collision_rect_x(self, collider):
        if self.rect.centerx < collider.centerx:
            self.rect.right = collider.left
            self.vit.x = 0
        if self.rect.centerx > collider.centerx:
            self.rect.left = collider.right
            self.vit.x = 0

    def gestion_collision_rect_y(self, collider):
        if self.rect.centery > collider.centery:
            self.rect.top = collider.bottom
            self.vit.y = 0
        if self.rect.centery < collider.centery:
            self.rect.bottom = collider.top
            self.vit.y = 0

    def draw(self, surface, pos):
        surface.blit(self.image, pos)
