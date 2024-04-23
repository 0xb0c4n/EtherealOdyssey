import json

def changeJson(key, value, file):
    """Prend en compte trois variables, key (str) et value (libre) et file (str)
    Modifie le fichier player.json avec la clé correspondante"""
    with open(file, "r") as f:
        data = json.load(f)

    if "/" in key:
        key_parts = key.split("/")  
        modify_key = data
        for i in range(len(key_parts)):
            for char in key_parts[i]:
                
                if char.isdigit():
                    key_parts[i] = int(key_parts[i])
            if i == len(key_parts) - 1:
                modify_key[key_parts[i]] = value
            else:
                modify_key = modify_key[key_parts[i]]   
        
    else:    
        data[key] = value

    with open(file, "w") as f:
        f.write(json.dumps(data, indent=4))