def passive_regen(current_life):
  """Prend en compte la vie actuelle (integer)
  Renvoie la nouvelle vie (integer)"""
  if(current_life < 100):
    current_life += 2
  return current_life

def player_damage(current_life, damage):
  current_life -= damage
  return current_life