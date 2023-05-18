import re
from typing import List

def extract_mentions(text: str) -> List[str]:
    """
    Extrait les noms de personnages mentionnés à partir d'un texte donné.

    Args:
    text (str): Le texte d'entrée à partir duquel extraire les mentions.

    Retourne:
    List[str]: Une liste des noms de personnages mentionnés.
    """
    character_names = ["Harry Potter", "Ron Weasley", "Hermione Granger", "Argus Filch", "Dungeon Master"]
    mentioned_characters = []

    for name in character_names:
        if re.search(fr'\b{name}\b', text, re.IGNORECASE):
            mentioned_characters.append(name)

    return mentioned_characters

def check_word_limit(text: str, word_limit: int) -> bool:
    """
    Vérifie si le texte donné est dans la limite de mots spécifiée.

    Args:
    text (str): Le texte d'entrée à vérifier.
    word_limit (int): Le nombre maximal de mots autorisés.

    Retourne:
    bool: Vrai si le texte est dans la limite de mots, Faux sinon.
    """
    words = text.split()
    return len(words) <= word_limit

def validate_message(text: str, word_limit: int) -> bool:
    """
    Valide un message en fonction de la limite de mots et des mentions de caractères.

    Args:
    text (str): Le message d'entrée à valider.
    word_limit (int): Le nombre maximal de mots autorisés.

    Retourne:
    bool: Vrai si le message est valide, Faux sinon.
    """
    if not check_word_limit(text, word_limit):
        return False

    mentions = extract_mentions(text)
    if len(mentions) > 1:
        return False

    return True

def parse_response1(response):
    test_pattern = r"Test: (oui|None)"
    stats_pattern = r"Stats: ([\w\s]+)"
    player_pattern = r"Player: ([\w\s]+)"
    action_pattern = r"Action: ([\w\s]+)"


    test_result = re.search(test_pattern, response)
    stats_result = re.search(stats_pattern, response)
    player_result = re.search(player_pattern, response)
    action_result = re.search(action_pattern, response)

    if test_result and test_result.group(1) == "oui":
        return {
            "Test": "oui",
            "Stats": stats_result.group(1) if stats_result else None,
            "Player": player_result.group(1) if player_result else None,
            "action": action_result.group(1) if player_result else None
        }
    else:
        return {"Test": "None"}

def parse_context_response(response):
    context_pattern = r"Contexte: (Oui|Non)"
    reason_pattern = r"Raison: ([\w\s]+)"

    context_result = re.search(context_pattern, response)
    reason_result = re.search(reason_pattern, response)

    if context_result and context_result.group(1) == "Non":
        return {
            "Contexte": "Non",
            "Raison": reason_result.group(1) if reason_result else None,
        }
    else:
        return {"Contexte": "Oui"}
