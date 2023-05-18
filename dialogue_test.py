# dialogue_test.py

from langchain.chat_models import ChatOpenAI
from settings import build_analyze_message_for_stat_check_prompt, build_analyze_message_for_context_check_prompt
from character import get_stat_value
from dice import ask_for_dice_roll, perform_skill_check
from game_utils import parse_response1, parse_context_response

class TestCheck:
    def __init__(self, simulator, message):
        self.simulator = simulator
        self.message = message

    def check_for_stat_test(self):
        analyze_message_for_stat_check_prompt = build_analyze_message_for_stat_check_prompt(self.message)
        response1 = ChatOpenAI(temperature=0.5)(analyze_message_for_stat_check_prompt).content
        parsed_response1 = parse_response1(response1)
        print(parsed_response1)
        return parsed_response1

class DiceRoll:
    def __init__(self, parsed_response1, name):
        self.parsed_response1 = parsed_response1
        self.character_name = name
        self.dice_roll_text = ""

    def perform_dice_roll(self):
        self.parsed_response1["Player"] = self.character_name
        stat_to_check = self.parsed_response1["Stats"]
        print(f"Stats à vérifier : {stat_to_check}")  # Ajouté pour le débogage
        stat_value = get_stat_value(self.character_name, stat_to_check)
        dice_roll = ask_for_dice_roll(self.character_name)
        success = perform_skill_check(dice_roll, stat_value)
        success_action = "succès" if success else "échec"
        self.dice_roll_text = self.test_jet_prompt(success_action, self.parsed_response1["Player"],
                                                   self.parsed_response1["action"])
        return success_action, self.dice_roll_text

    @staticmethod
    def test_jet_prompt(success_action, player, action):
        if success_action == "succès":
            return f"""L'action du joueur {player} qui est d'avoir {action} a du subir un test de jet de dé qui a été un succès. Adapte ta réponse en conséquence"""
        elif success_action == "échec":
            return f"""L'action du joueur {player} qui est d'avoir {action} a du subir un test de jet de dé qui a été un échec. Adapte ta réponse en conséquence"""
        else:
            return ""

class ContextCheck:
    def __init__(self, simulator, message):
        self.simulator = simulator
        self.message = message

    def check_context(self):
        analyze_message_for_context_check_prompt = build_analyze_message_for_context_check_prompt(self.message)
        response1 = ChatOpenAI(temperature=0.5)(analyze_message_for_context_check_prompt).content
        parsed_context_response = parse_context_response(response1)

        return parsed_context_response
