def follow(perso_x, monster_x, dir_monster):
    if(perso_x + 140 < monster_x):
        monster_x -= 3
        dir_monster = -1
    elif(perso_x - 140 > monster_x):
        monster_x += 3
        dir_monster = 1
    else:
        monster_x = monster_x
        dir_monster = dir_monster
    return monster_x, dir_monster