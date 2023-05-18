from typing import List

from dialogue_agent import DialogueAgent
from dialogue_simulator import DialogueSimulator
from settings import character_names, storyteller_name, character_system_messages, storyteller_system_message, quest_specifier_prompt
from langchain.chat_models import ChatOpenAI
import os

os.environ["OPENAI_API_KEY"] = "YourKey"

if __name__ == "__main__":
    # Création des personnages et du narrateur (Dungeon Master)
    characters = []
    for character_name, character_system_message in zip(character_names, character_system_messages):
        characters.append(DialogueAgent(
            name=character_name,
            system_message=character_system_message,
            model=ChatOpenAI(temperature=0.2),
            is_user_controlled=True))

    storyteller = DialogueAgent(name=storyteller_name,
                         system_message=storyteller_system_message,
                         model=ChatOpenAI(temperature=0.2))

    # Fonction de sélection pour le simulateur de dialogue
    def select_next_speaker(step: int, agents: List[DialogueAgent]) -> int:
        if step % 2 == 0:
            idx = 0
        else:
            idx = (step//2) % (len(agents)-1) + 1
        return idx

    max_iters = 20
    n = 0

    simulator = DialogueSimulator(
        agents=[storyteller] + characters,
        selection_function=select_next_speaker
    )
    simulator.reset()
    simulator.inject(storyteller_name, quest_specifier_prompt)
    print(f"({storyteller_name}): {quest_specifier_prompt}")
    print('\n')

    while n < max_iters:
        name, message = simulator.step()
        print(f"({name}): {message}")
        print('\n')

        n += 1



