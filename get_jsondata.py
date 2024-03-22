import json

def get_quests():
  """Prend aucun paramètre en compte
  Renvoie l'intégralité du tableau de quêtes"""
  f = open("quests.json")
  obj = json.load(f)
  return obj

def get_spells():
  """Prend aucun paramètre en compte
  Renvoie l'intégralité du tableau de sorts"""
  f = open("spells.json")
  obj = json.load(f)
  return obj

def get_player():
  """Prend aucun paramètre en compte
  Renvoie l'intégralité du tableau des infos du joueur"""
  f = open("player.json")
  obj = json.load(f)
  return obj