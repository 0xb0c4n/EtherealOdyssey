import pyxel
from deplacement import deplacement_x
from quests import interact, launch_quest
from get_jsondata import get_quests, get_player, get_spells, get_pnj
from write import changeJson
from random import randint

run_sprite = [(48, 0, 38, 58), (88, 0, 29, 56), (120, 0, 32, 56),
              (152, 0, 33, 50), (192, 0, 43, 51), (0, 64, 31, 51)]
jump_sprite = [(0, 120, 28, 53), (32, 120, 36, 56), (72, 120, 31, 50),
               (104, 120, 32, 60), (136, 120, 38, 53), (176, 120, 25, 46)]
fireball_sprite = [(0, 184, 32, 56), (32, 184, 39, 56), (72, 184, 48, 53),
                   (120, 184, 50, 53)]
pal = [0x1b2954,0x8c938c,0x5a3936,0x28222c,0x4c505b,0x73522d,
       0x83604f,0x3c4c54,0xc49892,0x3c445c,0x6c6e6c,0x7c706a,
       0x6c6468,0xf3b340,0xe68d02,0xffb228,0xAF082D,0x83213C,
       0xF35C5C,0x2D2E4D,0x316595,0xffffff,0x3fb34e,0x000000]

pyxel.init(500, 250, "Ethereal Odyssey", display_scale=2)
pyxel.load("ressources.pyxres")
pyxel.colors.from_list(pal)

#Définition de toutes les variables pour les mettre dans la fonction draw

showed = False
perso_x = 0
y = 169
scroll_x = 0
SCROLL_BORDER_X = 125
animation = "fireball"
is_jumping = False
is_descending = False
is_inside = {}
launch = False
dialog = {}
character = ""
i = 0
game_launched = False
direction = 1

def update():
  global perso_x, animation, direction, y, scroll_x, is_jumping, is_descending, is_inside, character_name, position_x, showed, game_launched, title, launch, character, pnj_list, dialog, instruction, i, characters_quest, objective

  perso_x, animation, direction = deplacement_x(perso_x, 1, direction)

  quest_list = get_quests()
  questNumber = get_player()['questNumber']
  dimension = get_player()["dimension"]
  pnj_list = get_pnj(dimension)

  questNumber = get_player()['questNumber']
  secondQuestNumber = int(str(questNumber % 1).split(".")[1]) - 1
  deploy = quest_list[int(questNumber)]["deploy"]
  instruction = deploy[secondQuestNumber]["instruction"]
  title = quest_list[int(questNumber)]["title"]
  objective = deploy[secondQuestNumber]["objective"]
  characters_quest = deploy[secondQuestNumber]["character"]

  if perso_x > scroll_x + SCROLL_BORDER_X and direction == 1:
    scroll_x += 3
  elif perso_x < SCROLL_BORDER_X:
    scroll_x = 0
  elif direction == -1 and animation == "run":
    scroll_x -= 3

  for elt in pnj_list:
    if elt["interactable"] == True:
      character_name = elt["name"]
      position_x = elt["position_x"]
      is_inside[character_name] = interact(perso_x, position_x)

  if(is_inside[characters_quest] == True and objective == "dialog"):
    launch, dialog, character = launch_quest(questNumber, quest_list, launch, dialog, character, i)
      
    if(pyxel.btnr(pyxel.KEY_J)):
      i+=1

  if pyxel.btnr(pyxel.KEY_Z):
    animation = "fireball"

  if(game_launched == False):
    if(pyxel.btnr(pyxel.KEY_E)):
      game_launched = True

  if (pyxel.btnr(pyxel.KEY_SPACE)):
    is_jumping = True


  if (y >= 149 and is_jumping == True):
    y -= 2
  elif (is_descending == True and y <= 169):
    y += 2
  elif (y <= 149):
    is_descending = True
    is_jumping = False
  else:
    is_descending = False
    is_jumping = False


def draw():
  if game_launched == False:
    pyxel.text(100, 10, "Ethereal Odyssey", 12)
    pyxel.text(40,100,"Press [E] to play (full screen highly recommended)", 12)
  else:
    pyxel.cls(0)
    pyxel.camera(scroll_x, 0)
    pyxel.images[2].load(0, 0, "assets/assets1.png")
    pyxel.images[1].load(0, 0, "assets/background.png")
    for i in range(10):
      pyxel.blt(256*i, 0, 1, 0,0,256,177)

    for elt in pnj_list:
      pyxel.blt(elt["position_x"], elt["position_y"], elt["image_bank"], elt["location_x"], elt["location_y"], elt["size_x"], elt["size_y"], 21)

      if (is_inside[elt["name"]] == True):
        pyxel.text(elt["position_x"]-20, 140, "Press [E] to interact", 21)
    #Démarrage de la quête
    
    for i in range(1400):
      pyxel.blt(41*i,250-21,2,1,74,41,21)

    pyxel.blt(200, 0, 2, 47,0,128,100,21)

 #Animation
    if (animation == "run" and is_jumping == False):
      coef = pyxel.frame_count // 5 % 5
      pyxel.blt(perso_x, y, 0, run_sprite[coef][0], run_sprite[coef][1],
                run_sprite[coef][2] * direction, run_sprite[coef][3], 0)
    elif (animation == "fireball" and is_jumping == False):
      coef = pyxel.frame_count // 4 % 4
      pyxel.blt(perso_x, y, 0, fireball_sprite[coef][0], fireball_sprite[coef][1],
                fireball_sprite[coef][2], fireball_sprite[coef][3], 0)
    elif (y != 150 and is_jumping == True):
      coef = pyxel.frame_count // 6 % 6
      pyxel.blt(perso_x, y, 0, jump_sprite[coef][0], jump_sprite[coef][1],
                jump_sprite[coef][2] * direction, jump_sprite[coef][3], 0)
    else:
      pyxel.blt(perso_x, y, 0, 0, 0, 24*direction, 58, 0)

    if character != "" and dialog != {} and dialog != "" and showed == False:  
      pyxel.rect(scroll_x,170,500,100,23)
      pyxel.text(scroll_x + 20,185,character.split("_")[0], 21)
      pyxel.text(scroll_x + 20,215,dialog[character],21)
      pyxel.text(scroll_x + 400, 230, "Press [J] to continue", 21)
   
    pyxel.rect(scroll_x + 390, 0, 110, 25, 23)
    pyxel.text(scroll_x + 400, 5, title, 21)
    pyxel.text(scroll_x + 400, 15, instruction, 21)

pyxel.run(update, draw)
