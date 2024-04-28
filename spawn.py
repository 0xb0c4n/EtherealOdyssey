import random

def spawn_ressources(min_x, max_x, platform_mine):
    """Prend en compte min_x (int), max_x (int), platform_mine (liste de tuples)
    Renvoie la liste des éléments spawn (list)"""
    list = []
    for i in range(5):
        x = random.randint(min_x, max_x)    
        for elt in platform_mine:
            if elt[0] <= x <= elt[1]:
                y = 256-30*elt[2]-29
        list.append(tuple([x, y]))
    return list