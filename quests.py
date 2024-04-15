import pyxel

i = 0

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


def interact(perso_x, pos_x):
  hitbox = calc_hitbox(pos_x)
  return is_in_hitbox(perso_x, hitbox)

def launch_quest(questNumber, questDict, launch, dialog, character, i, index):
  if(pyxel.btnr(pyxel.KEY_E)):
    launch = True
    
  if(launch == True):
    secondQuestNumber = int(str(questNumber % 1).split(".")[1]) - 1
    dialog = questDict[int(questNumber)]["deploy"][secondQuestNumber]["dialog"]

    if(index == None):
      if dialog != {}:
        character_list = list(dialog.keys())
        character = character_list[i]
    else:
      character_list = list(dialog.keys())
      character = character_list[i]
      dialog = dialog[character][index]
      character_list = list(dialog.keys())
      character = character_list[-1]

  return launch, dialog, character

