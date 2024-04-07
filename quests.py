import pyxel

def calc_hitbox(pos_x):
  """Renvoie la hitbox d'un objet (string)
  Prend en paramètre les coordonnées x  de l'objet (integer)"""
  debut_hitbox = pos_x - 50
  fin_hitbox = pos_x + 50
  hitbox = str(debut_hitbox) + ";" + str(fin_hitbox)
  return hitbox


def is_in_hitbox(pos_x, hitbox):
  """Renvoie True si l'objet est dans la hitbox (boolean)
  Prend en paramètre les coordonnées x et y de l'objet (integer) et la hitbox (string)"""
  if pos_x > int(hitbox.split(";")[0]) and pos_x < int(hitbox.split(";")[1]):
    return True
  else:
    return False


def start_quest(perso_x, pos_x_wizard):
  wizard_hitbox = calc_hitbox(pos_x_wizard)
  return is_in_hitbox(perso_x, wizard_hitbox)

def launch_quest(questNumber, questDict, launch, title, dialog, character, pressed):
  """Vérifie si la quête précédente est terminée, et si oui démarre la nouvelle quête
  Prend en compte le questNumber du joueur, et l'état de la quête précédente"""
  if(pyxel.btnr(pyxel.KEY_E)):
    launch = True
    title = questDict[int(questNumber)]["title"]
    dialog = questDict[int(questNumber)]["deploy"][0]["dialog"]
    character_list = list(dialog.keys())
    i = 0
    pressed = True
    character = character_list[i]
    if(pyxel.btnr(pyxel.KEY_SPACE)):
      i+=1
    
  return launch, title, dialog, character, pressed
