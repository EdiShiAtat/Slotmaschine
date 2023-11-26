# allgemeine Anzeige Einstelungen
DEFAULT_IMAGE_SIZE = (300, 300) # Standard Bild Größe
FPS = 120 # max Bilder pro Sekunde
HEIGHT = 1000 # Höhe
WIDTH = 1600 # Breite
START_X, START_Y = 10, -300 # Koordinaten, wo Gitter anfängt
X_OFFSET, Y_OFFSET = 20, 0 #Abstand von einen Gitter zum anderen

# Images
BG_IMAGE_PATH = 'graphics/0/background_slotmachine.png' # Hintergrundbild
GRID_IMAGE_PATH = 'graphics/0/gridline.png' # Gitterbild
GAME_INDICES = [1, 2, 3] # Spalten
SYM_PATH = 'graphics/0/symbols' # Pfad zu den Bildern

# Text
TEXT_COLOR = (0xff, 0xff, 0xff, 0xff) # Textfarbe
UI_FONT = 'graphics/font/Super Dessert.ttf' # Schriftart
UI_FONT_SIZE = 40 # Schriftgröße
WIN_FONT_SIZE = 90 # Geweinn Schriftgröße
 
 #Symbole Bilder Pfade
symbols = {
    'wassermelone': f"{SYM_PATH}/wassermelone.png", 
    'banane': f"{SYM_PATH}/banane.png",
    'kirsche': f"{SYM_PATH}/cherry.png",
    'aubergine': f"{SYM_PATH}/eggplant.png",
    'pfirsich': f"{SYM_PATH}/peach.png"
}