from settings import * # importiert benötigte Bibliotheken
import pygame, random

class Reel:
    def __init__(self, pos):
        self.symbol_list = pygame.sprite.Group() # lädt Symbole
        self.shuffled_keys = list(symbols.keys()) # wird eine Liste von Zahlen (keys) generiert
        random.shuffle(self.shuffled_keys) # Ändert zufällig die Reihenfolge von den keys
        self.shuffled_keys = self.shuffled_keys[:5] # die Liste von keys wird auf die ersten 5 abgeschnitten

        self.reel_is_spinning = False # Zustand, ob Slotmaschine im Moment dreht oder nicht.

        for idx, item in enumerate(self.shuffled_keys): # durchläuft die Liste self.shuffled_keys und weist jedem Element item und seinem Index idx in der Liste einen Wert zu.
            self.symbol_list.add(Symbol(symbols[item], pos, idx)) # es wird ein Objekt der Klasse Symbol erstellt und diesem Objekt werden drei Argumente übergeben: symbols[item], pos, idx
            pos = list(pos) # pos wird in eine Liste umgewandelt.
            pos[1] += 300 # Pos-Variable wird um 300 erhöht.
            pos = tuple(pos) # pos wird in ein tuple umgewandelt

    def animate(self, delta_time): # Funktion für die Animation
        if self.reel_is_spinning: # wenn Slotmaschine sich dreht
            self.delay_time -= (delta_time * 1000) # erstellt eine Variable, um eine Verzögerung zu erzeugen
            self.spin_time -= (delta_time * 1000) # erstellt eine Variable, um eine Verzögerung zu erzeugen
            reel_is_stopping = False # gibt den Zustand an, ob die Slotmaschine schon gestoppt wurde.

            if self.spin_time < 0: # wenn self.spin_time ist kleiner als 0
                reel_is_stopping = True # dann steht die Slotmaschine

            # Startet die Animation
            if self.delay_time <= 0: #wenn self.delay_time ist gleich oder kleiner als 0

                # dann alle 5 Symbole auf der Walze durchlaufen, abschneiden, neues zufälliges Symbol oben auf dem Stapel hinzufügen
                for symbol in self.symbol_list:
                    symbol.rect.bottom += 100 #gibt die große von dem Symbol an

                   
                    if symbol.rect.top == 1200: # Wenn Symbol oben einen abstand von 1200 hat
                        if reel_is_stopping: # und wenn Slotmaschine gestoppt ist
                            self.reel_is_spinning = False # dann dreht sich die Slotmaschine nicht

                        symbol_idx = symbol.idx # erstellt einen Symbol index
                        symbol.kill() # löscht die zu vielen Symbole
                        self.symbol_list.add(Symbol(symbols[random.choice(self.shuffled_keys)], ((symbol.x_val), -300), symbol_idx)) # erstellt anstelle ein zufälliges Symbol von oben

    def start_spin(self, delay_time): # Funktion um das drehen zu starten
        self.delay_time = delay_time
        self.spin_time = 1000 + delay_time
        self.reel_is_spinning = True

    def reel_spin_result(self):
        # Abfrage und Rückgabe der Textdarstellung von Symbolen in einer gegebenen Spule
        spin_symbols = []
        for i in GAME_INDICES:
            spin_symbols.append(self.symbol_list.sprites()[i].sym_type)
        return spin_symbols[::-1]

class Symbol(pygame.sprite.Sprite): # Klasse von Symbol
    def __init__(self, pathToFile, pos, idx):
        super().__init__()

        self.sym_type = pathToFile.split('/')[3].split('.')[0]

        self.pos = pos #Position von dem Symbol
        self.idx = idx #Index vom Symbol
        self.image = pygame.image.load(pathToFile).convert_alpha() #lädt das Symbol
        self.rect = self.image.get_rect(topleft = pos) #erstellt einen Rechteck, für den Umriss
        self.x_val = self.rect.left # setzt den Ankerpunkt

        # Position/Einstellungen für den Gewonnentext
        self.size_x = 300
        self.size_y = 300
        self.alpha = 255
        self.fade_out = False
        self.fade_in = False

    def update(self):
        # Erstellt den leichten Vergrößerneffekt beim Gewinnen
        if self.fade_in:
            if self.size_x < 320:
                self.size_x += 1
                self.size_y += 1
                self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))
        
        # Verblasst die Icons beim verlieren
        elif not self.fade_in and self.fade_out:
            if self.alpha > 115:
                self.alpha -= 7
                self.image.set_alpha(self.alpha)