
def calc_hitbox(pos_x, pos_y):
  """Renvoie la hitbox d'un objet (string)
  Prend en paramètre les coordonnées x et y de l'objet (integer)"""
  fin_hitbox = pos_x + 10
  debut_hitbox = pos_x - 10
  hitbox = str(fin_hitbox) + ";" + str(debut_hitbox)
  return hitbox

def is_in_hitbox(pos_x, pos_y, hitbox):
  """Renvoie True si l'objet est dans la hitbox (boolean)
  Prend en paramètre les coordonnées x et y de l'objet (integer) et la hitbox (string)"""
  if pos_x 