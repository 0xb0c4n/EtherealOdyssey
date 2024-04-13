import pyxel

class ParallaxBackground:
    def __init__(self):
        pyxel.init(160, 120, "Parallax Background")
        pyxel.load("2.png")  # Load background images
        pyxel.load("3.png")
        pyxel.load("5.png")

        self.scroll_speeds = [1, 2, 3]  # Speed of each layer
        self.layer_positions = [0, 0, 0]  # Initial positions of each layer

        pyxel.run(self.update, self.draw)

    def update(self):
        for i in range(len(self.layer_positions)):
            self.layer_positions[i] -= self.scroll_speeds[i]
            # Reset position when the layer moves out of the screen
            if self.layer_positions[i] <= -pyxel.width:
                self.layer_positions[i] = 0

    def draw(self):
        pyxel.cls(0)  # Clear the screen

        # Draw each background layer
        for i in range(len(self.layer_positions)):
            pyxel.blt(self.layer_positions[i], 0, 0, 0, pyxel.width, pyxel.height)

ParallaxBackground()