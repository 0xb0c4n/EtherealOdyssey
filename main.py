import pyxel
from deplacement import deplacement_x
from quests import start_quest, launch_quest
from get_jsondata import get_quests, get_player, get_spells, get_pnj

run_sprite = [(48, 0, 38, 58), (88, 0, 29, 56), (120, 0, 32, 56),
              (152, 0, 33, 50), (192, 0, 43, 51), (0, 64, 31, 51)]
jump_sprite = [(0, 120, 28, 53), (32, 120, 36, 56), (72, 120, 31, 50),
               (104, 120, 32, 60), (136, 120, 38, 53), (176, 120, 25, 46)]
fireball_sprite = [(0, 184, 32, 56), (32, 184, 39, 56), (72, 184, 48, 53),
                   (120, 184, 50, 53)]
pal = [0xffffff,0x8c938c,0x5a3936,0x28222c,0x4c505b,0x73522d,
       0x83604f,0x3c4c54,0xc49892,0x3c445c,0x6c6e6c,0x7c706a,
       0x6c6468,0xf3b340,0xe68d02,0xffb228,0xAF082D,0x83213C,
       0xF35C5C,0x2D2E4D,0x3A072B]

pyxel.init(254, 157, "Ethereal Odyssey")
pyxel.load("ressources.pyxres")
pyxel.colors.from_list(pal)

perso_x = 0
y = 99
scroll_x = 0
SCROLL_BORDER_X = 125
animation = "fireball"
is_jumping = False
is_descending = False
is_inside = False
launch = False
title = ""
dialog = {}
character = ""
i = 0
quest_list = get_quests()
instruction = ""
game_launched = False

def update():
  global perso_x, animation, direction, y, scroll_x, is_jumping, is_descending, is_inside, game_launched, title, launch, character, pnj_list, dialog, instruction, i

  perso_x, animation, direction = deplacement_x(perso_x, 1)
  questNumber = get_player()['questNumber']
  dimension = get_player()["dimension"]
  pnj_list = get_pnj(dimension)

  for elt in pnj_list:
    if elt["questGiver"] == True:
      is_inside = start_quest(perso_x, elt["position_x"])

  if perso_x > scroll_x + SCROLL_BORDER_X and direction == 1:
    scroll_x += 3
  elif direction == -1:
    scroll_x -= 3
  
  if(is_inside == True):
    if(i == len(get_quests()[0]["deploy"][0]["dialog"])):
      dialog = ""
      quest_list[int(questNumber)]["deploy"][int(questNumber % 1)]["showed"] = False
      print(int(questNumber % 1))
    else:
      launch, title, dialog, character, instruction = launch_quest(questNumber, get_quests(), launch, title, dialog, character, instruction, i)
    
      if(pyxel.btnr(pyxel.KEY_J)):
        i+=1


  if pyxel.btnr(pyxel.KEY_Z):
    animation = "fireball"

  if(game_launched == False):
    if(pyxel.btnr(pyxel.KEY_E)):
      game_launched = True

  if (pyxel.btnr(pyxel.KEY_SPACE)):
    is_jumping = True

  print(y)

  if (y >= 79 and is_jumping == True):
    y -= 2
  elif (is_descending == True and y <= 99):
    y += 2
  elif (y <= 79):
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
    pyxel.blt(scroll_x, 0, 2, 36, 0, 60, 23, 23)
    for i in range(50):
      pyxel.blt(256*i, 0, 1, 0,0,256,177)

    for elt in pnj_list:
      pyxel.blt(elt["position_x"], elt["position_y"], elt["image_bank"], elt["location_x"], elt["location_y"], elt["size_x"], elt["size_y"])

    #Démarrage de la quête

    if (is_inside == True):
      pyxel.text(375, 75, "Press [E] to interact", 12)
    
    if(launch):
      pyxel.text(scroll_x + 160, 5, title, 12)
      pyxel.text(scroll_x + 150, 15, instruction, 12)

    if character != "" and dialog != {} and dialog != "":  
      pyxel.rect(scroll_x, 85, 256, 82, 12)
      pyxel.text(scroll_x + 20,99,character.split("_")[0], 0)
      pyxel.text(scroll_x + 20,120,dialog[character],0)
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
      print(coef)
      pyxel.blt(perso_x, y, 0, jump_sprite[coef][0], jump_sprite[coef][1],
                jump_sprite[coef][2] * direction, jump_sprite[coef][3], 0)
    else:
      pyxel.blt(perso_x, y, 0, 0, 0, 24*direction, 58, 0)


pyxel.run(update, draw)
