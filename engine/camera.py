# player pour Platformer
import pygame as pg
from engine.constants import *


class Camera:
    def __init__(self):
        self.camera = pg.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.offset = pg.math.Vector2(0, 0)
        self.figer = True

    def update(self, focus, niv_size):
        if self.figer:
            pass
        if not self.figer:
            self.fluide(focus)
            if self.offset.x >= 0:
                self.offset.x = 0
            elif self.offset.x <= -niv_size[0]+SCREEN_WIDTH:
                self.offset.x = -niv_size[0]+SCREEN_WIDTH
            if 0 <= self.offset.x <= -niv_size[0]+SCREEN_WIDTH:
                self.offset.x = int((SCREEN_WIDTH - niv_size[0]) / 2)

            if self.offset.y >= 0:
                self.offset.y = 0
            elif self.offset.y <= -niv_size[1]+SCREEN_HEIGHT:
                self.offset.y = -niv_size[1]+SCREEN_HEIGHT
            if 0 <= self.offset.y <= -niv_size[1]+SCREEN_HEIGHT:
                self.offset.y = int((SCREEN_HEIGHT - niv_size[1]) / 2)

    def fluide(self, focus):
        # A vector that points from the camera to the player.
        heading = focus.rect.center - self.camera
        # Follow the player with the camera.
        # Move the camera by a fraction of the heading vector's length.
        self.camera += heading * 0.05
        # The actual offset that we have to add to the positions of the objects.
        self.offset = -self.camera + pg.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        #                          + (__, __) to center the player
