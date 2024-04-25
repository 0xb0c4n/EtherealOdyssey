import json

def get_quests():
  """Prend aucun paramètre en compte
  Renvoie l'intégralité du tableau de quêtes"""
  f = open("data/quests.json")
  obj = json.load(f)
  return obj

def get_spells():
  """Prend aucun paramètre en compte
  Renvoie l'intégralité du tableau de sorts"""
  f = open("data/spells.json")
  obj = json.load(f)
  return obj

def get_player():
  """Prend aucun paramètre en compte
  Renvoie l'intégralité du tableau des infos du joueur"""
  f = open("data/player.json")
  obj = json.load(f)
  return obj

def get_pnj(dimension):
  """Prend la dimension (str) en paramètre
  Renvoie l'intégralité du tableau des PNJ"""
  f = open("data/" + dimension + "_pnj.json")
  obj = json.load(f)
  return obj

def get_monster():
  """Prend aucun paramètre en compte
  Renvoie l'intégralité du tableau des infos des monstres"""
  f = open("data/monsters.json")
  obj = json.load(f)
  return obj
