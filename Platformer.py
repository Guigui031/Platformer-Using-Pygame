# creer par Guillaume Genois

# art by Master484
# https://opengameart.org/users/master484
# https://opengameart.org/content/cute-platformer-sisters

import pygame as pg
import sys, os, random
from engine.constants import *
from engine.player import *
from engine.entities import *
from engine.colliders import *
from engine.camera import *
from engine.menus import *
from engine.interactifs import *
from engine.background import *
# from level_editor.level_editor import App as LevelEditor
from warnings import filterwarnings

filterwarnings("ignore", category=DeprecationWarning)  # ignore les erreurs de non int pour rect

# si unresolved reference lors import own module
# https://stackoverflow.com/questions/21236824/unresolved-reference-issue-in-pycharm


def union_surface(img_1, img_2):
    surface_courante = pg.Surface(
        (img_1.get_width() + img_2.get_width(), img_1.get_height()),
        pg.SRCALPHA)
    surface_courante.blit(img_1, (0, 0))
    surface_courante.blit(img_2, (img_1.get_width(), 0))
    return surface_courante


def lire_fichier_niveaux(fichier):
    counter_lignes_niv = 0
    niv_courant = []
    listes_tous_niv = []
    salle_entre_niv = []
    with open(os.path.join("data", fichier), 'r') as file:
        for ligne in file.readlines():
            if ligne[0] == ">":
                # ligne = ligne[:ligne.index(">")]
                pass
            elif ligne[0] == "(":
                niv_courant = []
            elif ligne[0] == ")":
                listes_tous_niv.append(niv_courant)
            elif ligne[0] == "/":
                salle_entre_niv.append(ligne.rstrip("/"))
            else:
                niv_courant.append(ligne.rstrip("\n"))
    return listes_tous_niv, salle_entre_niv


def insert_anim(folder, nom_img, width, nb_frames):
    list = []
    folder_path = os.path.join('image', folder)
    img = pg.image.load(os.path.join(folder_path, nom_img))
    img = img.convert()
    #img.set_alpha(None)
    img.set_colorkey(img.get_at((5, 5)), pg.RLEACCEL)
    # regler le probleme de set_colorkey sur les images!!!!!
    # j'ai finalement juste mis le bckg transparent sur aseprite
    # 1. Prendre la couleur du background avec l'eprouvette
    # 2. Mettre Layer -> Layer from Background  (parfois deja mis)
    # 3. Edit -> Replace Color...
    # 4. Mettre comme couleur de remplacement "Mask"
    # (devrait deja voir l'image changé avant de cliquer sur ok)
    # 5. Ne pas oublier de Save apres

    # découpage
    image_width, image_height = img.get_size()
    k = width * nb_frames / image_width
    img = pg.transform.smoothscale(img, (int(width * nb_frames), int(image_height * k)))
    image_width, image_height = img.get_size()
    frame_width = image_width / nb_frames

    # ajouter dans liste
    for i in range(nb_frames):
        list.append(img.subsurface((i * frame_width, 0, frame_width, image_height)))
    return list


def load_img(folder, nom_img, size=(TILE_SIZE, TILE_SIZE), colorkey=True):
    folder_path = os.path.join('image', folder)
    img = pg.image.load(os.path.join(folder_path, nom_img))
    img = img.convert()
    if colorkey:
        img.set_colorkey(img.get_at((0, 0)), pg.RLEACCEL)
    img = pg.transform.smoothscale(img, (int(size[0]), int(size[1])))
    return img


class App:
    """
    Gestion du program flow et des evenements
    """

    def __init__(self):
        """
        Creation de l'objet rectangle apres avoir initialisé et recuperer
        la surface de la fenêtre
        """
        # utilitaires pour fullscreen
        self.ecran_w, self.ecran_h = pg.display.Info().current_w, pg.display.Info().current_h
        
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(TITRE)
        self.jeu = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    def initialisation_variables(self):
        # creation des variables des events
        self.keys = pg.key.get_pressed()

        # creation d'une list des niveaux qui sont des listes de string (aussi list)
        self.fichier_background, self.salle_entre_niv_bckg = lire_fichier_niveaux(FICHIER_BACKGROUND)
        self.fichier_niveaux, self.salle_entre_niv = lire_fichier_niveaux(FICHIER_NIVEAUX)
        self.niveau = 0
        self.niv_size = (0, 0)

        # gestion de l'horloge et du fps max
        self.clock = pg.time.Clock()
        self.dt = 0

        # setup bool
        self.quit = False
        self.fullscreen = False
        self.presentement_entre_niv = False

        self.camera = Camera()
        self.current_keys = KEYS  # par default
        self.read_fichier_customizations()

    def load_images(self):
        # UI
        #                           si jamais veut anim, pour l'instant non necessaire
        self.anim_boutton_quitter = [load_img(os.path.join('Land Objects', 'Sprites'), 'ExitSign_A1.png', (200, 112.5), True),
                                     load_img(os.path.join('Land Objects', 'Sprites'), 'ExitSign_A2.png', (200, 112.5), True)]
        # self.font_personnaliser = insert_anim('Background', 'Alfabeto.png', 26, 50)

        # background
        self.imgs_background = [load_img('Background', 'Horror.png', (SCREEN_WIDTH, SCREEN_HEIGHT)),
                                load_img(os.path.join('GraveyardTileset', 'png'), 'BG.png', (SCREEN_WIDTH, SCREEN_HEIGHT))]
        self.anim_particles = insert_anim('Special Effects', 'BigSmoke3_32x32_Anim.png', 1/4*TILE_SIZE, 7)
        self.imgs_wall = load_img(os.path.join('Land Objects', 'Sprites'), 'Tile_Black.png', (5/4*TILE_SIZE, 5/4*TILE_SIZE))

        # player
        self.anim_Melissa_immobile = insert_anim('Player Melissa', 'Melissa_Stand_R.png', 3 / 4 * TILE_SIZE, 1)
        self.anim_Melissa_bouge = insert_anim('Player Melissa', 'Melissa_Walk_Anim_R.png', 3/4*TILE_SIZE, 4)
        self.anim_Melissa_brake = insert_anim('Player Melissa', 'Melissa_Brake_R.png', 3/4*TILE_SIZE, 1)
        self.anim_Melissa_jump = insert_anim('Player Melissa', 'Melissa_Jump2_R.png', 3/4*TILE_SIZE, 1)
        self.anim_Melissa_fall = insert_anim('Player Melissa', 'Melissa_Fall2_R.png', 3/4*TILE_SIZE, 1)
        self.anim_Melissa_dash = insert_anim('Player Melissa', 'Melissa_Att_Dash_R.png', 3 / 4 * TILE_SIZE, 1)
        self.atk_Melissa_proche = [load_img('Special Effects', 'SmallHitFlash4_A1.png', (1/2*TILE_SIZE, 1/2*TILE_SIZE)),
                                   load_img('Special Effects', 'SmallHitFlash4_A2.png', (1/2*TILE_SIZE, 1/2*TILE_SIZE))]

        self.anim_Rosette_immobile = insert_anim('Player Rosette', 'Rosette_Stand_R.png', 3 / 4 * TILE_SIZE, 1)
        self.anim_Rosette_bouge = insert_anim('Player Rosette', 'Rosette_Walk_32x32_Anim_R.png', 3 / 4 * TILE_SIZE, 4)
        self.anim_Rosette_brake = insert_anim('Player Rosette', 'Rosette_Brake_R.png', 3 / 4 * TILE_SIZE, 1)
        self.anim_Rosette_jump = insert_anim('Player Rosette', 'Rosette_Jump2_R.png', 3 / 4 * TILE_SIZE, 1)
        self.anim_Rosette_fall = insert_anim('Player Rosette', 'Rosette_Fall2_R.png', 3 / 4 * TILE_SIZE, 1)
        self.anim_Rosette_dash = insert_anim('Player Rosette', 'Rosette_Att_Dash_R.png', 3 / 4 * TILE_SIZE, 1)
        self.atk_Rosette_proche = [load_img('Special Effects', 'SmallHitFlash5_A1.png', (1/2*TILE_SIZE, 1/2*TILE_SIZE)),
                                   load_img('Special Effects', 'SmallHitFlash5_A2.png', (1/2*TILE_SIZE, 1/2*TILE_SIZE))]

        self.anim_Luigi_immobile = insert_anim('Player Luigi', 'immobile.png', 3/4*TILE_SIZE, 1)
        self.anim_Luigi_bouge = insert_anim('Player Luigi', 'walk.png', 3 / 4 * TILE_SIZE, 3)
        self.anim_Luigi_brake = insert_anim('Player Luigi', 'brake.png', 3 / 4 * TILE_SIZE, 1)
        self.anim_Luigi_jump = insert_anim('Player Luigi', 'jump.png', 3 / 4 * TILE_SIZE, 1)
        self.anim_Luigi_fall = insert_anim('Player Luigi', 'fall.png', 3 / 4 * TILE_SIZE, 1)
        self.anim_Luigi_dash = insert_anim('Player Luigi', 'dash.png', 3 / 4 * TILE_SIZE, 1)
        self.atk_Luigi_proche = [load_img('Special Effects', 'SmallHitFlash6_A1.png', (1/2*TILE_SIZE, 1/2*TILE_SIZE)),
                                 load_img('Special Effects', 'SmallHitFlash6_A2.png', (1/2*TILE_SIZE, 1/2*TILE_SIZE))]

        # monstres
        zombie_anim = insert_anim('Monsters', 'Zombie Gros.png', TILE_SIZE, 4)
        self.anim_zombie_immobile = [zombie_anim[2]]
        self.anim_zombie_bouge = [zombie_anim[0], zombie_anim[1]]

        # blocks
        self.brick_images = [load_img(os.path.join('Land Objects', 'Sprites'), 'Block_Type2_Black.png', colorkey=False),
                            load_img('Land', 'Small_Platform_Orange.png'), load_img('Land', 'Small_Platform_Green.png')]
        self.tiles_set = ('Land', 'Small_Platform_Orange.png', True), ('Land', 'Small_Platform_Green.png', True),\
                         ('Land', 'Small_Platform_Purple.png', True), ('Land', 'Small_Platform_White.png', True), \
                         ('Land', 'Small_Platform_Brown.png', True), \
                         (os.path.join('Land Objects', 'Sprites'), 'Block_Type2_Black.png', False), \
                         (os.path.join('Land Objects', 'Sprites'), 'Block_Type2_Blue.png', False), \
                         (os.path.join('Land Objects', 'Sprites'), 'Block_Type2_Brown.png', False), \
                         (os.path.join('Land Objects', 'Sprites'), 'Block_Type2_Gray.png', False), \
                         (os.path.join('Land Objects', 'Sprites'), 'Block_Type2_Green.png', False), \
                         (os.path.join('Land Objects', 'Sprites'), 'Block_Type2_Purple.png', False), \
                         (os.path.join('Land Objects', 'Sprites'), 'Block_Type2_Red.png', False), \
                         (os.path.join('Land Objects', 'Sprites'), 'Block_Type2_Yellow.png', False)

        # interactifs
        self.arrive_images = [load_img(os.path.join('Land Objects', 'Sprites'), 'Door_Type1_Blue_Open.png'),
                              load_img(os.path.join('Land Objects', 'Sprites'), 'Door_Type1_Blue_Closed.png')]
        self.debut_images = [load_img(os.path.join('Land Objects', 'Sprites'), 'Door_Type1_Green_Open.png'),
                             load_img(os.path.join('Land Objects', 'Sprites'), 'Door_Type1_Green_Closed.png')]
        self.pouvoir_img = [load_img('Collectibles', 'Apple_Green.png', (1/2*TILE_SIZE, 1/2*TILE_SIZE)),
                            load_img('Collectibles', 'Apple_Red.png', (1/2*TILE_SIZE, 1/2*TILE_SIZE)),
                            load_img('Collectibles', 'Apple_Orange.png', (1/2*TILE_SIZE, 1/2*TILE_SIZE)),
                            load_img('Collectibles', 'Cherry1.png', (1/2*TILE_SIZE, 1/2*TILE_SIZE)),
                            load_img('Collectibles', 'Cherry2.png', (1/2*TILE_SIZE, 1/2*TILE_SIZE))]
        self.current_background = self.imgs_background[0]

    def read_fichier_customizations(self):
        """current_customization = []  # list en train de se faire lire
        custom_keys = []
        with open(os.path.join("data", "Customizations.txt"), 'r') as file:
            for ligne in file:
                if ligne == "custom_keys":
                    current_customization = custom_keys
                elif ligne == "add autre custom drette la plus tard":
                    pass
                else:
                    current_customization.append(ligne.rstrip("\n"))
        for ligne in custom_keys:
            action, key = (ligne.strip().split(":"))
            for act in self.current_keys:
                if act == action:
                    self.current_keys[act] = key
        print(self.current_keys)"""
        with open(os.path.join("data", "Customizations.txt"), 'r') as file:
            for ligne in file:
                action, key = (ligne.strip().split(":"))
                for act in self.current_keys:
                    if act == action:
                        self.current_keys[act] = int(key)

    def new(self, new_niv=True):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.colliders = pg.sprite.Group()
        self.interactifs = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.background_objects = pg.sprite.Group()
        if self.player is None:
            self.load_player()
        if new_niv:
            self.load_niv(self.fichier_background[self.niveau])
            self.load_niv(self.fichier_niveaux[self.niveau])
            self.current_background = self.imgs_background[0]
        elif not new_niv:
            self.load_niv(self.salle_entre_niv_bckg)
            self.load_niv(self.salle_entre_niv)
            self.current_background = self.imgs_background[1]

        if self.niv_size[0] > SCREEN_WIDTH * 1.5 or self.niv_size[1] > SCREEN_HEIGHT * 1.5:
            self.camera.figer = False
            self.camera.offset = pg.math.Vector2((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                                                 - pg.math.Vector2(self.player.rect.center))
            self.camera.camera = pg.math.Vector2(self.player.rect.center)
        else:
            self.camera.figer = True
            self.camera.offset = pg.math.Vector2(int((SCREEN_WIDTH - self.niv_size[0]) / 2),
                                                 int((SCREEN_HEIGHT - self.niv_size[1]) / 2))
            self.camera.camera = pg.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def load_niv(self, niveau):
        for range, ligne in enumerate(niveau):
            for colonne, item in enumerate(ligne):
                if item == 'P':
                    self.player.reset(colonne, range)
                    self.all_sprites.add(self.player)
                elif item == '#':
                    Brick(self, colonne, range)
                elif item == 'Z':
                    Zombie(self, colonne, range)
                elif item == '@':
                    Pouvoir(self, colonne, range)
                elif item == 'F':
                    Arrive(self, colonne, range)
                elif item == 'D':
                    Debut(self, colonne, range)
                elif item == 'W':
                    Wall(self, colonne, range)
                elif item == 'H':
                    Fenetre(self, colonne, range)
                else:
                    pass
        self.niv_size = len(niveau[0]) * TILE_SIZE, len(niveau) * TILE_SIZE

    def load_player(self):
        if self.player:
            x, y = self.player.rect.x / TILE_SIZE, self.player.rect.y / TILE_SIZE
            self.player.kill()
        elif self.player is None:
            x, y = 0, 0

        if self.niveau == 0:
            self.player = PlayerNiv0(self, x, y)
        elif self.niveau in (1, 2):
            self.player = PlayerNiv1(self, x, y)
        elif self.niveau in (3, 4):
            self.player = PlayerNiv2(self, x, y)
        elif self.niveau in (5, 6):
            self.player = PlayerNiv3(self, x, y)

    def event_handler(self):
        """
        capture des évenements clavier
        """
        for event in pg.event.get():
            if event.type == QUIT:
                self.quit = True
            elif event.type in (KEYUP, KEYDOWN):
                self.keys = pg.key.get_pressed()
                if event.type == KEYDOWN:
                    if self.keys[K_2]:
                        self.run_level_editor()
                        print("lol")

                    if self.keys[K_FULLSCREEN]:
                        self.fullscreen = not self.fullscreen
                        if self.fullscreen:
                            self.screen = pg.display.set_mode((self.ecran_w, self.ecran_h), pg.FULLSCREEN)
                        else:
                            self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)

                    if self.keys[K_ESCAPE]:
                        if self.fullscreen:
                            self.fullscreen = not self.fullscreen
                            self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
                        else:
                            self.quit = True

                    if self.player.allow_jump:    # ca veut dire sur la terre
                        if event.key == self.current_keys['bouge_droite']:
                            for i in range(5):
                                Particle(self, self.player.rect.bottomleft, self.player.vit, -1)
                        if event.key == self.current_keys['bouge_gauche']:
                            for i in range(5):
                                Particle(self, self.player.rect.bottomright, self.player.vit, 1)
                        if event.key == self.current_keys['jump'] and self.player.niveau >= 1:
                            for i in range(5):
                                Particle(self, self.player.rect.midbottom, self.player.vit, 0)
                        if event.key == self.current_keys['dash'] and self.player.niveau >= 2 and self.player.allow_dash:
                            for i in range(5):
                                Particle(self, self.player.rect.bottomleft, self.player.vit, copysign(1, -self.player.vit.x))
                    if event.key == self.current_keys['atk_proche'] and self.player.niveau >= 3:
                        if self.player.direction == DROIT:
                            # optimiser, depend quel personnage choisie, changer en dictionnaire
                            PlayerAtkProche(self, self.player.rect.right, self.player.rect.centery)
                        elif self.player.direction == GAUCHE:
                            PlayerAtkProche(self, self.player.rect.left, self.player.rect.centery)

                if event.type == KEYUP:
                    if event.key == K_PAUSE:
                        pause = Pause(self, self.screen.copy())
                        if pause.quit_jeu:
                            self.quit = True
                    if event.key == self.current_keys['jump']:
                        self.player.cut_saut()
                    if event.key == self.current_keys['jump'] and self.player.niveau > 0:
                        if self.player.state in (IMMOBILE, BOUGE):
                            self.player.check_allow_jump(self.keys)

    def update(self):
        """
        Mise à jour des attributs de chaque rectangle en fonction des
        évènements capturés
        """
        # update all sprites + camera
        self.all_sprites.update()
        self.camera.update(self.player, self.niv_size)

        # --------------------------------------------------move player
        self.player.handle_state(self.keys)
        # x
        self.player.rect.x += int(self.player.vit.x + self.player.acc.x / 2 + self.dt)
        # collisions colliders
        hits = pg.sprite.spritecollide(self.player, self.colliders, False)
        for hit in hits:
            self.player.gestion_collision_rect_x(hit.rect)
        # y
        self.player.rect.y += int(self.player.vit.y + self.player.acc.y / 2 + self.dt)
        hits = pg.sprite.spritecollide(self.player, self.colliders, False)
        for hit in hits:
            self.player.gestion_collision_rect_y(hit.rect)

        # ----------------------------------------------------move mobs
        for mob in self.mobs:
            # x
            mob.rect.x += int(mob.vit.x + mob.acc.x / 2 + self.dt)
            # collisions colliders
            hits = pg.sprite.spritecollide(mob, self.colliders, False)
            for hit in hits:
                mob.gestion_collision_rect_x(hit.rect)
            # y
            mob.rect.y += int(mob.vit.y + mob.acc.y / 2 + self.dt)
            hits = pg.sprite.spritecollide(mob, self.colliders, False)
            for hit in hits:
                mob.gestion_collision_rect_y(hit.rect)

        # ---------------------------------------------------collisions interactifs et player
        hits = pg.sprite.spritecollide(self.player, self.interactifs, False)
        for hit in hits:
            if hit.type == "Arrive":
                # lorsque atteint dernier niv, recommence
                self.niveau = (self.niveau + 1) % len(self.fichier_niveaux)
                if self.niveau in (1, 3, 5):
                    self.new(False)
                    self.presentement_entre_niv = True
                else:
                    self.new()
            elif hit.type == "Debut":
                if hit.ouvert is True:
                    self.new()
                    self.presentement_entre_niv = False
            elif hit.type == "Pouvoir":
                for interactif in self.interactifs:
                    if interactif.type == "Debut":
                        interactif.ouvert = True
                self.load_player()
                hit.kill()

        # ----------------------------------------collisions interactifs et mobs
        for mob in self.mobs:
            hits = pg.sprite.spritecollide(mob, self.interactifs, False)
            for hit in hits:
                if hit.type == "Player_atk_proche":
                    mob.kill()

        # gestion limites lorsque tombe  # optimiser, automatiser
        if self.player.rect.y >= self.niv_size[1]*2:
            self.new(True)

    def draw(self):
        """
        Dessine tout ce qu'il y a a dessiner sur la surface
        """
        self.jeu.blit(self.current_background, (0, 0))
        for sprite in self.all_sprites:
            if sprite in self.background_objects:
                sprite.draw(self.jeu, (sprite.img_rect.x + int(self.camera.offset.x),
                                       sprite.img_rect.y + int(self.camera.offset.y)))
            sprite.draw(self.jeu, (sprite.img_rect.x + int(self.camera.offset.x),
                                   sprite.img_rect.y + int(self.camera.offset.y)))
            """
            # draw les differents rect image et collision
            pg.draw.rect(self.jeu, ROUGE, (sprite.img_rect.x+int(self.camera.offset.x),
                                           sprite.img_rect.y+int(self.camera.offset.y),
                                           sprite.img_rect.w, sprite.img_rect.h), 1)
            pg.draw.rect(self.jeu, NOIR, (sprite.rect.x + int(self.camera.offset.x),
                                          sprite.rect.y + int(self.camera.offset.y),
                                          sprite.rect.w, sprite.rect.h), 1)
            """

    def render(self):
        """
        Appelée apres les update().
        pousse la surface temporaire sur l'écran visible
        """
        self.screen.blit(pg.transform.scale(self.jeu, (self.screen.get_width(), self.screen.get_height())), (0, 0))
        pg.display.flip()

    def boucle_principale(self):
        # load nouveau niveau
        if not self.quit:
            self.player = None
            self.new()
        while not self.quit:
            self.dt = self.clock.tick(FPS) / 1000  # en milisecondes
            self.event_handler()
            self.update()
            self.draw()
            self.render()

    def menu_principale(self):
        menu = MenuPrincipal(self)
        if menu.quit_jeu:
            self.quit = True
            return
        if menu.personnage == 'Melissa':
            self.anim_player_immobile = self.anim_Melissa_immobile
            self.anim_player_bouge = self.anim_Melissa_bouge
            self.anim_player_brake = self.anim_Melissa_brake
            self.anim_player_fall = self.anim_Melissa_fall
            self.anim_player_jump = self.anim_Melissa_jump
            self.anim_player_dash = self.anim_Melissa_dash
            self.img_player_atk = self.atk_Melissa_proche
        elif menu.personnage == 'Rosette':
            self.anim_player_immobile = self.anim_Rosette_immobile
            self.anim_player_bouge = self.anim_Rosette_bouge
            self.anim_player_brake = self.anim_Rosette_brake
            self.anim_player_fall = self.anim_Rosette_fall
            self.anim_player_jump = self.anim_Rosette_jump
            self.anim_player_dash = self.anim_Rosette_dash
            self.img_player_atk = self.atk_Rosette_proche
        elif menu.personnage == 'Luigi':
            self.anim_player_immobile = self.anim_Luigi_immobile
            self.anim_player_bouge = self.anim_Luigi_bouge
            self.anim_player_brake = self.anim_Luigi_brake
            self.anim_player_fall = self.anim_Luigi_fall
            self.anim_player_jump = self.anim_Luigi_jump
            self.anim_player_dash = self.anim_Luigi_dash
            self.img_player_atk = self.atk_Luigi_proche

    def run_level_editor(self):
        os.system("level_editor.py")
        #lvl_editor = LevelEditor(self.imgs_background, self.tiles_set, os.path.join("data", "Niveaux.txt"))
        #lvl_editor.boucle_principale()


def main():
    """
    Initialise la fenêtre, prépare la surface et initialise le programme
    """
    pg.init()
    app = App()
    # ---question d'optimation lors du level editor
    app.initialisation_variables()
    app.load_images()
    # --------------
    app.menu_principale()
    app.boucle_principale()
    on_quit()


def on_quit():
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
