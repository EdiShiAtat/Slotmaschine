from player import Player
from reel import *
from settings import *
from ui import UI
from wins import *
from gpiozero import Button
import pygame

class Machine:
    def __init__(self):
        self.display_surface = pygame.display.get_surface() # erstellt Fläche vom Fenster
        self.machine_balance = 10000.00 #Standardguthaben
        self.reel_index = 0 # Spuleindex
        self.reel_list = {} # Liste von den Spulen
        self.can_toggle = True # Kann man drehen
        self.spinning = False # Dreht es sich
        self.can_animate = False # Kann man die Animation durchlaufen lassen
        self.win_animation_ongoing = False # Ist im Moment die Gewinnanimation

        # Ergebnisse von den Spulen
        self.prev_result = {0: None, 1: None, 2: None, 3: None, 4: None}
        self.spin_result = {0: None, 1: None, 2: None, 3: None, 4: None}

        self.spawn_reels() # lädt die Spulen
        self.currPlayer = Player() # lädt die Player Klasse
        self.ui = UI(self.currPlayer) # lädt die UI Klasse mit der Player Klasse als Atribut

    def cooldowns(self):
        # Lässt den Spieler nur drehen, wenn sich alle Spulen nicht drehen
        for reel in self.reel_list: # für jede Spule
            if self.reel_list[reel].reel_is_spinning: # wenn Spule am drehen ist
                self.can_toggle = False # setzte Spule auf kann nicht drehen
                self.spinning = True # und setzte drehen auf True

        if not self.can_toggle and [self.reel_list[reel].reel_is_spinning for reel in self.reel_list].count(False) == 5: # wenn man die Spule nicht drehen kann und die Animation durch ist
            self.can_toggle = True # setzte Spule auf kann drehen
            self.spin_result = self.get_result() # speicher die Ergebnisse

            if self.check_wins(self.spin_result): # überprüfe, ob man gewonnen hat und gebe es aus
                self.win_data = self.check_wins(self.spin_result)
                self.pay_player(self.win_data, self.currPlayer)
                self.win_animation_ongoing = True
                self.ui.win_text_angle = random.randint(-4, 4)


    def input(self): # Funktion für den Input im Spiel
        
        keys = pygame.key.get_pressed() # Keyboard Variable
        spin = Button(2)
        reset = Button(3)

        # Überprüft, ob die Leertaste, die Fähigkeit zum Umschalten der Drehung und das Guthaben zur Deckung des Einsatzes ausreichen.
        # if keys[pygame.K_SPACE] and self.can_toggle and self.currPlayer.balance >= self.currPlayer.bet_size:

        # Überprüft, ob der Button auf GPIO 2, die Fähigkeit zum Umschalten der Drehung und das Guthaben zur Deckung des Einsatzes ausreichen.
        if spin.is_pressed and self.can_toggle and self.currPlayer.balance >= self.currPlayer.bet_size:
            self.toggle_spinning()
            self.spin_time = pygame.time.get_ticks()
            self.currPlayer.place_bet()
            self.machine_balance += self.currPlayer.bet_size
            self.currPlayer.last_payout = None
            
        # if keys[pygame.K_k] and self.can_toggle: # setzt das Guthaben auf 30 zurück, wenn K gedrückt wurde
        if reset.is_pressed and self.can_toggle: # setzt das Guthaben auf 30 zurück, wenn Button auf GPIO 3 gedrückt wurde
            self.currPlayer.balance = 30
                 
    #zeigt die Spulen an und animiert die Spulen
    def draw_reels(self, delta_time):
        for reel in self.reel_list:
            self.reel_list[reel].animate(delta_time)

    #erzeugt die Spulen
    def spawn_reels(self):
        if not self.reel_list:
            x_topleft, y_topleft = 10, -300
        while self.reel_index < 5:
            if self.reel_index > 0:
                x_topleft, y_topleft = x_topleft + (300 + X_OFFSET), y_topleft
            
            self.reel_list[self.reel_index] = Reel((x_topleft, y_topleft))
            self.reel_index += 1

    # Funktion für die Drehung
    def toggle_spinning(self):
        if self.can_toggle:
            self.spin_time = pygame.time.get_ticks()
            self.spinning = not self.spinning
            self.can_toggle = False

            for reel in self.reel_list:
                self.reel_list[reel].start_spin(int(reel) * 200)
                self.win_animation_ongoing = False

    # Funktion, um die Ergebnisse zu erhalten
    def get_result(self):
        for reel in self.reel_list:
            self.spin_result[reel] = self.reel_list[reel].reel_spin_result()
        return self.spin_result

    # überprüft, ob etwas gewonnen wurde
    def check_wins(self, result):
        hits = {}
        horizontal = flip_horizontal(result)
        for row in horizontal:
            for sym in row:
                # möglicher Gewinn
                if row.count(sym) > 2:
                    possible_win = [idx for idx, val in enumerate(row) if sym == val]

                    # Prüfe possible_win auf eine Teilsequenz, die länger als 2 ist, und füge sie zu den Treffern hinzu.
                    if len(longest_seq(possible_win)) > 2:
                        hits[horizontal.index(row) + 1] = [sym, longest_seq(possible_win)]
        if hits:
            self.can_animate = True
            return hits

    def pay_player(self, win_data, curr_player): # Funktion für die Auszahlung nach dem drehen, um den Spieler das Geld auszuzahlen
        multiplier = 0
        spin_payout = 0
        for v in win_data.values():
            multiplier += len(v[1])
        spin_payout = (multiplier * curr_player.bet_size)
        curr_player.balance += spin_payout
        self.machine_balance -= spin_payout
        curr_player.last_payout = spin_payout
        curr_player.total_won += spin_payout

    def win_animation(self): # Funktion für die Animation beim Gewinnen
        if self.win_animation_ongoing and self.win_data:
            for k, v in list(self.win_data.items()):
                if k == 1:
                    animationRow = 3
                elif k == 3:
                    animationRow = 1
                else:
                    animationRow = 2
                animationCols = v[1]
                for reel in self.reel_list:
                    if reel in animationCols and self.can_animate:
                        self.reel_list[reel].symbol_list.sprites()[animationRow].fade_in = True
                    for symbol in self.reel_list[reel].symbol_list:
                        if not symbol.fade_in:
                            symbol.fade_out = True

    def update(self, delta_time): # Funktion, die ständig Aktualisiert wird
        self.cooldowns()
        self.input()
        self.draw_reels(delta_time)
        for reel in self.reel_list:
            self.reel_list[reel].symbol_list.draw(self.display_surface)
            self.reel_list[reel].symbol_list.update()
        self.ui.update()
        self.win_animation()