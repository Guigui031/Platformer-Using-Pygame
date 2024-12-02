import pygame, sys

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 400
FPS = 120

PS4_KEYS = {"x": 0,
  "circle": 1,
  "square": 2,
  "triangle": 3,
  "share": 4,
  "PS": 5,
  "options": 6,
  "left_stick_click": 7,
  "right_stick_click": 8,
  "L1": 9,
  "R1": 10,
  "up_arrow": 11,
  "down_arrow": 12,
  "left_arrow": 13,
  "right_arrow": 14,
  "touchpad": 15}


class App:
    """
    Gestion du program flow et des evenements
    """

    def __init__(self):
        """
        Creation de l'objet rectangle apres avoir initialisé et recuperer
        la surface de la fenêtre
        """

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("TITRE")

        self.quit = False

        # creation des variables des events
        self.keys = pygame.key.get_pressed()

        # Initialize controller
        '''
        joysticks = []
        for i in range(pygame.joystick.get_count()):
            joysticks.append(pygame.joystick.Joystick(i))
        for joystick in joysticks:
            joystick.init()
        '''

        #print(joysticks)
        self.j = pygame.joystick.Joystick(0)
        self.j.init()
        print(self.j)
        print(self.j.get_button(6))

        # gestion de l'horloge et du fps max
        self.clock = pygame.time.Clock()
        self.clock.tick(60)

    def event_handler(self):
        """
        capture des évenements clavier
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                self.quit = True

            if event.type == pygame.JOYBUTTONUP:
                for button in PS4_KEYS:
                    if event.button == PS4_KEYS[button]:
                        print(button)
                        return

    def update(self):
        """
        Mise à jour des attributs de chaque rectangle en fonction des
        évènements capturés
        """
        pass

    def draw(self):
        """
        Dessine tout ce qu'il y a a dessiner sur la surface
        """
        pass

    def render(self):
        """
        Appelée apres les update().
        pousse la surface temporaire sur l'écran visible
        """
        pygame.display.flip()

    def boucle_principale(self):
        while not self.quit:
            self.clock.tick(FPS)
            self.event_handler()
            self.update()
            self.draw()
            self.render()


def main():
    """
    Initialise la fenêtre, prépare la surface et initialise le programme
    """
    pygame.init()
    app = App()
    app.boucle_principale()
    on_quit()


def on_quit():
    print("Merci et aurevoir...")
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
