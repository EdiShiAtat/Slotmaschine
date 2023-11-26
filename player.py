from settings import *

class Player():
    def __init__(self):
        self.balance = 30.00 #Startguthaben
        self.bet_size = 10.00 #Einsatz
        self.last_payout = 0.00 #letzte Auszahlung
        self.total_won = 0.00 #gesamt gewonnen
        self.total_wager = 0.00 #gesamt gewettet

    def get_data(self): # Variablen um die oben generierten Werte abzurufen
        player_data = {}
        player_data['balance'] = "{:.2f}".format(self.balance)
        player_data['bet_size'] = "{:.2f}".format(self.bet_size)
        player_data['last_payout'] = "{:.2f}".format(self.last_payout) if self.last_payout else "N/A"
        player_data['total_won'] = "{:.2f}".format(self.total_won)
        player_data['total_wager'] = "{:.2f}".format(self.total_wager)
        return player_data # gibt player_data zurück

    def place_bet(self): # Funktion um den Einsatz zu platzieren
        bet = self.bet_size # erstellt eine Variable und nimmt den Wert von self.bet_size
        self.balance -= bet # zieht Guthaben ab
        self.total_wager += bet # fügt den Einsatz zum kompletten Wette hinzu.