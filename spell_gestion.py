import pyxel
from quests import is_in_hitbox, calc_hitbox


def which_spell():
    """Renvoie le sort correspondant à la touche pressée (string) depuis la table des sorts du fichier spell.json obtenu grâce à l'appel de la fonction get_spells() du fichier get_jsondata.py
    Prend en paramètre la touche pressée (string)"""
    



def is_spell_in_hitbox(spell_name, hitbox):
  """Renvoie True si le sort est dans la hitbox (str), False sinon (booléen)"""
  return False

def object_in_trajectory(y, *n):
  tab_pos_object = []
  for pos in n:
    if y in pos :
        tab_pos_object.append(pos)
  return tab_pos_object
      


def fireball(pos_x, direction, tab_pos_object, dico_object_ig):
    if direction == 1:
       pos_end = pos_x + 225
    elif direction == -1:
       pos_end = pos_x - 225
    while pos_x != pos_end :
      for pos_object in tab_pos_object:
         hitbox_object = calc_hitbox(pos_object[0])
         if is_in_hitbox(pos_x, hitbox_object) == True:
            for key, value in dico_object_ig.items():
               if pos_object == value:
                  return key
      if direction == 1:   
         pos_x += 1
      elif direction == -1:
         pos_x -= 1
    return pos_end

def dash(pos_x, direction, dico_object_ig):
    if direction == 1:
       range = calc_hitbox(pos_x)[1]
    elif direction == -1:
       range = calc_hitbox(pos_x)[0]
    
      

   