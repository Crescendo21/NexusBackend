from typing import List
from dialogue_agent import DialogueAgent
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
    SystemMessage,
)
import os

os.environ["OPENAI_API_KEY"] = "YourKey"

# Define roles and quest
character_names = ["Harry Potter", "Ron Weasley", "Hermione Granger", "Argus Filch"]
storyteller_name = "Maitre du jeux"
quest = "Trouver les sept horcruxes de Lord Voldemort.."
stats = "Force, Dexterite, charisme, intelligence, constitution, Sagesse, Perception"
word_limit = 50

game_description = f"""Voici le sujet d'une partie de Donjons & Dragons : {quest}.
                    Les personnages sont : {*character_names,}.
                    L'histoire est racontée par le conteur, {storyteller_name}."""

player_descriptor_system_message = SystemMessage(
    content="YVous pouvez ajouter des détails à la description d'un joueur de Donjons & Dragons.")


def generate_character_description(character_name):
    character_specifier_prompt = [
        player_descriptor_system_message,
        HumanMessage(content=
                     f"""{game_description}
                    Veuillez répondre avec une description créative du personnage, {character_name}, en {word_limit} mots ou moins.
                    Parlez directement à {character_name}.
                    N'ajoutez rien d'autre."""
                     )
    ]
    character_description = ChatOpenAI(temperature=1.0)(character_specifier_prompt).content
    return character_description


def generate_character_system_message(character_name, character_description):
    return SystemMessage(content=(
        f"""{game_description}
        Votre nom est {character_name}. 
        La description de votre personnage est la suivante : {character_description}.
        Vous proposerez des actions à entreprendre et {storyteller_name} expliquera ce qui se passe lorsque vous les réalisez.
        Parlez à la première personne du point de vue de {character_name}.
        Pour décrire vos propres mouvements corporels, entourez votre description d'astérisques (*).
        Ne changez pas de rôle !
        Ne parlez pas du point de vue de quelqu'un d'autre.
        Souvenez-vous que vous êtes {character_name}.
        Arrêtez de parler dès que vous avez terminé de parler de votre point de vue.
        N'oubliez jamais de limiter votre réponse à {word_limit} mots !
        N'ajoutez rien d'autre.
    """
    ))

character_descriptions = [generate_character_description(character_name) for character_name in character_names]
character_system_messages = [generate_character_system_message(character_name, character_description) for character_name, character_description in zip(character_names, character_descriptions)]

storyteller_specifier_prompt = [
    player_descriptor_system_message,
    HumanMessage(content=
                 f"""{game_description}
    Veuillez répondre avec une description créative du conteur, {storyteller_name}, en {word_limit} mots ou moins. 
    Parlez directement à {storyteller_name}.
    N'ajoutez rien d'autre."""
                 )
]
storyteller_description = ChatOpenAI(temperature=1.0)(storyteller_specifier_prompt).content

storyteller_system_message = SystemMessage(content=(
    f"""{game_description}
    Vous êtes le conteur, {storyteller_name}.
    Voici votre description : {storyteller_description}.
    Les autres joueurs proposeront des actions à entreprendre et vous expliquerez ce qui se passe lorsqu'ils les réalisent.
    Parlez à la première personne du point de vue de {storyteller_name}.
    Ne changez pas de rôle !
    Ne parlez pas du point de vue de quelqu'un d'autre.
    Souvenez-vous que vous êtes le conteur, {storyteller_name}.
    Arrêtez de parler dès que vous avez terminé de parler de votre point de vue.
    N'oubliez jamais de limiter votre réponse à {word_limit} mots !
    N'ajoutez rien d'autre.
    """
))


quest_specifier_prompt = [
    SystemMessage(content="Vous pouvez rendre une tâche plus précise."),
    HumanMessage(content=
                 f"""{game_description}

    Vous êtes le conteur, {storyteller_name}.
    Veuillez rendre la quête plus précise. Soyez créatif et imaginatif.
    Veuillez répondre avec la quête spécifiée en {word_limit} mots ou moins. 
    Parlez directement aux personnages : {*character_names,}.
    N'ajoutez rien d'autre"""
                 )
]

def build_analyze_message_for_stat_check_prompt(last_action):
    return [
        SystemMessage(content="Vous êtes un analyste dans un jeux de donjon et dragon"),
        HumanMessage(content=f"""votre objectif et d'analyser les actions des joueurs et les réponses du conteur, {storyteller_name}
        Seuls ces stats sont possibles (Dexterite, Constitution, Charisme, Force, Intelligence, Sagesse)
        pour determiner si oui ou non les actions selon le contexte nécessite un jet de test de statistique afin de déterminer la réussite ou l'echec de l'action du joueur. Si l'action nécessite un ou plusieurs jets de test répond moi exclusivement comme ceci : (Test: oui, Stats : Force, Player : Harry Potter, Action : Porter un rocher). Le champ "stats" et Action doit être obligatoirement remplis par une des stats disponibles et ne jamais être None
        si l'action nécessite aucun jet de test répond exclusivement par (Test : None) et rien d'autres.
        Voici le texte à analyser :
        Action du joueur : {last_action}""")
    ]

def build_analyze_message_for_inventory_change_prompt():
    return [
        SystemMessage(content="Vous êtes un analyste dans un jeu de donjon et dragon"),
        HumanMessage(content=f"""Votre objectif est d'analyser les actions des joueurs et les réponses du conteur, {storyteller_name}, pour déterminer si l'inventaire du joueur a changé suite à l'action et à la réponse. Si l'inventaire a changé, indiquez le changement en précisant l'ajout ou la perte d'objet(s) et pour quel joueur. Par exemple : (Changement d'inventaire : ajout, Objet : Épée, Joueur : Harry Potter)
        Si l'inventaire n'a pas changé, répondez exclusivement par (Changement d'inventaire : None) et rien d'autre.
        """)
    ]

def build_analyze_message_for_context_check_prompt(last_action):
    return [
        SystemMessage(content="Vous êtes un analyste dans un jeu de donjon et dragon"),
        HumanMessage(content=f"""Votre objectif est d'analyser les actions des joueurs et les réponses du conteur, {storyteller_name}.
        Vous devez déterminer si l'action donnée par le joueur est appropriée ou non selon un contexte qui fais sens et 
        de la conversation joueur et maitre du jeux. Si l'action est appropriée, répondez par 'Contexte: Oui'.
        Si l'action est inappropriée ou hors contexte, répondez par 'Contexte: Non, Raison: (insérez la raison ici). 
        La raison doit expliquer pourquoi l'action du joueur est hors contexte ou inappropriée.
        Voici le texte à analyser :
        description du jeu : {game_description}
        Action du joueur : {last_action}""")
    ]


def select_next_speaker(step: int, agents: List[DialogueAgent]) -> int:
    """
    Si l'étape est paire, alors sélectionnez le narrateur
    Sinon, sélectionnez les autres personnages de manière circulaire.

    Par exemple, avec trois personnages ayant les indices : 1 2 3
    Le narrateur a l'indice 0.
    Alors l'indice sélectionné sera comme suit :

    step: 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16

    idx:  0  1  0  2  0  3  0  1  0  2  0  3  0  1  0  2  0
    """
    if step % 2 == 0:
        idx = 0
    else:
        idx = (step // 2) % (len(agents) - 1) + 1
    return idx

