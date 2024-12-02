# level editor par Guillaume Genois

import sys, os
import pygame as pg
from Platformer import App as platformer

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
FPS = 120
ESPACE_ENTRE_TILES = 10
DEPART_SURFACE_TILES = 25
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)


def load_img(nom_img, colorkey=True, folder="level_editor"):
    folder_path = os.path.join('image', folder)
    img = pg.image.load(os.path.join(folder_path, nom_img)).convert()
    # img = pg.image.load(nom_img).convert()
    if colorkey:
        img.set_colorkey(img.get_at((0, 0)), pg.RLEACCEL)
    # img = pg.transform.smoothscale(img, (int(size[0]), int(size[1])))
    return img


def insert_anim(nom_img, width, nb_frames):
    liste = []
    # folder_path = os.path.join('image', folder)
    img = pg.image.load(os.path.join(os.path.join('image', "level_editor"), nom_img)).convert()
    # img = pg.image.load(nom_img).convert()
    # img.set_alpha(None)
    img.set_colorkey(img.get_at((0, 0)), pg.RLEACCEL)
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
        liste.append(img.subsurface((i * frame_width, 0, frame_width, image_height)))
    return liste


class Button(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, img):
        pg.sprite.Sprite.__init__(self)
        self.default_image = pg.transform.smoothscale(img, (int(w), int(h)))
        self.image = self.default_image
        self.default_image_on = True
        self.rect = self.image.get_rect()
        self.rect.topleft = int(x), int(y)

    def update(self):
        pass

    def detect_if_collided(self, pos):
        if pg.Rect.collidepoint(self.rect, pos[0], pos[1]):
            return True
        return False

    def change_image(self, image):
        self.image = pg.transform.smoothscale(image, self.rect.size)
        self.default_image_on = False

    def reset_default_image(self):
        self.image = self.default_image
        self.default_image_on = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Tile(pg.sprite.Sprite):
    # layer = tile, tile, tile, ...
    # tile = x, y, w, h, img, type, ...
    def __init__(self, image, type="collider", rect=None, source_img=None):
        self.layer = 0
        self._layer = self.layer
        pg.sprite.Sprite.__init__(self)
        self.image = image  # peut etre garder l'image original sauvegarde pour agrandissement plus tard
        self.source_image = source_img
        self.rect = rect
        self.type = type
        self.being_drag = False
        self.being_click = False
        print(self.rect)

    def loading_new_img(self, image):
        self.source_image = image
        self.image = load_img(image[1], image[2], image[0])
        self.rect = self.image.get_rect()

    def postionner_in_menu(self, surface_w, position):
        # ---------------------------------------postionne dans le rectangle de choix
        plus_grand_cote = surface_w / 2 - ESPACE_ENTRE_TILES
        if max(self.rect.w, self.rect.h) == self.rect.w:
            self.image = pg.transform.smoothscale(self.image, (
                int(plus_grand_cote), int(plus_grand_cote / self.rect.w * self.rect.h)))
        elif max(self.rect.w, self.rect.h) == self.rect.h:
            self.image = pg.transform.smoothscale(self.image, (
                int(plus_grand_cote / self.rect.h * self.rect.w), int(plus_grand_cote)))
        self.rect = self.image.get_rect()

        if position % 2:
            self.rect.left = DEPART_SURFACE_TILES
        else:
            self.rect.right = int(surface_w) + ESPACE_ENTRE_TILES
        self.rect.top = int((plus_grand_cote + ESPACE_ENTRE_TILES) * int((position / 2)))# + ESPACE_ENTRE_TILES

    def update(self, *args):
        # update layer par rapport aux autres et au max
        pass

    def rotate(self):
        # tourner l'image autour du centre
        # +ctrl --> par 90 degre
        pass

    def delete(self):
        self.kill()

    def resize(self):
        # etirer l'image en agrandissant le rect
        # +ctrl --> pas etirer, mais repete le motif
        pass

    def modify_layers(self, layer):
        # modifie la layer, la profondeur de l'objet par rapport aux autres
        self.layer = layer
        # self._layer = self.layer

    def check_if_collided(self, pos):
        if pg.Rect.collidepoint(self.rect, pos[0], pos[1]):
            return True
        return False

    def draw(self, surface):
        # imprime sur un rectangle invisble que l'on deplace avec le scroll bar
        surface.blit(self.image, self.rect)


class ScrollBar(pg.sprite.Sprite):
    def __init__(self, x, y, w, total_h_tiles, image):
        pg.sprite.Sprite.__init__(self)
        h = min(SCREEN_HEIGHT, SCREEN_HEIGHT/total_h_tiles*SCREEN_HEIGHT)
        self.image = pg.transform.smoothscale(image, (int(w), int(h)))
        self.rect = self.image.get_rect()
        self.rect.topright = int(x - w), int(y)
        if self.rect.h < SCREEN_HEIGHT:
            self.can_move = True
        else:
            self.can_move = False

        self.old_pos = self.rect.center

    def update(self, delta):
        self.old_pos = self.rect.center
        self.rect.y -= delta

        # gestion bords
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def detect_if_collided(self, pos):
        if pg.Rect.collidepoint(self.rect, pos[0], pos[1]):
            return True
        return False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class App:
    """
    Gestion du program flow et des evenements
    """
    def __init__(self, all_imgs_bckg, tiles_set, fichier):
        """
        Creation de l'objet rectangle apres avoir initialisé et recuperer
        la surface de la fenêtre
        """
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("LEVEL EDITOR")

        self.background = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill(BLANC)

        self.quit = False

        # creation des variables des events
        self.keys = pg.key.get_pressed()
        self.mouse_click = False
        self.release_mouse = True
        self.scroll_bar_drag = False
        self.old_pos_mouse = None
        self.pos_mouse = None
        self.ctrl_is_on = False

        # gestion de l'horloge et du fps max
        self.clock = pg.time.Clock()
        self.clock.tick(60)

        # variables necesaires peu importe le jeu
        self.all_imgs_bckg = all_imgs_bckg
        self.tiles_set = tiles_set  # pleins d'images
        self.fichier = fichier
        self.all_sprites = pg.sprite.Group()
        self.liste_layers = [[]]  # [premiere liste de layer]
        self.liste_tiles = pg.sprite.Group()  # pour draw et gerer plus facilement
        # liste_layers = layer, layer, layer, layer, ...
        # layer = tile, tile, tile, ...
        # tile = x, y, w, h, img, type

        # initier le tiles set
        self.tiles_set_length = len(self.tiles_set)  # nb de tiles dans le set
        self.tiles_set_w = 2
        self.tiles_set_h = round(self.tiles_set_length / self.tiles_set_w)

        # images du editor
        self.exit_images = [load_img('ExitSign_A1.png', True), load_img('ExitSign_A2.png', True)]
        self.add_lvl_images = insert_anim('add level butttons.png', 50, 3)
        self.delete_all_images = insert_anim('delete all buttons.png', 50, 3)
        self.scroll_bar_image = load_img('Cloud_Gray.png', True)  # rotationner a 90

        # objets
        self.exit_button = Button(SCREEN_WIDTH-50-25, 25, 50, 25, self.exit_images[0])
        self.delete_all_button = Button(SCREEN_WIDTH-50-25, SCREEN_HEIGHT-5-50, 50, 50, self.delete_all_images[0])
        self.add_lvl_button = Button(SCREEN_WIDTH-50-25, self.delete_all_button.rect.top-5-50, 50, 50,
                                     self.add_lvl_images[0])
        self.tiles_in_menu = []
        self.total_h_tiles = 0
        for position, tile in enumerate(self.tiles_set):
            obj = Tile(tile)  # ajoouter le type
            self.tiles_in_menu.append(obj)
            obj.loading_new_img(tile)
            obj.postionner_in_menu(SCREEN_WIDTH * 1 / 5, position)
            self.total_h_tiles = max(self.total_h_tiles, obj.rect.bottom)
        self.scroll_bar = ScrollBar(DEPART_SURFACE_TILES, 0, 10,
                                    self.total_h_tiles, self.scroll_bar_image)
        self.all_buttons = [(self.exit_button, self.exit_images, "exit"),
                            (self.add_lvl_button, self.add_lvl_images, "add_lvl"),
                            (self.delete_all_button, self.delete_all_images, "delete_all")]

        # bckg au choix
        self.choose_bckg()

        print(self.total_h_tiles)

    def event_handler(self):
        """
        capture des évenements clavier
        """
        self.mouse_click = False
        self.right_click = False  # pour faire ouvrir une fenetre de choix
        self.keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.quit = True
            if self.keys[pg.K_LCTRL] or self.keys[pg.K_RCTRL]:
                self.ctrl_is_on = not self.ctrl_is_on
            elif event.type == pg.MOUSEBUTTONDOWN:
                print(event.button)
                print(pg.mouse.get_pressed())
                self.mouse_click = True
                # self.mouse_down = True
                self.release_mouse = False
            elif event.type == pg.MOUSEBUTTONUP:
                print(event.button)
                self.release_mouse = True
                self.scroll_bar_drag = False

    def update(self):
        """
        Mise à jour des attributs de chaque rectangle en fonction des
        évènements capturés
        """
        self.old_pos_mouse = self.pos_mouse
        self.pos_mouse = pg.mouse.get_pos()

        # ----------------------------------------------------------------buttons
        for button in self.all_buttons:
            if button[0].detect_if_collided(self.pos_mouse):
                button[0].change_image(button[1][1])
                if self.mouse_click:
                    if button[2] == "exit":
                        self.do_quit()
                    elif button[2] == "add_lvl":
                        self.save()
                        # self.delete_all()
                    elif button[2] == "delete_all":
                        self.delete_all()
            else:
                if not button[0].default_image_on:
                    button[0].reset_default_image()

        # ---------------------------------------------------------------scroll bar
        if self.scroll_bar.can_move:
            if self.scroll_bar.detect_if_collided(self.pos_mouse) and self.mouse_click:
                self.scroll_bar_drag = True
            if self.scroll_bar_drag and self.release_mouse is False:
                delta = self.old_pos_mouse[1] - self.pos_mouse[1]
                print("delta " + str(delta))
                self.scroll_bar.update(delta)
                deplacement = round(self.total_h_tiles*(self.scroll_bar.old_pos[1]-self.scroll_bar.rect.center[1])
                                    / SCREEN_HEIGHT)  # produit croise
                """for tile in self.tiles_in_menu:
                    if tile.rect.top < SCREEN_HEIGHT - self.total_h_tiles:
                        # tile.rect.top = SCREEN_HEIGHT - self.total_h_tiles
                        deplacement = -deplacement
                        print("sommet atteint")
                    elif tile.rect.bottom > self.total_h_tiles:
                        # tile.rect.bottom = self.total_h_tiles
                        deplacement = -deplacement
                        print("bas atteint")
                    # print(tile.rect)"""  # fait tout bug, pas necessaire
                for tile in self.tiles_in_menu:
                    tile.rect.y += deplacement
                print("deplacement " + str(deplacement))

        # ----------------------------------------------------------tiles
        # en ajouter un a partir du menu
        for tile in self.tiles_in_menu:
            if tile.check_if_collided(self.pos_mouse) and self.mouse_click:
                new_tile = Tile(tile.image.copy(), tile.type, tile.rect.copy(), tile.source_image)
                new_tile.being_drag = True
                self.liste_tiles.add(new_tile)
        # gerer ceux existant
        for tile in self.liste_tiles:
            # verifier si cliquer
            if not tile.being_drag:
                if tile.check_if_collided(self.pos_mouse) and self.mouse_click:
                    tile.being_drag = True
            # bouger
            if tile.being_drag and self.release_mouse:
                tile.being_drag = False  # arrete de bouger lorsque souris relache
            elif tile.being_drag and not self.release_mouse:
                tile.rect.center = self.pos_mouse
                # positionne dans quadrille si pas ctrl d'appuyer
                if not self.ctrl_is_on:  # peut-etre flag
                    tile.rect.center = round(tile.rect.centerx / tile.rect.w) * tile.rect.w, \
                                       round(tile.rect.centery / tile.rect.h) * tile.rect.h

    def draw(self):
        """
        Dessine tout ce qu'il y a a dessiner sur la surface
        """
        self.screen.blit(self.background, (0, 0))
        for tile in self.tiles_in_menu:
            tile.draw(self.screen)
        for button in self.all_buttons:
            button[0].draw(self.screen)
        for tile in self.liste_tiles:
            tile.draw(self.screen)
        self.scroll_bar.draw(self.screen)

    def render(self):
        """
        Appelée apres les update().
        pousse la surface temporaire sur l'écran visible
        """
        pg.display.flip()

    def boucle_principale(self):
        while not self.quit:
            self.clock.tick(FPS)
            self.event_handler()
            self.update()
            self.draw()
            self.render()

    def new_level(self):
        # check if save
        # delete all et refresh les listes
        # choisi a nouveau le bckg parmis les choix
        pass

    def choose_bckg(self):
        # choisi un nouveau bckg
        # parmi les choix disponibles
        # adapter la taille selon le nombre
        self.background = self.all_imgs_bckg[0]
        pass

    def save(self):
        # incorpore les tiles dans la liste de layers en fonction de leur layer (profondeur)
        for tile in self.liste_tiles:
            if tile.layer > len(self.liste_layers)-1:
                layer = [tile]
                self.liste_layers.append(layer)
            else:
                self.liste_layers[tile.layer].append(tile)
        # enregistre dans le fichier donner
        # une ligne par layer, couche, la profondeur
        # ligne = obj; obj; obj; obj; ...
        # obj = x, y, w, h, img, type
        with open(self.fichier, 'a') as file:
            for layer in self.liste_layers:
                for tile in layer:
                    file.write("{0},{1},{2},{3},{4},{5};".format(tile.rect.x, tile.rect.y, tile.rect.w,
                                                                 tile.rect.h, tile.source_image, tile.type))
                file.write("\n")

    def do_quit(self):
        self.quit = True

    def delete_all(self):
        # demande si sur ou non
        # refresh toutes les listes, mais garde meme bckg
        self.liste_layers = []
        self.liste_tiles = pg.sprite.Group()


def main():
    """
    Initialise la fenêtre, prépare la surface et initialise le programme
    """
    pg.init()
    plat = platformer()
    plat.load_images()
    app = App(plat.imgs_background, plat.tiles_set, os.path.join("data", "Niveaux.txt"))
    app.boucle_principale()
    on_quit()


def on_quit():
    print("Merci et aurevoir...")
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
