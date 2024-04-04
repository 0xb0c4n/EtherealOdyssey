import pyxel
from deplacement import deplacement_x
run_sprite = [(48,0,38,58),(88,0,29,56),(120,0,32,56),(152,0,33,50),(192,0,43,51),(0,64,31,51)]
jump_sprite = [(0,120,28,53),(32,120,36,56), (72,120,31,50),(104,120,32,60),(136,120,38,53),(176,120,25,46)]
pyxel.init(500, 400, "Ethereal Odyssey", display_scale=2)
pyxel.load("ressources.pyxres")

perso_x = 0
y = 150
scroll_x = 0
SCROLL_BORDER_X = 225
animation="idle"
is_jumping = False
is_descending = False
def update():
    global perso_x, animation, direction, y, scroll_x, is_jumping, is_descending
    if perso_x < scroll_x:
            perso_x = scroll_x
    if perso_x > scroll_x + SCROLL_BORDER_X:
            scroll_x = min(perso_x - SCROLL_BORDER_X, 240 * 8)

    perso_x, animation, direction = deplacement_x(perso_x, 1)
    if(pyxel.btnr(pyxel.KEY_SPACE)):
        is_jumping = True
        animation = "jump"

    if(y > 125 and is_jumping == True):
        y-=2
        animation="jump"
    elif(is_descending == True and y < 150):
        y+=2
        animation="jump"
    elif(y < 125):
        is_descending = True
        is_jumping = False
    else:
        is_descending = False
        is_jumping = False
        

def draw():
    pyxel.cls(0)
    pyxel.text(scroll_x, 0, str(perso_x), 12)
    pyxel.camera(scroll_x, 0) 
    pyxel.images[1].load(0, 0, "assets/wizard.png")
    pyxel.blt(400, 41,1,0,0,153,191)

    if(animation == "run" ):
        coef = pyxel.frame_count // 5 % 5
        pyxel.blt(perso_x,y,0,run_sprite[coef][0],run_sprite[coef][1],run_sprite[coef][2]*direction,run_sprite[coef][3], 0) 
    elif(y != 150):
        coef = pyxel.frame_count // 6 % 6
        print(coef)
        pyxel.blt(perso_x,y,0,jump_sprite[coef][0],jump_sprite[coef][1],jump_sprite[coef][2]*direction,jump_sprite[coef][3]) 
    else:
        coef = 0
        pyxel.blt(perso_x,y,0,0,0,24,58) 
    print(coef)

pyxel.run(update, draw)