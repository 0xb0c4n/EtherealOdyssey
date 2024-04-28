def passive_regen(current_life):
  """Prend en compte la vie actuelle (integer)
  Renvoie la nouvelle vie (integer)"""
  if(current_life < 100):
    current_life += 2
  return current_life

def player_damage(current_life, damage):
  """Prend en compte la vie actuelle (integer) et les dégâts du monstre (int)
  Renvoie la nouvelle vie (integer)"""
  current_life -= damage
  return current_life

def check_health(current_life):
  """Prend en compte la vie actuelle (integer)
  Vérifie si c'est game over, si oui renvoie True, sinon renvoie False"""
  if current_life <= 0:
    return True
  else:
    return False
  