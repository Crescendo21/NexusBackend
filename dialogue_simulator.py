"""
dialogue_simulator.py

Ce fichier fait partie du projet Donjon et Dragon et contient la classe DialogueSimulator.
DialogueSimulator est utilisé pour simuler une conversation entre différents personnages et le narrateur (Dungeon Master) en utilisant des agents de dialogue. Chaque agent de dialogue représente un personnage et peut envoyer et recevoir des messages. DialogueSimulator gère la sélection du prochain locuteur, le déroulement des étapes de la conversation et le suivi des actions effectuées par les personnages.

La classe DialogueSimulator possède les méthodes suivantes :
    - __init__: Initialise un nouvel objet DialogueSimulator avec une liste d'agents et une fonction de sélection du prochain locuteur.
    - reset: Réinitialise tous les agents de la conversation.
    - inject: Injecte un message initial dans la conversation pour la démarrer.
    - step: Avance la conversation d'un pas, faisant parler le prochain personnage et mettant à jour l'historique des messages.
    - get_last_action: Récupère la dernière action effectuée par un joueur (hors narrateur).
"""

from typing import List, Callable
from dialogue_agent import DialogueAgent
from dialogue_test import DiceRoll, TestCheck, ContextCheck
from settings import storyteller_name

import os

os.environ["OPENAI_API_KEY"] = "YourKey"


class DialogueSimulator:
    def __init__(
            self,
            agents: List[DialogueAgent],
            selection_function: Callable[[int, List[DialogueAgent]], int],
    ) -> None:
        self.agents = agents
        self._step = 0
        self.select_next_speaker = selection_function

    def reset(self):
        for agent in self.agents:
            agent.reset()

    def inject(self, name: str, message: str):
        """
        Initiates the conversation with a {message} from {name}
        """
        for agent in self.agents:
            agent.receive(name, message)

        self._step += 1

    def step(self) -> tuple[str, str]:
        # 1. choisis le prochain "speaker"
        speaker_idx = self.select_next_speaker(self._step, self.agents)
        speaker = self.agents[speaker_idx]

        # 2. Le prochain "speaker" envoie le message
        message = speaker.send()

        # Si le locuteur n'est pas le conteur, vérifiez d'abord si l'action est dans le contexte
        if speaker.name != storyteller_name:
            context_check = ContextCheck(self, message)
            parsed_context_response = context_check.check_context()

            if parsed_context_response.get("Contexte", "").lower() == "non":
                reason = parsed_context_response.get("Raison", "")
                message += f"\nVotre action est hors contexte. Raison : {reason}. Veuillez proposer une autre action."
            else:
                test_check = TestCheck(self, message)
                parsed_response1 = test_check.check_for_stat_test()

                if parsed_response1.get("Test", "").lower() == "oui":
                    # Utilisez la classe DiceRoll pour effectuer le jet de dé
                    dice_roll = DiceRoll(parsed_response1, speaker.name)
                    success_action = dice_roll.perform_dice_roll()
                    message += f"\nLe jet de compétence de {speaker.name} est un {success_action}."

        # 3. Tout le monde recoit le message
        for receiver in self.agents:
            receiver.receive(speaker.name, message)

        # 4. increment time
        self._step += 1

        return speaker.name, message

    def get_last_action(self) -> str:
        """
        Returns the last action of any player (not the storyteller)
        """
        last_action = ""
        for agent in reversed(self.agents[1:]):
            if len(agent.message_history) > 1:
                last_action = agent.message_history[-1]
                break
        return last_action

