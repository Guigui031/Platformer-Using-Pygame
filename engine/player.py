# player pour Platformer
import pygame as pg
from math import copysign
from engine.constants import *
from pygame.locals import *
vecteur = pg.math.Vector2


class PlayerNiv0(pg.sprite.Sprite):
    def __init__(self, jeu, x, y):
        self._layer = PLAYER_LAYER  # draw par-dessus les layers plus basses
        self.groups = jeu.all_sprites  # ajoute automatiquement a tous ses groupes
        pg.sprite.Sprite.__init__(self, self.groups)

        # load images
        self.anim_player_immobile_D = jeu.anim_player_immobile
        self.anim_player_immobile_G = self.load_gauche(self.anim_player_immobile_D)
        self.anim_player_bouge_D = jeu.anim_player_bouge
        self.anim_player_bouge_G = self.load_gauche(self.anim_player_bouge_D)
        self.anim_player_brake_D = jeu.anim_player_brake
        self.anim_player_brake_G = self.load_gauche(self.anim_player_brake_D)
        self.anim_player_fall_D = jeu.anim_player_fall
        self.anim_player_fall_G = self.load_gauche(self.anim_player_fall_D)

        # setup
        self.image = self.anim_player_immobile_D[0]
        # self.image.fill(BLEU)
        self.rect = pg.Rect((0, 0, 1/2*TILE_SIZE, 1/2*TILE_SIZE))
        self.img_rect = self.image.get_rect(midbottom=self.rect.midbottom)
        # todo: hit_rect pour les collisions (plus petit sur les cotes)

        # pos de depart
        self.rect.midbottom = vecteur(x, y) * TILE_SIZE + vecteur(TILE_SIZE/2, TILE_SIZE) / 2

        # utilitaires
        self.vit = vecteur(0, 0)
        self.acc = vecteur(0, GRAVITY)
        self.state = IMMOBILE
        self.frame_index = 0
        self.ticks = 0
        self.current_anim = self.anim_player_immobile_D
        self.old_anim = self.anim_player_immobile_D
        self.direction = DROIT
        self.allow_jump = True   # pour les particles, si faux ne marche pas
        self.allow_dash = True   # pareil
        self.niveau = 0

    def reset(self, x, y):
        # pos de depart
        self.rect.midbottom = vecteur(x, y) * TILE_SIZE + vecteur(TILE_SIZE/2, TILE_SIZE-1)
        # -1 a cause d'un bug lorsqu'apparaissait dans le bloc, surement a cause de gravite

    def load_gauche(self, list_anim):
        list_anim_g = []
        for img in list_anim:
            img = pg.transform.flip(img, True, False)
            list_anim_g.append(img)
        return list_anim_g

    def update(self):
        self.acc.x += self.vit.x * PLAYER_FRICTION  # plus il va vite, plus la friction est grande
        self.vit += self.acc
        self.animation()
        if abs(self.vit.x) > 7.5 and self.state != DASH:
            self.vit.x = copysign(7.5, self.vit.x)
        self.img_rect.midbottom = self.rect.midbottom

    def handle_state(self, keys):
        self.old_anim = self.current_anim
        if self.state == IMMOBILE:
            self.immobile(keys)
        elif self.state == BOUGE:
            self.bouger(keys)
        elif self.state == TOMBE:
            self.tomber(keys)

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

    def immobile(self, keys):
        # self.image.fill(ROSE)
        # self.animation(self.anim_player_immobile)

        if keys[KEYS['bouge_droite']] or keys[KEYS['bouge_gauche']]:
            if keys[KEYS['bouge_gauche']]:
                self.acc.x = -PLAYER_ACC
                self.state = BOUGE
                self.direction = GAUCHE
            elif keys[KEYS['bouge_droite']]:
                self.acc.x = PLAYER_ACC
                self.state = BOUGE
                self.direction = DROIT
            if keys[KEYS['bouge_droite']] and keys[KEYS['bouge_gauche']]:
                self.acc.x = 0
        else:
            self.acc.x = 0

        if self.direction == DROIT:
            self.current_anim = self.anim_player_immobile_D
        elif self.direction == GAUCHE:
            self.current_anim = self.anim_player_immobile_G

        if self.vit.y > GRAVITY * 2:  # * 2 pour plus facile
            self.state = TOMBE

    def bouger(self, keys):
        # self.image.fill(VERT)
        # self.animation(self.anim_player_bouge)

        if keys[KEYS['bouge_droite']] or keys[KEYS['bouge_gauche']]:
            if keys[KEYS['bouge_gauche']]:
                self.acc.x = -PLAYER_ACC
                self.direction = GAUCHE
            elif keys[KEYS['bouge_droite']]:
                self.acc.x = PLAYER_ACC
                self.direction = DROIT
            if keys[KEYS['bouge_droite']] and keys[KEYS['bouge_gauche']]:
                self.acc.x = 0
        else:
            self.acc.x = 0

        if self.direction == GAUCHE:
            self.current_anim = self.anim_player_bouge_G
        elif self.direction == DROIT:
            self.current_anim = self.anim_player_bouge_D

        # brake
        if self.vit.x > 0 and self.direction == GAUCHE:
            self.current_anim = self.anim_player_brake_D
        elif self.vit.x < 0 and self.direction == DROIT:
            self.current_anim = self.anim_player_brake_G

        if self.vit.y > GRAVITY * 2:  # * 2 pour plus facile
            self.state = TOMBE
        elif abs(self.vit.x) <= 0.1:
            self.vit.x = 0
            self.state = IMMOBILE

    def tomber(self, keys):
        # self.image.fill(JAUNE)
        # self.animation(self.anim_player_fall)
        if keys[KEYS['bouge_droite']] or keys[KEYS['bouge_gauche']]:
            if keys[KEYS['bouge_gauche']]:
                self.acc.x = -PLAYER_ACC
                self.direction = GAUCHE
            elif keys[KEYS['bouge_droite']]:
                self.acc.x = PLAYER_ACC
                self.direction = DROIT
            if keys[KEYS['bouge_droite']] and keys[KEYS['bouge_gauche']]:
                self.acc.x = 0
        else:
            self.acc.x = 0

        if self.direction == DROIT:
            self.current_anim = self.anim_player_fall_D
        elif self.direction == GAUCHE:
            self.current_anim = self.anim_player_fall_G

        if self.vit.y <= GRAVITY and self.vit.x != 0:
            self.state = BOUGE
        elif self.vit.y <= GRAVITY and self.vit.x == 0:
            self.state = IMMOBILE

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

    def jump(self, keys):
        pass

    def cut_saut(self):
        pass

    def check_allow_jump(self, keys):
        pass

    def dash(self, keys):
        pass

    def check_allow_dash(self, keys):
        pass


class PlayerNiv1(PlayerNiv0):
    # jump en plus
    def __init__(self, jeu, x, y):
        PlayerNiv0.__init__(self, jeu, x, y)
        # load images
        self.anim_player_jump_D = jeu.anim_player_jump
        self.anim_player_jump_G = self.load_gauche(self.anim_player_jump_D)

        # utilitaires
        self.niveau = 1

    def handle_state(self, keys):
        PlayerNiv0.handle_state(self, keys)
        if self.state == JUMP:
            self.jump(keys)
        self.check_allow_jump(keys)

    def immobile(self, keys):
        PlayerNiv0.immobile(self, keys)
        if keys[KEYS['jump']]:
            if self.allow_jump:
                self.vit.y = PLAYER_JUMP
                self.state = JUMP
                self.allow_jump = False

    def bouger(self, keys):
        PlayerNiv0.bouger(self, keys)
        if keys[KEYS['jump']]:
            if self.allow_jump:
                self.vit.y = PLAYER_JUMP
                self.state = JUMP
                self.allow_jump = False

    def jump(self, keys):
        # self.image.fill(BLEU)
        # self.animation(self.anim_player_jump)
        if keys[KEYS['bouge_droite']] or keys[KEYS['bouge_gauche']]:
            if keys[KEYS['bouge_gauche']]:
                self.acc.x = -PLAYER_ACC
                self.direction = GAUCHE
            elif keys[KEYS['bouge_droite']]:
                self.acc.x = PLAYER_ACC
                self.direction = DROIT
            if keys[KEYS['bouge_droite']] and keys[KEYS['bouge_gauche']]:
                self.acc.x = 0
        else:
            self.acc.x = 0

        if self.direction == DROIT:
            self.current_anim = self.anim_player_jump_D
        elif self.direction == GAUCHE:
            self.current_anim = self.anim_player_jump_G

        if self.vit.y > GRAVITY:
            self.state = TOMBE

    def cut_saut(self):
        # si relache touche jump, saut s'arrete non brusque
        if self.vit.y < -4:
            self.vit.y = -4

    def check_allow_jump(self, keys):
        # empeche les sauts repetes lorsque touche reste appuye
        if not keys[KEYS['jump']]:
            self.allow_jump = True


class PlayerNiv2(PlayerNiv1):
    # dash en plus
    def __init__(self, jeu, x, y):
        PlayerNiv1.__init__(self, jeu, x, y)
        # load images
        self.anim_player_dash_D = jeu.anim_player_dash
        self.anim_player_dash_G = self.load_gauche(self.anim_player_dash_D)
        # utilitaires
        self.niveau = 2

    def handle_state(self, keys):
        PlayerNiv1.handle_state(self, keys)
        if self.state == DASH:  # oui ou non (comme brake)
            self.dash(keys)

    def immobile(self, keys):
        PlayerNiv1.immobile(self, keys)
        if keys[KEYS['dash']] and self.allow_dash:
            # self.dash(keys)  # ou le mettre en self.state = DASH
            self.state = DASH
            self.direction_dash()
        self.check_allow_dash(keys)

    def bouger(self, keys):
        PlayerNiv1.bouger(self, keys)
        if keys[KEYS['dash']] and self.allow_dash:
            # self.dash(keys)
            self.state = DASH
            self.direction_dash()
        self.check_allow_dash(keys)

    def tomber(self, keys):
        PlayerNiv1.tomber(self, keys)
        if keys[KEYS['dash']] and self.allow_dash:
            # self.dash(keys)
            self.state = DASH
            self.direction_dash()

    def jump(self, keys):
        PlayerNiv1.jump(self, keys)
        if keys[KEYS['dash']] and self.allow_dash:
            # self.dash(keys)
            self.state = DASH
            self.direction_dash()

    def dash(self, keys):
        if keys[KEYS['bouge_droite']] or keys[KEYS['bouge_gauche']]:
            if keys[KEYS['bouge_gauche']]:
                self.acc.x = -PLAYER_ACC
            elif keys[KEYS['bouge_droite']]:
                self.acc.x = PLAYER_ACC
            if keys[KEYS['bouge_droite']] and keys[KEYS['bouge_gauche']]:
                self.acc.x = 0
        else:
            self.acc.x = 0

        if abs(self.vit.x) < 10 and self.vit.y >= GRAVITY:
            self.state = TOMBE
        # elif abs(self.vit.x) < 10 and self.vit.y <= GRAVITY:
          #  self.state = BOUGE

    def direction_dash(self):
        if self.direction == DROIT:
            self.vit.x = PLAYER_DASH
            self.current_anim = self.anim_player_dash_D
        elif self.direction == GAUCHE:
            self.vit.x = -PLAYER_DASH
            self.current_anim = self.anim_player_dash_G
        if self.vit.y > 0:
            self.vit.y = 0
        self.allow_dash = False

    def check_allow_dash(self, keys):
        if not keys[KEYS['dash']]:
            self.allow_dash = True


class PlayerNiv3(PlayerNiv2):
    # attaque proche en plus
    def __init__(self, jeu, x, y):
        PlayerNiv2.__init__(self, jeu, x, y)
        # load images
        # self.anim_attaque_walKEYS['dash']...
        # utilitaires
        self.niveau = 3

    def handle_state(self, keys):
        PlayerNiv2.handle_state(self, keys)

