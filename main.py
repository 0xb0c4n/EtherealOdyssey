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
       0xF35C5C,0x2D2E4D,0x316595,0xffffff,0x3fb34e,0x000000,
       0x171724,0x3d232a,0x232b5c]

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
index = None
input_text = ""
subcharacter = ""
def update():
  global perso_x, subcharacter, input_text, animation, direction, state, dimension, y, scroll_x, is_jumping, is_descending, is_inside, character_name, index, position_x, showed, game_launched, title, launch, character, pnj_list, dialog, instruction, i, characters_quest, objective

  perso_x, animation, direction = deplacement_x(perso_x, 1, direction)

  state = ""
  quest_list = get_quests()
  dimension = get_player()["dimension"]

  questNumber = get_player()['questNumber']
  
  secondQuestNumber = int(str(questNumber).split(".")[1]) - 1
  deploy = quest_list[int(questNumber)]["deploy"]
  instruction = deploy[secondQuestNumber]["instruction"]
  title = quest_list[int(questNumber)]["title"]
  objective = deploy[secondQuestNumber]["objective"]
  characters_quest = deploy[secondQuestNumber]["character"]
  if "correct_index" in deploy[secondQuestNumber]:
    correct_index = deploy[secondQuestNumber]["correct_index"]
  else:
    correct_index = ""

  original_dialog = deploy[secondQuestNumber]["dialog"]
  dimension = get_player()["dimension"]
  pnj_list = get_pnj(dimension)

  pyxel.images[2].load(0,0,"assets/" + dimension + "_assets.png")
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
    if(i == len(original_dialog) ):
      if(correct_index == index or correct_index == ""):
        if subcharacter == "" or subcharacter == "true":
          if(quest_list[int(questNumber)]["deploy"][secondQuestNumber] == quest_list[int(questNumber)]["deploy"][-1]):
            if(quest_list[int(questNumber)]["reward"]):
              reward = quest_list[int(questNumber)]["reward"]
              if "spell_" in reward:
                changeJson("0/unlocked", True, "data/spells.json")
            questNumber = int(questNumber) + 1.1
            launch = False
            changeJson("questNumber", questNumber, "data/player.json")
            dialog = ""
            input_text = ""
            index = None
          else:
            dialog = ""
            i = 0
            questNumber = round(questNumber + 0.1, 1)
            launch = False
            index = None
            changeJson("questNumber", questNumber, "data/player.json")
            input_text = ""
            if(questNumber == 1.2):
              dimension = "genesis"
              changeJson("dimension", dimension, "data/player.json")
              pyxel.cls(0)
            elif(questNumber == 1.4):
              dimension = "ethereum"
              changeJson("dimension", dimension, "data/player.json")
              pyxel.cls(0)
        else:
          launch = False
          dialog = ""
          i = 0
          index = None
          input_text = ""
      else:
        launch = False
        dialog = ""
        i = 0
        index = None
    else:
      launch, dialog, character = launch_quest(questNumber, quest_list, launch, dialog, character, i, index)
      if launch:
        if type(dialog[character]) == list:
          if pyxel.btnr(pyxel.KEY_1):
              index = 0
          elif pyxel.btnr(pyxel.KEY_2):
              index = 1
          elif pyxel.btnr(pyxel.KEY_3):
              index = 2
        elif dialog[character] == "":
          for k in pyxel.__dict__.keys():
            if k.startswith('KEY_'):
                if pyxel.btn(getattr(pyxel, k)):
                    if k == "KEY_RETURN":
                      with open("data/message.txt") as f:
                        f = f.read()    
                        if input_text == f:
                          i += 1
                          subcharacter = "true"
                          print(subcharacter)
                        else:
                          i+=1
                          subcharacter="false"
                          print(subcharacter)
        else:
          if(pyxel.btnr(pyxel.KEY_J)):
            i+=1



  if pyxel.btnr(pyxel.KEY_Z):
    animation = "fireball"

  if(game_launched == False):
    if(pyxel.btnr(pyxel.KEY_E)):
      game_launched = True

  if (pyxel.btnr(pyxel.KEY_SPACE) and is_jumping == False and is_descending == False and input_text == ""):
    is_jumping = True

    
  elif (y >= 149 and is_jumping == True):
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
  global input_text
  if game_launched == False:
    pyxel.text(100, 10, "Ethereal Odyssey", 12)
    pyxel.text(40,100,"Press [E] to play (full screen highly recommended)", 12)
  else:
    if get_player()["dimension"] == "ethereum":
      pyxel.images[1].load(0,0,"assets/ethereum.png")
      pyxel.cls(0)
      pyxel.camera(scroll_x, 0)

      for i in range(10):
        pyxel.blt(256*i, 0, 1, 0,0,256,177)

      for elt in pnj_list:
        if(type(elt["location_x"]) != list):
          pyxel.blt(elt["position_x"], elt["position_y"], elt["image_bank"], elt["location_x"], elt["location_y"], elt["size_x"], elt["size_y"], 21)

          if (is_inside[elt["name"]] == True and elt["name"] == characters_quest):
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

      if character != "" and dialog != {} and dialog != "" and is_inside[characters_quest]: 
        if(type(dialog[character]) == list):
          pyxel.rect(scroll_x,170,500,100,23)
          pyxel.text(scroll_x + 20,185,character.split("_")[0], 21)
          for i in range(len(dialog[character])):
            pyxel.text(scroll_x + 20,200+i*10,dialog[character][i]["Me_t1"], 21)
        else:
          pyxel.rect(scroll_x,170,500,100,23)
          pyxel.text(scroll_x + 20,185,character.split("_")[0], 21)
          pyxel.text(scroll_x + 20,215,dialog[character],21)
          pyxel.text(scroll_x + 400, 230, "Press [J] to continue", 21)
    
      pyxel.rect(scroll_x + 370, 0, 130, 25, 23)
      pyxel.text(scroll_x + 380, 5, title, 21)
      pyxel.text(scroll_x + 380, 15, instruction, 21)
    elif get_player()["dimension"] == "genesis":
      pyxel.cls(0)
      pyxel.camera(scroll_x, 0)
      pyxel.images[1].load(0,0,"assets/genesis.png")
      for i in range(10):
        pyxel.blt(127*i,0,1,0,0,127,256)
      for j in range(5):
        pyxel.blt(1270+114*j,0,1,127,0,114,256)
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

      for elt in pnj_list:
        if elt["name"] == "Original Block":
          coef = pyxel.frame_count // len(elt["location_x"]) % len(elt["location_x"])
          pyxel.blt(elt["position_x"], 225-elt["size_y"][coef], elt["image_bank"], elt["location_x"][coef], elt["location_y"][coef], elt["size_x"][coef], elt["size_y"][coef], 0)

        if (is_inside[elt["name"]] == True and elt["name"] == characters_quest):
          pyxel.text(elt["position_x"]-20, 140, "Press [E] to interact", 21)

      if character != "" and dialog != {} and dialog != "" and is_inside[characters_quest]: 
        if(type(dialog[character]) == list):
          pyxel.rect(scroll_x,170,500,100,23)
          pyxel.text(scroll_x + 20,185,character.split("_")[0], 21)
          for i in range(len(dialog[character])):
            pyxel.text(scroll_x + 20,200+i*10,dialog[character][i]["Me_t1"], 21)
        elif(type(dialog[character]) == dict):
          pyxel.rect(scroll_x,170,500,100,23)
          pyxel.text(scroll_x + 20,185,character.split("_")[0], 21)
          pyxel.text(scroll_x + 20, 200, dialog[character][subcharacter], 21)       
          pyxel.text(scroll_x + 400, 230, "Press [J] to continue", 21)  
        elif(dialog[character] == ""):
          pyxel.rect(scroll_x,170,500,100,23)
          pyxel.text(scroll_x + 20,185,character.split("_")[0], 21)
          pyxel.text(scroll_x + 20, 200, input_text, 21)
          if len(input_text) < 133:
            for key in range(pyxel.KEY_A, pyxel.KEY_Z + 1):
              if pyxel.btnp(key):
                  input_text += chr(ord('A') + (key - pyxel.KEY_A))
          
            if pyxel.btnp(pyxel.KEY_SPACE):
                input_text += " "
            
            if pyxel.btnp(pyxel.KEY_BACKSPACE) and len(input_text) > 0:
                input_text = input_text[:-1]
              
            if pyxel.btnp(pyxel.KEY_PERIOD):
              input_text += "'"
        
          pyxel.text(scroll_x + 390, 230, "Press [ENTER] to continue", 21)
        else:
          pyxel.rect(scroll_x,170,500,100,23)
          pyxel.text(scroll_x + 20,185,character.split("_")[0], 21)
          pyxel.text(scroll_x + 20,215,dialog[character],21)
          pyxel.text(scroll_x + 400, 230, "Press [J] to continue", 21)
    
      pyxel.rect(scroll_x + 370, 0, 130, 25, 23)
      pyxel.text(scroll_x + 380, 5, title, 21)
      pyxel.text(scroll_x + 380, 15, instruction, 21)


pyxel.run(update, draw)