from pathlib import Path
import json
from ai_solver import Mode

LEADERBOARD_FILE_NAME = "leaderboard.json"

def update_leaderboard(n_bombs, time, mode: Mode):
    leaderboard_path = Path(LEADERBOARD_FILE_NAME)
    mode = "AI Assisted" if mode == Mode.INTERACTIVE else "Unassisted" 

    if leaderboard_path.exists():
        with open(LEADERBOARD_FILE_NAME, "r") as file:
            data = json.load(file)
        if mode not in data:
            data[mode] = dict()
        if n_bombs not in data[mode] or data[mode][str(n_bombs)] > time:
            data[mode][str(n_bombs)] = time
        with open(LEADERBOARD_FILE_NAME, "w") as file:
            json.dump(data, file)
    else:
        with open(LEADERBOARD_FILE_NAME, "w") as file:
            data = {mode : {n_bombs : time}}
            json.dump(data, file)
