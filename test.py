import pyxel

class Game:
    def __init__(self):
        pyxel.init(1920, 1080)
        pyxel.image(0).load(0, 0, "assets/background.png")  # Charge l'image "sprites.png" dans la banque d'images 0
        self.sprite_x = 0
        self.sprite_y = 0
        self.sprite_width = 400
        self.sprite_height = 400
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)  # Efface l'écran avec la couleur noire (couleur index 0)
        pyxel.blt(80, 60, 0, self.sprite_x, self.sprite_y, self.sprite_width, self.sprite_height, 0)  # Dessine une partie de l'image

Game()