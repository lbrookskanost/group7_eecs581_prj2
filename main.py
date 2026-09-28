"""
Description: Handles the command line interface game loop and user input. Displays the board, validates player moves, and sends uncover or flag actions
to the game logic.
Inputs: Number of mines (10-20), column (A-J), row (1-10), and action (U or F).
Outputs: Displays the 10x10 game board, game status, and final win or loss message.

Author: Sabelli Antebi Delmas
Creation Date: 09-13-2026
External Sources: https://www.askpython.com/python/examples/create-minesweeper-using-python used this to help me clear some of my doubts a
nd ideas a little better. 

Basic Code Template/Outline: Marie Biernacki, Gemini
"""

from game_logic import Game
from board_manager import BoardManager
from PyQt5.QtWidgets import QApplication, QDialog
from display import BombInputDialog, GameWindow

def main():

    app = QApplication([])

    setup = BombInputDialog() #blocks until a valid mine count is entered or the user cancels
    print("Starting Minesweeper Setup...")
    if setup.exec() != QDialog.Accepted:
        return

    num_mines = setup.num_mines
    window = GameWindow(num_mines)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()


