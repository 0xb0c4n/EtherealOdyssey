import pyxel
from deplacement import deplacement_x, jump
run_sprite = [(48,0,38,58),(88,0,29,56),(120,0,32,56),(152,0,33,50),(192,0,43,51),(0,64,31,51)]
pyxel.init(500, 400, "Ethereal Odyssey", display_scale=2)
pyxel.load("ressources.pyxres")
perso_x = 0
y = 150
scroll_x = 0
SCROLL_BORDER_X = 250
animation="idle"
def update():
    global perso_x, animation, direction, y, scroll_x
    if perso_x < scroll_x:
            perso_x = scroll_x
    if perso_x > scroll_x + SCROLL_BORDER_X:
            scroll_x = min(perso_x - SCROLL_BORDER_X, 240 * 8)

    perso_x, animation, direction = deplacement_x(perso_x, 1)

def draw():
    pyxel.cls(0)
    pyxel.camera(scroll_x, 0)
    if(animation == "run"):
        coef = pyxel.frame_count // 5 % 5
        pyxel.blt(perso_x,y,0,run_sprite[coef][0],run_sprite[coef][1],run_sprite[coef][2],run_sprite[coef][3]) 
    else:
        pyxel.blt(perso_x,y,0,0,0,24,58) 

pyxel.run(update, draw)