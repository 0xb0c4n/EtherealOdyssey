import json

def get_quests():
  """Prend aucun paramètre en compte
  Renvoie l'intégralité du tableau de Json"""
  f = open("quests.json")
  obj = json.load(f)
  return obj