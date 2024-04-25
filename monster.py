def follow(perso_x, monster_x):
    if(perso_x + 200 < monster_x):
        monster_x -= 2
    else:
        monster_x = monster_x
    return monster_x

def has_been_hit_gb(is_jumping, is_attack):
    if(is_jumping == False and is_attack):
        return True
    else:
        return False