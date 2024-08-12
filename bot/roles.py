import random

def generate_roles(num_players):
    if num_players == 4:
        roles = ["Civilian"] * 3 + ["Mafia"]
    elif num_players == 5:
        roles = ["Civilian"] * 4 + ["Mafia"]
    elif num_players == 6:
        roles = ["Civilian"] * 4 + ["Mafia", "Sheriff", "Don"]
    elif num_players == 7:
        roles = ["Civilian"] * 4 + ["Mafia", "Don", "Sheriff"]
    elif num_players == 8:
        roles = ["Civilian"] * 5 + ["Mafia", "Don", "Sheriff"]
    elif num_players == 9:
        roles = ["Civilian"] * 5 + ["Mafia"] * 2 + ["Don", "Sheriff"]
    elif num_players == 10:
        roles = ["Civilian"] * 6 + ["Mafia"] * 2 + ["Don", "Sheriff"]
    else:
        raise ValueError("Invalid number of players. Must be between 4 and 10.")

    random.shuffle(roles)
    return roles

def format_roles_message(roles):
    result_message = "Players and roles:\n"
    for i, role in enumerate(roles):
        result_message += f"{i + 1} - {role}\n"
    return result_message
