"""
dialogue_agent.py

Ce fichier fait partie du projet Donjon et Dragon et contient la classe DialogueAgent.
Chaque instance de DialogueAgent représente un participant à la conversation (soit un personnage, soit le maître du donjon) dans le simulateur de dialogue.

DialogueAgent peut envoyer des messages (par le biais de sa méthode 'send') et recevoir des messages (par le biais de sa méthode 'receive'). La méthode 'send' utilise un modèle de chat pour générer des réponses en fonction de l'historique des messages. La méthode 'receive' ajoute simplement le message reçu à l'historique des messages.

La classe DialogueAgent possède les méthodes suivantes :
    - __init__: Initialise un nouvel objet DialogueAgent avec un nom, un message système, un modèle de chat et un indicateur indiquant si l'agent est contrôlé par l'utilisateur.
    - reset: Réinitialise l'historique des messages de l'agent.
    - send: Applique le modèle de chat à l'historique des messages et renvoie le message généré.
    - receive: Ajoute le message reçu à l'historique des messages de l'agent.
    - get_last_action: Récupère la dernière action effectuée par l'agent.

Le DialogueAgent est une composante essentielle du simulateur de dialogue, permettant d'interagir et de maintenir une conversation dynamique dans le jeu de Donjon et Dragon.
"""
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

class DialogueAgent:
    def __init__(
            self,
            name: str,
            system_message: SystemMessage,
            model: ChatOpenAI,
            is_user_controlled: bool = False,  # Ajoutez cette ligne
    ) -> None:
        self.name = name
        self.system_message = system_message
        self.model = model
        self.is_user_controlled = is_user_controlled  # Ajoutez cette ligne
        self.prefix = f"{self.name}: "
        self.reset()

    def reset(self):
        self.message_history = ["Here is the conversation so far."]

    def send(self) -> str:
        """
        Applies the chatmodel to the message history
        and returns the message string
        """
        if self.is_user_controlled:
            message_content = input(f"{self.name}, que voulez-vous faire? ")
            return message_content
        else:
            message = self.model(
                [
                    self.system_message,
                    HumanMessage(content="\n".join(self.message_history + [self.prefix])),
                ]
            )
            return message.content

    def receive(self, name: str, message: str) -> None:
        """
        Concatenates {message} spoken by {name} into message history
        """
        self.message_history.append(f"{name}: {message}")

    def get_last_action(self) -> str:
        """
        Returns the last action of the player
        """
        if len(self.message_history) > 1:
            return self.message_history[-1]
        else:
            return ""


