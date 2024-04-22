import pyxel

def deplacement_x(perso_x, speed, direction):
  """Prend en compte le x du personnage (integer) et la vitesse (float)
  Renvoie le nouveau x (integer)"""
  if(pyxel.btn(pyxel.KEY_RIGHT) and perso_x+3*speed < 1500):
    perso_x+=3*speed
    animation="run"
    direction=1
  elif(pyxel.btn(pyxel.KEY_LEFT) and perso_x-3*speed >= 0):
    animation="run"
    direction=-1
    perso_x-=3*speed
  else:
    animation="idle"
  return perso_x, animation, direction
