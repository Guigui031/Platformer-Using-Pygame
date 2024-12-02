# constants pour Platformer
import pygame as pg

# window & jeu
TITRE = "Qqch"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
FPS = 60
TILE_SIZE = 80
FICHIER_NIVEAUX = 'Niveaux_Blocks.txt'
FICHIER_BACKGROUND = 'Niveaux_Background.txt'

# Common physics
GRAVITY = .8

# Player
PLAYER_JUMP = -15
PLAYER_ACC = 0.75
PLAYER_MAX_SPEED = 10
PLAYER_FRICTION = -0.1
PLAYER_DASH = 15

# layers
PLAYER_ATK_PROCHE_LAYER = 6
PLAYER_LAYER = 5
OBJECTIF_LAYER = 3

# colors
GRIS = (200, 200, 200)
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)
JAUNE = (255, 255, 0)
BRUN = (185, 122, 87)
ROSE = (255, 174, 201)
MAUVE = (255, 0, 255)
ORANGE = (255, 122, 0)

# keys
KEYS = {'bouge_droite': pg.K_RIGHT,
        'bouge_gauche': pg.K_LEFT,
        'jump': pg.K_w,
        'dash': pg.K_d,
        'atk_proche': pg.K_f}
K_FULLSCREEN = pg.K_i
K_PAUSE = pg.K_p

# states
IMMOBILE = "immobile"
BOUGE = "bouge"
DECELERATION = "decelaration"
JUMP = "jump"
TOMBE = "tombe"
DASH = "dash"

# directions
DROIT = "droit"
GAUCHE = "gauche"
HAUT = "haut"
BAS = "bas"
