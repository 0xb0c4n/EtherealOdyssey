import pyxel

def deplacement_x(perso_x, speed, direction, block_left, block_right):
  """Prend en compte le x du personnage (integer) et la vitesse (float)
  Renvoie le nouveau x (integer)"""
  if(pyxel.btn(pyxel.KEY_RIGHT) and block_right == False):
    perso_x+=3*speed
    animation="run"
    direction=1
  elif(pyxel.btn(pyxel.KEY_LEFT) and perso_x-3*speed >= 0 and block_left == False):
    animation="run"
    direction=-1
    perso_x-=3*speed
  else:
    animation="idle"
  return perso_x, animation, direction
