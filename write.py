import json

def changeJson(key, value, file):
    """Prend en compte trois variables, key (str) et value (libre) et file (str)
    Modifie le fichier player.json avec la clé correspondante"""
    with open(file, "r") as f:
        data = json.load(f)

    data[key] = value

    with open(file, "w") as f:
        f.write(json.dumps(data, indent=4))