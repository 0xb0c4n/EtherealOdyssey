def follow(perso_x, monster_x):
    """Prend en compte perso_x (int), monster_x (int)
    Renvoie l'état du boss (str) et le monster_x (int)"""
    if(perso_x + 200 < monster_x):
        monster_x -= 2
        boss = "walk"
    else:
        monster_x = monster_x
        boss = "idle"
    return monster_x, boss

def has_been_hit(is_jumping, is_attack):
    """Prend en compte is_jumping et is_attack (bool)
    Renvoie un booléen désignant si le monstre a touché par son attaque le joueur"""
    if(is_jumping == False and is_attack):
        return True
    else:
        return False
    
def monster_hit(is_launched, fireball_x, monster_x, fireball_launched, animation, perso_x):
    """Prend 5 paramètres : is_launched (bool), fireball_x (int), monster_x (int), fireball_launched(bool), animation (str), perso_x (int)
    Renvoie un booléen (désignant si le monstre est touché) et fireball_launched (bool)"""
    if(fireball_launched and is_launched and fireball_x >= monster_x):
        fireball_launched = False
        return True, fireball_launched
    elif animation == "dash" and perso_x + 66 >= monster_x:
        return True, fireball_launched
    else:
        return False, fireball_launched