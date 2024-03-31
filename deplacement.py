import pyxel

def deplacement_x(perso_x, speed):
  """Prend en compte le x du personnage (integer) et la vitesse (float)
  Renvoie le nouveau x (integer)"""
  if(pyxel.btn(pyxel.KEY_RIGHT)):
    perso_x+=3*speed
    animation="run"
    direction=1
  elif(pyxel.btn(pyxel.KEY_LEFT)):
    animation="run"
    direction=-1
    perso_x+=3*speed
  else:
    animation="idle"
    direction=1
  return perso_x, animation, direction

def jump(perso_y, height):
  """Prend en compte le y du personnage (integer) et height(float)
  Renvoie le nouveau y"""
  return y