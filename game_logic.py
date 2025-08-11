# game_logic.py
def determine_winner(choice1, choice2):
    if choice1 == choice2:
        return "draw"
    wins = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper"
    }
    return "win" if wins.get(choice1) == choice2 else "lose"
