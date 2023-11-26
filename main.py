from machine import Machine
from settings import *
import ctypes, pygame, sys
from machine import *

class Game:
    def __init__(self):

        # Allgemeine Einstellungen
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN) # sellt Spiel auf Fullscreen

        pygame.display.set_caption('Slot Machine Projekt') # Überschrift vom Fenster
        self.clock = pygame.time.Clock() # erstellt ein Objekt für die Zeiterfassung
        self.bg_image = pygame.image.load(BG_IMAGE_PATH).convert_alpha() # erstellt ein Objekt für das Hintergrundbild
        self.grid_image = pygame.image.load(GRID_IMAGE_PATH).convert_alpha() # erstellt ein Objekt für das Gitterbild

        self.machine = Machine() # erstellt ein Objekt von der Klasse "Machine"
        self.delta_time = 0 # Variable für die Zeit

    def run(self):

        self.start_time = pygame.time.get_ticks() # gibt in millisekunden an, wie viele millisekunden seit dem pygame.init() Abruf vergangen sind

        while True: # Dauerschleife
            # Reguliert den quit operation (Standardcode für Pygame)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Zeitvariablen
            self.delta_time = (pygame.time.get_ticks() - self.start_time) / 1000
            self.start_time = pygame.time.get_ticks()

            #Updatet das Bild
            pygame.display.update()
            self.screen.blit(self.bg_image, (0, 0))
            self.machine.update(self.delta_time)
            self.screen.blit(self.grid_image, (0, 0))
            self.clock.tick(FPS)

if __name__ == '__main__':  # startet das Spiel, wenn dieser Script ausgeführt wird
    game = Game()
    game.run()