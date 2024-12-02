# platforma pour Platformer
import pygame as pg
import os
from engine.constants import *


class Pause:
    def __init__(self, jeu, surface):
        self.jeu = jeu
        # setup bool
        self.quit_jeu = False
        self.choix = False
        self.mouse_down = False
        self.final_pos = False
        self.fullscreen = jeu.fullscreen

        # setup screen
        self.keys = pg.key.get_pressed()
        if self.fullscreen:
            self.screen = pg.display.set_mode((jeu.ecran_w, jeu.ecran_h), pg.FULLSCREEN)
        elif not self.fullscreen:
            self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
        self.surface = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        # images
        self.anim_boutton_quitter = jeu.anim_boutton_quitter
        # todo: fullscreen expand fonctionne pas, les rect sont decales (scale?)

        # objets a l'ecran
        self.continuer = pg.Surface((200, 50))
        self.continuer_rect = self.continuer.get_rect(right=0, top=50)
        self.customizer_keys = pg.Surface((200, 50))
        self.customizer_keys_rect = self.customizer_keys.get_rect(top=self.continuer_rect.bottom+100, right=0)
        self.quitter = self.anim_boutton_quitter[0]
        self.quitter_rect = self.quitter.get_rect(top=self.customizer_keys_rect.bottom+100, right=0)
        self.liste_rect = [self.continuer_rect, self.customizer_keys_rect, self.quitter_rect]

        # background
        self.background = surface  # comprends pas pk jeu.screen.copy() fonctionne pas
        self.background.set_alpha(100)
        while not self.choix:
            self.mouse_down = False
            # event
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.choix = True
                    self.quit_jeu = True
                # pour bouger avec les flèches
                elif event.type in (pg.KEYUP, pg.KEYDOWN):
                    self.keys = pg.key.get_pressed()
                    if event.type == pg.KEYDOWN:
                        if self.keys[K_FULLSCREEN]:
                            self.fullscreen = not self.fullscreen
                            if self.fullscreen:
                                self.screen = pg.display.set_mode((jeu.ecran_w, jeu.ecran_h), pg.FULLSCREEN)
                            else:
                                self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)

                        if self.keys[pg.K_ESCAPE]:
                            if self.fullscreen:
                                self.fullscreen = not self.fullscreen
                                self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
                            else:
                                self.choix = True
                                self.quit_jeu = True
                    if event.type == pg.KEYUP:
                        if event.key == K_PAUSE:
                            self.choix = True
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.mouse_down = True
            self.update()
            self.draw()
    
    def update(self):
        mx, my = pg.mouse.get_pos()
        # animation arriver
        if not self.final_pos:
            self.animation_ouverture()

        if self.final_pos:
            # boutton continuer
            if pg.Rect.collidepoint(self.continuer_rect, mx, my):
                self.continuer.fill(VERT)
                if self.mouse_down:
                    self.choix = True
            else:
                self.continuer.fill(ROUGE)

            # boutton customizer
            if pg.Rect.collidepoint(self.customizer_keys_rect, mx, my):
                self.customizer_keys.fill(BLEU)
                if self.mouse_down:
                    menu = MenuCustomKeys(self.jeu, self.background)
                    if menu.quit_jeu:
                        self.choix = True
                        self.quit_jeu = True
            else:
                self.customizer_keys.fill(BRUN)

            # boutton quitter
            if pg.Rect.collidepoint(self.quitter_rect, mx, my):
                # center = self.quitter_rect.center
                self.quitter = self.anim_boutton_quitter[1]
                # self.quitter_rect = self.quitter.get_rect(center=center)

                if self.mouse_down:
                    self.choix = True
                    self.quit_jeu = True
            else:
                # center = self.quitter_rect.center
                self.quitter = self.anim_boutton_quitter[0]
                # self.quitter_rect = self.quitter.get_rect(center=center)

            for rect in self.liste_rect:
                if rect.centerx != self.screen.get_width()/2:
                    rect.centerx = self.screen.get_width()/2
    
    def draw(self):
        # draw
        pg.draw.rect(self.surface, NOIR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surface.blit(self.background, (0, 0))

        # render
        self.screen.blit(pg.transform.scale(self.surface, (self.screen.get_width(), self.screen.get_height())), (0, 0))
        self.screen.blit(self.continuer, self.continuer_rect)
        self.screen.blit(self.customizer_keys, self.customizer_keys_rect)
        self.screen.blit(self.quitter, self.quitter_rect)
        pg.display.flip()

    def animation_ouverture(self):
        for rect in self.liste_rect:
            if rect.centerx < SCREEN_WIDTH / 2:
                scroll = (SCREEN_WIDTH / 2 + 100 - rect.centerx) / 50
                rect.centerx += scroll
                self.final_pos = False
            else:
                self.final_pos = True


class MenuPrincipal:
    def __init__(self, jeu):
        # setup
        self.quit_jeu = False
        self.choix = False
        self.mouse_down = False
        self.personnage = None
        self.last_update = 0
        self.frame_index = 0
        self.fullscreen = jeu.fullscreen
        self.font_64 = pg.font.SysFont("arial", 64)
        self.font_32 = pg.font.SysFont("arial", 32)
        self.font_20 = pg.font.SysFont("arial", 20)

        # setup screen
        self.keys = pg.key.get_pressed()
        if self.fullscreen:
            self.screen = pg.display.set_mode((jeu.ecran_w, jeu.ecran_h), pg.FULLSCREEN)
        elif not self.fullscreen:
            self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)

        # images
        self.anim_Melissa = []
        for img in jeu.anim_Melissa_bouge:
            img = pg.transform.scale(img, (150, 200))
            self.anim_Melissa.append(img)
        self.anim_Rosette = []
        for img in jeu.anim_Rosette_bouge:
            img = pg.transform.scale(img, (150, 200))
            self.anim_Rosette.append(img)
        self.anim_Luigi = []
        for img in jeu.anim_Luigi_bouge:
            img = pg.transform.scale(img, (150, 200))
            self.anim_Luigi.append(img)
        self.anim_boutton_quitter = []
        for img in jeu.anim_boutton_quitter:
            img = pg.transform.scale(img, (75, 40))
            self.anim_boutton_quitter.append(img)

        # ------------------------------objets
        # Melissa
        self.Melissa = self.anim_Melissa[0]
        self.Melissa_rect = self.Melissa.get_rect(right=self.screen.get_width()-100, top=175)
        self.Melissa_couleur = NOIR
        self.Melissa_texte = self.font_20.render("Melissa", True, GRIS)
        # Rosette
        self.Rosette = self.anim_Rosette[0]
        self.Rosette_rect = self.Rosette.get_rect(left=100, top=175)
        self.Rosette_couleur = NOIR
        self.Rosette_texte = self.font_20.render("Rosette", True, GRIS)
        # Luigi
        self.Luigi = self.anim_Luigi[0]
        self.Luigi_rect = self.Luigi.get_rect(centerx=SCREEN_WIDTH/2, top=175)
        self.Luigi_couleur = NOIR
        self.Luigi_texte = self.font_20.render("Luigi", True, GRIS)
        # Quitter
        self.quitter = self.anim_boutton_quitter[0]
        self.quitter_rect = self.quitter.get_rect(bottom=self.screen.get_height() - 50, right=self.screen.get_width()-50)
        # ajouter autres personnages
        self.liste_rect = [self.Melissa_rect, self.quitter_rect]

        # background
        self.background = jeu.imgs_background[1]
        # self.titre = jeu.ecrire_texte(jeu.font_personnaliser, TITRE, (25, 50))
        self.titre = self.font_64.render(TITRE, True, MAUVE)
        self.instructions = self.font_32.render("Choisissez votre personnage!", True, ROUGE)

        while not self.choix:
            self.mouse_down = False
            # event
            for event in pg.event.get():
                if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                    self.choix = True
                    self.quit_jeu = True
                # pour bouger avec les flèches
                elif event.type in (pg.KEYUP, pg.KEYDOWN):
                    self.keys = pg.key.get_pressed()
                    if event.type == pg.KEYUP:
                        if event.key == K_PAUSE:
                            self.choix = True
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.mouse_down = True
            self.update()
            self.draw()

    def update(self):
        mx, my = pg.mouse.get_pos()
        now = pg.time.get_ticks()

        # boutton Melissa
        if pg.Rect.collidepoint(self.Melissa_rect, mx, my):
            if now - self.last_update > 100:
                self.Melissa, self.Melissa_rect = self.animation(self.anim_Melissa, self.Melissa_rect)
                self.last_update = now
            self.Melissa_couleur = ROUGE
            if self.mouse_down:
                self.choix = True
                self.personnage = 'Melissa'
        else:
            self.Melissa = self.anim_Melissa[0]
            self.Melissa_couleur = NOIR

        # boutton Rosette
        if pg.Rect.collidepoint(self.Rosette_rect, mx, my):
            if now - self.last_update > 100:
                self.Rosette, self.Rosette_rect = self.animation(self.anim_Rosette, self.Rosette_rect)
                self.last_update = now
            self.Rosette_couleur = ROUGE
            if self.mouse_down:
                self.choix = True
                self.personnage = 'Rosette'
        else:
            self.Rosette = self.anim_Rosette[0]
            self.Rosette_couleur = NOIR

        # boutton Luigi
        if pg.Rect.collidepoint(self.Luigi_rect, mx, my):
            if now - self.last_update > 100:
                self.Luigi, self.Luigi_rect = self.animation(self.anim_Luigi, self.Luigi_rect)
                self.last_update = now
            self.Luigi_couleur = ROUGE
            if self.mouse_down:
                self.choix = True
                self.personnage = 'Luigi'
        else:
            self.Luigi = self.anim_Luigi[0]
            self.Luigi_couleur = NOIR

        # boutton Quitter
        if pg.Rect.collidepoint(self.quitter_rect, mx, my):
            self.quitter = self.anim_boutton_quitter[1]
            if self.mouse_down:
                self.choix = True
                self.quit_jeu = True
        else:
            self.quitter = self.anim_boutton_quitter[0]

    def animation(self, anim, rect):
        center = rect.center
        self.frame_index = (self.frame_index + 1) % len(anim)
        image = anim[self.frame_index]
        rect = image.get_rect()
        rect.center = center
        return image, rect

    def draw(self):
        # --------------draw
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.titre, (self.screen.get_width()/2-self.titre.get_width()/2, 10))
        self.screen.blit(self.instructions, (self.screen.get_width()/2-self.instructions.get_width()/2, 80))
        # Melissa
        self.screen.blit(self.Melissa, self.Melissa_rect)
        pg.draw.rect(self.screen, self.Melissa_couleur, self.Melissa_rect, 2)
        self.screen.blit(self.Melissa_texte, (self.Melissa_rect.centerx-self.Melissa_texte.get_width()/2,
                                              self.Melissa_rect.y-self.Melissa_texte.get_height()))
        # Rosette
        self.screen.blit(self.Rosette, self.Rosette_rect)
        pg.draw.rect(self.screen, self.Rosette_couleur, self.Rosette_rect, 2)
        self.screen.blit(self.Rosette_texte, (self.Rosette_rect.centerx - self.Rosette_texte.get_width() / 2,
                                              self.Rosette_rect.y - self.Rosette_texte.get_height()))
        # Luigi
        self.screen.blit(self.Luigi, self.Luigi_rect)
        pg.draw.rect(self.screen, self.Luigi_couleur, self.Luigi_rect, 2)
        self.screen.blit(self.Luigi_texte, (self.Luigi_rect.centerx - self.Luigi_texte.get_width() / 2,
                                              self.Luigi_rect.y - self.Luigi_texte.get_height()))
        # Quitter
        self.screen.blit(self.quitter, self.quitter_rect)
        # render
        pg.display.flip()


class GameOverScreen:
    def __init__(self, surface):
        self.quit_jeu = False
        self.choix = False
        self.mouse_down = False
        self.keys = pg.key.get_pressed()
        self.jeu = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.set_alpha(100)
        self.jeu.blit(surface)
        while not self.choix:
            self.mouse_down = False
            # event
            for event in pg.event.get():
                if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                    self.choix = True
                    self.quit_jeu = True
                # pour bouger avec les flèches
                elif event.type in (pg.KEYUP, pg.KEYDOWN):
                    self.keys = pg.key.get_pressed()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.mouse_down = True
            self.update()
            self.draw()

    def update(self):
        pass

    def draw(self):
        # draw
        # render
        pg.display.flip()


class MenuCustomKeys:
    def __init__(self, jeu, surface):
        self.current_keys = jeu.current_keys
        self.default_keys = KEYS
        self.jeu = jeu
        self.font = pg.font.SysFont("arial", 32)
        self.texte_deux_points = self.font.render('  :  ', True, BLANC)
        # setup bool
        self.quit_jeu = False
        self.back = False
        self.mouse_down = False
        self.en_train_de_choisir = False
        self.touche_a_changer = None
        self.release_mouse = True
        self.fullscreen = jeu.fullscreen

        # setup screen
        self.keys = pg.key.get_pressed()
        if self.fullscreen:
            self.screen = pg.display.set_mode((jeu.ecran_w, jeu.ecran_h), pg.FULLSCREEN)
        elif not self.fullscreen:
            self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
        self.surface = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        # images
        self.anim_boutton_quitter = jeu.anim_boutton_quitter
        # todo: fullscreen expand fonctionne pas, les rect sont decales (scale?)

        # objets a l'ecran
        self.retour = pg.Surface((100, 50))
        self.retour_rect = self.retour.get_rect(left=15, top=20)
        self.quitter = self.anim_boutton_quitter[0]
        self.quitter_rect = self.quitter.get_rect(right=SCREEN_WIDTH-15, bottom=SCREEN_HEIGHT-20)
        last_bottom = 100
        self.keys_afficher = []
        for action in self.current_keys:
            rect = pg.Rect((0, last_bottom, 300, self.font.get_height()))
            rect.centerx = SCREEN_WIDTH/2
            act_pos = pg.math.Vector2(rect.centerx/2, rect.centery)
            key_pos = pg.math.Vector2(rect.centerx * 3/2, rect.centery)
            self.keys_afficher.append([rect, [action, act_pos], [self.current_keys[action], key_pos], ORANGE])
            last_bottom = rect.bottom
        self.liste_rect = [self.retour_rect, self.quitter_rect, self.keys_afficher]
        print(self.keys_afficher)

        # background
        self.background = surface  # comprends pas pk jeu.screen.copy() fonctionne pas
        self.background.set_alpha(100)
        while not self.back:
            self.mouse_down = False
            # event
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.back = True
                    self.quit_jeu = True
                # pour bouger avec les flèches
                elif event.type in (pg.KEYUP, pg.KEYDOWN):
                    self.keys = pg.key.get_pressed()
                    if event.type == pg.KEYDOWN:
                        if self.keys[K_FULLSCREEN]:
                            self.fullscreen = not self.fullscreen
                            if self.fullscreen:
                                self.screen = pg.display.set_mode((jeu.ecran_w, jeu.ecran_h), pg.FULLSCREEN)
                            else:
                                self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)

                        if self.keys[pg.K_ESCAPE]:
                            if self.fullscreen:
                                self.fullscreen = not self.fullscreen
                                self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
                            else:
                                self.back = True
                                self.quit_jeu = True
                    if event.type == pg.KEYUP:
                        if event.key == K_PAUSE:
                            self.back = True
                elif event.type == pg.MOUSEBUTTONDOWN:
                    print("mouse button down")
                    self.mouse_down = True
                    self.release_mouse = False
                elif event.type == pg.MOUSEBUTTONUP:
                    print("mouse button up")
                    self.release_mouse = True
            self.update()
            self.draw()

    def update(self):
        mx, my = pg.mouse.get_pos()

        if not self.en_train_de_choisir:
            # boutton retour/sauvegarder
            if pg.Rect.collidepoint(self.retour_rect, mx, my):
                self.retour.fill(VERT)
                if self.mouse_down:
                    for chose in self.keys_afficher:
                        self.current_keys[chose[1][0]] = chose[2][0]
                    self.modify_fichier_customizations()
                    self.back = True
            else:
                self.retour.fill(ROUGE)

            # boutton quitter
            if pg.Rect.collidepoint(self.quitter_rect, mx, my):
                # center = self.quitter_rect.center
                self.quitter = self.anim_boutton_quitter[1]
                # self.quitter_rect = self.quitter.get_rect(center=center)

                if self.mouse_down:
                    self.back = True
                    self.quit_jeu = True
            else:
                # center = self.quitter_rect.center
                self.quitter = self.anim_boutton_quitter[0]
                # self.quitter_rect = self.quitter.get_rect(center=center)

            # differentes touches
            for chose in self.keys_afficher:
                if pg.Rect.collidepoint(chose[0], mx, my):
                    chose[3] = VERT
                    if self.mouse_down:
                        self.en_train_de_choisir = True
                        self.touche_a_changer = chose
                        pass  # clignote la couleur (switch)
                else:
                    chose[3] = ORANGE

        if self.en_train_de_choisir:
            for key in self.keys:
                if key not in (pg.K_i, K_PAUSE, pg.K_ESCAPE) and key:
                    self.touche_a_changer[2][0] = self.keys.index(key)
                    self.en_train_de_choisir = False
                    print(key)
            if self.release_mouse:
                if self.mouse_down:
                    self.en_train_de_choisir = False

    def draw(self):
        # draw
        pg.draw.rect(self.surface, NOIR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surface.blit(self.background, (0, 0))

        # render
        self.screen.blit(pg.transform.scale(self.surface, (self.screen.get_width(), self.screen.get_height())), (0, 0))
        self.screen.blit(self.retour, self.retour_rect)
        self.screen.blit(self.quitter, self.quitter_rect)
        for chose in self.keys_afficher:
            # self.keys_afficher.append([rect, [action, act_pos], [self.current_keys[action], key_pos], ORANGE])
            texte_action = self.font.render(str(chose[1][0]), True, BLANC)
            texte_key = self.font.render(str(pg.key.name(chose[2][0])), True, BLANC)
            #                texte     rect
            self.screen.blit(texte_action, chose[1][1] -
                             pg.math.Vector2(texte_action.get_width()/2, texte_action.get_height()/2))
            self.screen.blit(self.texte_deux_points, chose[0].center -
                            pg.math.Vector2(self.texte_deux_points.get_width()/2, self.texte_deux_points.get_height()/2))
            self.screen.blit(texte_key, chose[2][1] -
                             pg.math.Vector2(texte_key.get_width()/2, texte_key.get_height()/2))
            #                         color     rect
            pg.draw.rect(self.screen, chose[3], chose[0], 1)
        pg.display.flip()

    def modify_fichier_customizations(self):
        print(self.current_keys)
        # self.keys_afficher.append([rect, [action, act_pos], [self.current_keys[action], key_pos], ORANGE])
        with open(os.path.join("data", "Customizations.txt"), 'w') as file:
            for action in self.current_keys:
                file.write("{0}:{1}\n".format(action, self.current_keys[action]))
            print(file)

