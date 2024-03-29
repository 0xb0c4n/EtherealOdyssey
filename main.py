import pyxel

pyxel.init(160, 120)

def update():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
  """Dessine la fenêtre
  """
  
pyxel.run(update, draw)