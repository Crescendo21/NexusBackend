import json

# Charger les personnages à partir du fichier JSON
with open('character.json', 'r') as f:
    data = json.load(f)
    characters = data['characters']

def get_character(character_name):
    """
    Récupère les données du personnage spécifié.
    :param character_name: Nom du personnage.
    :return: Dictionnaire de données du personnage.
    """
    for character in characters:
        if character['name'] == character_name:
            return character
    return None

def get_stat_value(character_name, stat_to_check):
    """
    Récupère la valeur de la statistique spécifiée pour le personnage donné.
    :param character_name: Nom du personnage.
    :param stat_to_check: Nom de la statistique à vérifier.
    :return: Valeur de la statistique.
    """
    character = get_character(character_name)
    if character is not None:
        stat_value = character['stats'][stat_to_check]
        print(stat_value)
        return stat_value
    else:
        print(f"Aucun personnage trouvé avec le nom {character_name}")
        return None
