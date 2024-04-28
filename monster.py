def follow(perso_x, monster_x):
    if(perso_x + 200 < monster_x):
        monster_x -= 2
        boss = "walk"
    else:
        monster_x = monster_x
        boss = "idle"
    return monster_x, boss

def has_been_hit(is_jumping, is_attack):
    if(is_jumping == False and is_attack):
        return True
    else:
        return False
    
def monster_hit(is_lauched, fireball_x, monster_x, fireball_launched, animation, perso_x):
    if(fireball_launched and is_lauched and fireball_x >= monster_x):
        fireball_launched = False
        return True, fireball_launched
    elif animation == "dash" and perso_x + 66 >= monster_x:
        return True, fireball_launched
    else:
        return False, fireball_launched