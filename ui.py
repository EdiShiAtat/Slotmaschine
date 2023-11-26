from player import Player
from settings import *
import pygame, random

class UI:
    def __init__(self, player):
        self.player = player #Erstellt Objekt von der Klasse Player
        self.display_surface = pygame.display.get_surface() #erstellt UI Grundfläche
        try: # lädt die Schrift
            self.font, self.bet_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE), pygame.font.Font(UI_FONT, UI_FONT_SIZE)
            self.win_font = pygame.font.Font(UI_FONT, WIN_FONT_SIZE)
        except: # Falls Schrift nicht lädt, dann gebe das unten in der Konsole aus
            print("Error loading font!")
            print(f"Currently, the UI_FONT variable is set to {UI_FONT}")
            print("Does the file exist?")
            quit()
        self.win_text_angle = random.randint(-4, 4) # Gewinntext mit zufälliger Neigung

    def display_info(self):
        player_data = self.player.get_data() # lädt daten von der Klasse Player

        # Zeigt den Guthaben an und setzt die Platzierung vom Text
        balance_surf = self.font.render("Guthaben: €" + player_data['balance'], True, TEXT_COLOR, None)
        x, y = 20, self.display_surface.get_size()[1] - 30
        balance_rect = balance_surf.get_rect(bottomleft = (x, y))

        # Zeigt den Einsatz an und setzt die Platzierung vom Text
        bet_surf = self.bet_font.render("Einsatz: €" + player_data['bet_size'], True, TEXT_COLOR, None)
        x = self.display_surface.get_size()[0] - 20
        bet_rect = bet_surf.get_rect(bottomright = (x, y))

        # zeigt die Spielerdaten an
        pygame.draw.rect(self.display_surface, False, balance_rect)
        pygame.draw.rect(self.display_surface, False, bet_rect)
        self.display_surface.blit(balance_surf, balance_rect)
        self.display_surface.blit(bet_surf, bet_rect)

        # Zeigt den letzten Gewinn an und setzt die Platzierung vom Text
        if self.player.last_payout:
            last_payout = player_data['last_payout']
            win_surf = self.win_font.render("WIN! €" + last_payout, True, TEXT_COLOR, None)
            x1 = 800
            y1 = self.display_surface.get_size()[1] - 60
            win_surf = pygame.transform.rotate(win_surf, self.win_text_angle)
            win_rect = win_surf.get_rect(center = (x1, y1))
            self.display_surface.blit(win_surf, win_rect)

    def update(self): #Funktion, die ständig Aktualisiert wird
        color = (0x00, 0x00, 0x00, 0x00) # Farbe schwarz
        pygame.draw.rect(self.display_surface , color, pygame.Rect(0, 900, 2000, 500)) # Setzt den Schwarzen Balken auf der Unterseite
        self.display_info()