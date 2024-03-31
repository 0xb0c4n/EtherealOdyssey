import pyxel
from deplacement import deplacement_x
run_sprite = [(48,0,38,58),(88,0,29,56),(120,0,32,56),(152,0,33,50),(192,0,43,51),(0,64,31,51)]
pyxel.init(500, 400, "Ethereal Odyssey", display_scale=2)
pyxel.load("ressources.pyxres")
perso_x = 0
animation="idle"
def update():
    global perso_x, animation, direction

    perso_x, animation, direction = deplacement_x(perso_x, 1)

def draw():
    pyxel.cls(0)
    if(animation == "run"):
        coef = pyxel.frame_count // 5 % 5
        pyxel.blt(perso_x,150,0,run_sprite[coef][0],run_sprite[coef][1],run_sprite[coef][2],run_sprite[coef][3]) 
    else:
        pyxel.blt(perso_x,150,0,0,0,24,58) 

pyxel.run(update, draw)