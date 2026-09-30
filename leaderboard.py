from pathlib import Path
LEADERBOARD_FILE_NAME = "leaderboard.txt"

def update_leaderboard(time):

    leaderboard_path = Path(LEADERBOARD_FILE_NAME)

    if leaderboard_path.exists():
        with open(LEADERBOARD_FILE_NAME, "r+") as file:
            leaderboard = file.read()
            for leaderboard_char, time_char in zip(leaderboard, time):
                if time_char < leaderboard_char:
                    file.write(time)
                    break
    else:
        with open(LEADERBOARD_FILE_NAME, "w") as file:
            file.write(time)