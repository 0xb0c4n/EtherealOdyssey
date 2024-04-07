import pyxel
from deplacement import deplacement_x
from quests import start_quest, launch_quest
from get_jsondata import get_quests, get_player, get_spells

run_sprite = [(48, 0, 38, 58), (88, 0, 29, 56), (120, 0, 32, 56),
              (152, 0, 33, 50), (192, 0, 43, 51), (0, 64, 31, 51)]
jump_sprite = [(0, 120, 28, 53), (32, 120, 36, 56), (72, 120, 31, 50),
               (104, 120, 32, 60), (136, 120, 38, 53), (176, 120, 25, 46)]
fireball_sprite = [(0, 184, 32, 56), (32, 184, 39, 56), (72, 184, 48, 53),
                   (120, 184, 50, 53), (168, 184, 7, 8)]
pal = [0xffffff,0x8c938c,0x5a3936,0x28222c,0x4c505b,0x73522d,
       0x83604f,0x3c4c54,0xc49892,0x3c445c,0x6c6e6c,0x7c706a,
       0x6c6468,0xf3b340,0xe68d02,0xffb228,0xAF082D,0x83213C,
       0xF35C5C,0x2D2E4D,0x3A072B]

pyxel.init(500, 400, "Ethereal Odyssey", display_scale=2)
pyxel.load("ressources.pyxres")
pyxel.colors.from_list(pal)
perso_x = 0
y = 150
scroll_x = 0
SCROLL_BORDER_X = 225
animation = "fireball"
pos_x_wizard = 400
pos_y_wizard = 140
is_jumping = False
is_descending = False
is_inside = False
launch = False
title = ""
dialog = {}
character = ""
pressed = False

def update():
  global perso_x, animation, direction, y, scroll_x, is_jumping, is_descending, is_inside, title, launch, character, dialog, pressed
  if perso_x > scroll_x + SCROLL_BORDER_X and direction == 1:
    scroll_x = perso_x - SCROLL_BORDER_X
  elif perso_x > scroll_x + SCROLL_BORDER_X and direction == -1:
    scroll_x = perso_x

  perso_x, animation, direction = deplacement_x(perso_x, 1)
  is_inside = start_quest(perso_x, pos_x_wizard)
  questNumber = get_player()['questNumber']

  if(is_inside == True and pressed == False):
    launch, title, dialog, character, pressed = launch_quest(questNumber, get_quests(), launch, title, dialog, character, pressed)

  if pyxel.btnr(pyxel.KEY_Z):
    animation = "fireball"

  if(launch != True):
    if (pyxel.btnr(pyxel.KEY_SPACE)):
      is_jumping = True

  if (y > 125 and is_jumping == True):
    y -= 2
  elif (is_descending == True and y < 150):
    y += 2
  elif (y < 125):
    is_descending = True
    is_jumping = False
  else:
    is_descending = False
    is_jumping = False


def draw():
  pyxel.cls(0)
  pyxel.camera(scroll_x, 0)
  pyxel.images[1].load(0, 0, "assets/wizard.png")
  pyxel.images[2].load(0, 0, "assets/heart.png")
  pyxel.blt(pos_x_wizard, pos_y_wizard, 1, 0, 0, 153, 191, 12)
  pyxel.blt(scroll_x, 0, 2, 0, 0, 153, 23, 23)

  #Démarrage de la quête

  if (is_inside == True):
    pyxel.text(375, 130, "Press [E] to interact", 12)
  
  if(launch):
    pyxel.text(500, 50, title, 12)

  if character != "" and dialog != {}:  
    pyxel.text(200,300,character, 12)
    pyxel.text(200,350,dialog[character],12)
  #Animation
  if (animation == "run" and is_jumping == False):
    coef = pyxel.frame_count // 5 % 5
    pyxel.blt(perso_x, y, 0, run_sprite[coef][0], run_sprite[coef][1],
              run_sprite[coef][2] * direction, run_sprite[coef][3], 0)
  elif (animation == "fireball"):
    coef = pyxel.frame_count // 5 % 5
    pyxel.blt(perso_x, y, 0, fireball_sprite[coef][0],
              fireball_sprite[coef][1], fireball_sprite[coef][2],
              fireball_sprite[coef][3], fireball_sprite[coef][4], 0)
  elif (y != 150 and is_jumping == True):
    coef = pyxel.frame_count // 6 % 6
    print(coef)
    pyxel.blt(perso_x, y, 0, jump_sprite[coef][0], jump_sprite[coef][1],
              jump_sprite[coef][2] * direction, jump_sprite[coef][3], 0)
  else:
    pyxel.blt(perso_x, y, 0, 0, 0, 24*direction, 58, 0)


pyxel.run(update, draw)
