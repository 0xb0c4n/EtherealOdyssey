import pyxel
from deplacement import deplacement_x
from quests import interact, launch_quest
from get_jsondata import get_quests, get_player, get_spells, get_pnj
from write import changeJson
from spawn import spawn_ressources
import time

run_sprite = [(48, 0, 38, 58), (88, 0, 29, 56), (120, 0, 32, 56),
              (152, 0, 33, 50), (192, 0, 43, 51), (0, 64, 31, 51)]
jump_sprite = [(0, 120, 28, 53), (32, 120, 36, 56), (72, 120, 31, 50),
               (104, 120, 32, 60), (136, 120, 38, 53), (176, 120, 25, 46)]
fireball_sprite = [(0, 184, 32, 56), (32, 184, 39, 56), (72, 184, 48, 53),
                   (120, 184, 50, 53)]
great_boss_sprite = [(0,80,48,62),(54,80,49,61),(107,80,149,63), (0,142,96,59)]

pal = [0x1b2954,0x8c938c,0x5a3936,0x28222c,0x4c505b,0x73522d,
       0x83604f,0x3c4c54,0xc49892,0x3c445c,0x6c6e6c,0x7c706a,
       0x6c6468,0xf3b340,0xe68d02,0xffb228,0xAF082D,0x83213C,
       0xF35C5C,0x2D2E4D,0x316595,0xffffff,0x3fb34e,0x000000,
       0x171724,0x3d232a,0x232b5c,0xfedba7]

platform_mine = [(0, 232, 1), (232, 261, 2), (261, 290, 3), (290, 319, 4), (319, 348, 3), 
                 (348, 609, 2), (609, 638, 1), (638, 667, 2), (667, 696, 3), 
                 (696, 725, 4), (725, 754, 3), (754, 783, 2), (783, 812, 1), (812, 841, 2), (841, 870, 3), 
                 (870, 899, 3), (899, 928, 3), (928, 957, 3), (957, 986, 3), (986, 2900, 2)]

pyxel.init(500, 250, "Ethereal Odyssey", display_scale=2)
pyxel.load("ressources.pyxres")
pyxel.colors.from_list(pal)

#Définition de toutes les variables pour les mettre dans la fonction draw
showed = False
perso_x = 0
y = 169
velocity_y = 0
scroll_x = 0
SCROLL_BORDER_X = 125
animation = "idle"

is_jumping = False

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

block_left = False
block_right = False

completion = 0

great_boss_attack = False

ressources_mine = spawn_ressources(0,2900,platform_mine)

def get_ground_height(x):
  for tuple in platform_mine:
    if tuple[0] <= x < tuple[1]:
      return tuple[2]

def update():
  global perso_x, block_left, deploy, secondQuestNumber, completion, questNumber, velocity_y, block_right, subcharacter, input_text, animation, direction, dimension, y, scroll_x, is_jumping, is_inside, character_name, index, position_x, showed, game_launched, title, launch, character, pnj_list, dialog, instruction, i, characters_quest, objective

  perso_x, animation, direction = deplacement_x(perso_x, 1, direction, block_left, block_right)

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

  if questNumber == 2.4:
      completion = deploy[secondQuestNumber]["completion"]
      if completion == 5:
          dialog = ""
          i = 0
          questNumber = round(questNumber + 0.1, 1)
          launch = False
          index = None
          changeJson("questNumber", questNumber, "data/player.json")
          input_text = ""

  dimension = get_player()["dimension"]
  pnj_list = get_pnj(dimension)

  if(dimension == "mine"):
    if(not is_jumping):
      for ind in range(len(platform_mine)):
        x1,x2,tup_y = platform_mine[ind][0], platform_mine[ind][1], platform_mine[ind][2]
        if x2 == perso_x + 28 and platform_mine[ind+1][2] > tup_y and direction == 1:
          block_left = False
          block_right = True
        elif x1 == perso_x and platform_mine[ind-1][2] > tup_y and direction == -1:
          block_left = True
          block_right = False
        elif x1 < perso_x < x2:
          block_left = False
          block_right = False
    else:
      block_right = False
      block_left = False

  if (pyxel.btnr(pyxel.KEY_SPACE) and not is_jumping and input_text == ""):
    is_jumping = True
    velocity_y = -5

  velocity_y += 0.2  
  y += velocity_y

  velocity_y = min(velocity_y, 5)
  if dimension == "mine":
    if direction == 1:
      if y >= 256-get_ground_height(perso_x+25)*29-58: 
          is_jumping = False
          y = 256-get_ground_height(perso_x+25)*29-58
    elif direction == -1:
      if y >= 256-get_ground_height(perso_x)*29-58: 
            is_jumping = False
            y = 256-get_ground_height(perso_x)*29-58
  else:
    if y >= 169:
      is_jumping = False
      y = 169

  pyxel.images[2].load(0,0,"assets/" + dimension + "_assets.png")
  pyxel.images[1].load(0,0,"assets/"+ dimension + ".png")

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
  if(characters_quest != "" and objective == "dialog" and is_inside[characters_quest] == True ):
    original_dialog = deploy[secondQuestNumber]["dialog"]
    if(i == len(original_dialog)):
      if(correct_index == index or correct_index == ""):
        if subcharacter == "" or subcharacter == "true":
          if(quest_list[int(questNumber)]["deploy"][secondQuestNumber] == quest_list[int(questNumber)]["deploy"][-1]):
            if(quest_list[int(questNumber)]["reward"]):
              reward = quest_list[int(questNumber)]["reward"]
              if "spell_" in reward:
                changeJson("0/unlocked", True, "data/spells.json")
            questNumber = int(questNumber) + 1.1
            print(questNumber)
            launch = False
            changeJson("questNumber", questNumber, "data/player.json")
            dialog = ""
            input_text = ""
            index = None
            i = 0
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
            elif(questNumber == 1.4):
              dimension = "ethereum"
              changeJson("dimension", dimension, "data/player.json")
            elif(questNumber == 2.2):
              dimension = "mine"
              changeJson("dimension", dimension, "data/player.json")
              dialog = ""
              i = 0
              questNumber = round(questNumber + 0.1, 1)
              launch = False
              index = None
              changeJson("questNumber", questNumber, "data/player.json")
              input_text = ""


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
                        else:
                          i+=1
                          subcharacter="false"
        else:
          if(pyxel.btnr(pyxel.KEY_J)):
            i+=1



  if pyxel.btnr(pyxel.KEY_Z):
    animation = "fireball"

  if(game_launched == False):
    if(pyxel.btnr(pyxel.KEY_E)):
      game_launched = True

def draw():
  global input_text, great_boss_attack
  if game_launched == False:
    pyxel.text(100, 10, "Ethereal Odyssey", 12)
    pyxel.text(40,100,"Press [E] to play (full screen highly recommended)", 12)
  else:
    if dimension == "mine":
      pyxel.camera(scroll_x, 0)
      pyxel.cls(0)
      for i in range(20):
        pyxel.blt(256*i, 0, 1, 0,0,256,256)

      for elt in pnj_list:
        if(type(elt["location_x"]) != list):
          pyxel.blt(elt["position_x"], elt["position_y"], elt["image_bank"], elt["location_x"], elt["location_y"], elt["size_x"], elt["size_y"], 21)

          if (elt["interactable"] == True and is_inside[elt["name"]] == True and elt["name"] == characters_quest):
            pyxel.text(elt["position_x"]-20, 140, "Press [E] to interact", 21)
        
      if questNumber == 2.4 and get_quests()[2]["deploy"][3]["completion"] != 5:
        for elt in ressources_mine:
          pyxel.blt(elt[0], elt[1], 2, 58, 0, 33,29,21)
          is_inside_mine = interact(perso_x, elt[0])
          if(is_inside_mine):
            pyxel.text(elt[0], 140, "[E] Mine", 21)
            if(pyxel.btnp(pyxel.KEY_E)):
              changeJson("2/deploy/3/completion", completion+1, "data/quests.json")
              ressources_mine.remove(elt)
      elif questNumber == 2.6:
        coef = pyxel.frame_count // 4 % 4
        if great_boss_attack == False:
          pyxel.blt(1500, 130, 2, great_boss_sprite[0][0], great_boss_sprite[0][1],
              great_boss_sprite[0][2]*-1, great_boss_sprite[0][3], 21)
          is_inside_gb = interact(perso_x, 1450)
          if(is_inside_gb):
            pyxel.text(1500, 100, "[E] Attack", 21)
            if(pyxel.btnp(pyxel.KEY_E)):
              great_boss_attack = True
        else:
          pyxel.blt(1500, 130, 2, great_boss_sprite[coef][0], great_boss_sprite[coef][1],
              great_boss_sprite[coef][2]*-1, great_boss_sprite[coef][3], 21)
      print("hello world") 
      for tuple in platform_mine:
        x1 = tuple[0]
        x2 = tuple[1]
        tup_y = tuple[2]
        coef_ind = (x2-x1) // 29
        for i in range(coef_ind):
          pyxel.blt(x1+29*i,256-29*tup_y,2,0,0,29,29,21)
          if tuple[2] != 1:
            for j in range(1,tup_y):
              pyxel.blt(x1+29*i,256-29*j,2,29,0,29,29,21)
            

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
      if questNumber == 2.4:
        pyxel.text(scroll_x + 380, 15, instruction, 21)
        pyxel.text(scroll_x + 480, 15, str(completion) + "/5", 21)
      else:
        pyxel.text(scroll_x + 380, 15, instruction, 21)
    elif dimension == "ethereum":
      pyxel.camera(scroll_x, 0)
      pyxel.cls(0)

      for i in range(10):
        pyxel.blt(256*i, 0, 1, 0,0,256,177)

      for elt in pnj_list:
        if(type(elt["location_x"]) != list):
          pyxel.blt(elt["position_x"], elt["position_y"], elt["image_bank"], elt["location_x"], elt["location_y"], elt["size_x"], elt["size_y"], 21)

          if (elt["interactable"] == True and is_inside[elt["name"]] == True and elt["name"] == characters_quest):
            pyxel.text(elt["position_x"]-20, 140, "Press [E] to interact", 21)
      #Démarrage de la quête
      for i in range(100):
        pyxel.blt(41*i,250-21,2,0,74,41,21)

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
    elif dimension == "genesis":
      pyxel.camera(scroll_x, 0)
      pyxel.cls(0)

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