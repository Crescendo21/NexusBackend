# dice.py

def ask_for_dice_roll(character_name):
    dice_roll = input(f"{character_name}, veuillez entrer le résultat de votre jet de dés (1-20): ")
    return int(dice_roll)

def perform_skill_check(dice_roll, stat_value):
    success = dice_roll > stat_value
    return success