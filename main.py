import pyxel
from deplacement import *

pyxel.init(160, 120)

def update():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
  pyxel.rect(50, 0, 8, 8, 9)
  
pyxel.run(update, draw)