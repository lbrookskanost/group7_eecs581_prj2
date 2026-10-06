from pathlib import Path
import json

LEADERBOARD_FILE_NAME = "leaderboard.json"

def update_leaderboard(n_bombs, time):
    leaderboard_path = Path(LEADERBOARD_FILE_NAME)

    if leaderboard_path.exists():
        with open(LEADERBOARD_FILE_NAME, "r") as file:
            data = json.load(file)
        if n_bombs not in data or data[str(n_bombs)] > time:
            data[str(n_bombs)] = time
        with open(LEADERBOARD_FILE_NAME, "w") as file:
            json.dump(data, file)
    else:
        with open(LEADERBOARD_FILE_NAME, "w") as file:
            data = { n_bombs : time}
            json.dump(data, file)