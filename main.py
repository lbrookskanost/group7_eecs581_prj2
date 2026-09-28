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

    '''
    first_uncover = True #keep track of whether the first cell was uncovered
    game = None #game logic does not exist until mines are placed

    while True:  #keep the game running until win or loss

        if game is not None: #check if game logic was created
            game_state = game.check_game_state() #get the current state from game logic
            print("Flags Remaining:", game.remaining_flags) #show remaining flags 
            print("Status:", game_state) #show current game status


            if game_state != "Playing": #check if the game is no longer playing
                break #leave the game loop

        user_input = input("Move: ").strip().upper().split() #get the move, remove extra spaces, make uppercase, and separate values

        if len(user_input) != 3: #check if the user entered exactly three values
            print("Invalid input. Example: A 5 U") #show the correct input format
            continue  #restart the loop
        
        col_input = user_input[0] #save the first value as the column
        row_input = user_input[1] #save the second value as the row
        action = user_input[2] #save the third value as the action
        
        if col_input not in "ABCDEFGHIJ" or len(col_input) != 1: #check if the column is between A and J
            print("Column must be A-J.") #tell the user the valid column range
            continue #restart the loop

        try: #try to convert the row into a number
            row = int(row_input) #convert the row input into an integer
            if row < 1 or row > 10: #check if the row is outside the board
                print("Row must be 1-10.") #tell the user the valid row range
                continue #restart the loop

        except ValueError: #handle a row that is not a number

            print("Row must be a number from 1-10.") #tell the user what type of value is needed
            continue #restart the loop

        if action not in ("U", "F"): #check if the action is uncover or flag
            print("Action must be U for uncover or F for flag.") #tell the user the valid actions
            continue #restart the loop

        row_index = row - 1 #change row 1-10 into index 0-9
        col_index = ord(col_input) - ord("A") #change column A-J into index 0-9

        if first_uncover and action == "U": #check if this is the first uncover
            board.place_mines(num_mines, row_index, col_index)#place mines while keeping the first cell safe
            game = GameLogic(board) #create the game logic using the board
            game.uncover_cell(row_index, col_index) #uncover the first selected cell
            first_uncover = False #mark that the first uncover already happened
            continue #restart the loop and show the updated board

        if first_uncover and action == "F": #check if the user tries to flag before the first uncover
            print("Please uncover a cell before placing flags.") #tell the user to uncover first
            continue #restart the loop

        if action == "U": #check if the action is uncover
            game.uncover_cell(row_index, col_index) #send the uncover action to game logic
        elif action == "F": #check if the action is flag
            game.toggle_flag(row_index, col_index) #send the flag action to game logic 
'''

if __name__ == "__main__":
    main()


