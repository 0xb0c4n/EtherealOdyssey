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
      


def fireball(pos_x):
    pos_end = pos_x + 500
    return pos_end

def dash(pos_x, direction):
    range = calc_hitbox(pos_x)[1]    
      

   