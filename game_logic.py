"""
Module Name: game_logic.py
Class Name: GameLogic

Description: This manages the game logic, such as uncovering cells, recursively revealing cells with no adjacent mines, toggling flags, tracking remaining flags, and checking status of the game.
Inputs: board_manager. uncover_cell() and toggle_flag() take a row and column to identify the selected cell.
Outputs: uncover_cell() and toggle_flag() update the state of the selected cells. check_game_state() returns "Playing", "Game Over: Loss", or "Victory".

Authors: Ximena Bustos, Jaydine Stiles
Creation Date(s): 09/14/26
External Sources: https://www.askpython.com/python/examples/create-minesweeper-using-python, ChatGPT

Basic Code Template/Outline: Marie Biernacki, Gemini
"""

from PyQt5.QtCore import QSize, Qt, QElapsedTimer
from PyQt5.QtWidgets import QLineEdit, QMainWindow, QApplication, QPushButton
from board_manager import BoardManager

class Game():
    def __init__(self, num_mines):
        self.board = BoardManager()
        self.num_mines = num_mines
        self.remaining_flags = num_mines
        self.game_state = "Playing"
        self.first_uncover = True
        self.elapsed = QElapsedTimer() # timer in ms

    def uncover_cell(self, row: int, col: int) -> None:
            if row < 0 or row >= self.board.rows or col < 0 or col >= self.board.cols: #check if the coordinates are outside the board
                return #stop if the coordinates are invalid

            if self.first_uncover: #place mines around the first click so it is always safe
                self.board.place_mines(self.num_mines, row, col)
                self.first_uncover = False
                self.start_timer()

            cell = self.board.get_cell(row, col) #get the selected cell
    
            if cell.state == 2: #clicking a revealed number attempts to chord
                self.chord_cell(row, col)
                return

            if cell.state == 1 or cell.state == 3: #check if the cell is flagged or already a revealed mine
                return #stop if the cell cannot be uncovered
    
            if cell.is_mine: #check if the selected cell contains a mine
                cell.state = 3 #reveal the mine
                return #stop without revealing neighboring cells
    
            if cell.adjacent_mines == 0: #check if the cell has no adjacent mines
                self.recursive_reveal(row, col) #recursively uncover the cell and its neighbors
            else: #handle cells that have adjacent mines
                cell.state = 2 #uncover the selected cell

    def chord_cell(self, row: int, col: int) -> None:
        cell = self.board.get_cell(row, col)
        neighbors = self.board.get_neighbors(row, col)
        flag_count = sum(neighbor.state == 1 for neighbor in neighbors)

        if cell.adjacent_mines == 0 or flag_count != cell.adjacent_mines:
            return

        for neighbor_row in range(max(0, row - 1), min(self.board.rows, row + 2)):
            for neighbor_col in range(max(0, col - 1), min(self.board.cols, col + 2)):
                if neighbor_row == row and neighbor_col == col:
                    continue

                neighbor = self.board.get_cell(neighbor_row, neighbor_col)
                if neighbor.state != 0:
                    continue

                if neighbor.is_mine:
                    neighbor.state = 3
                elif neighbor.adjacent_mines == 0:
                    self.recursive_reveal(neighbor_row, neighbor_col)
                else:
                    neighbor.state = 2

    def recursive_reveal(self, row: int, col: int) -> None:
        if row < 0 or row >= self.board.rows or col < 0 or col >= self.board.cols: #check if the coordinates are outside the board
            return #stop if the coordinates are invalid

        cell = self.board.get_cell(row, col) #get the current cell

        if cell.state != 0 or cell.is_mine: #check if the cell is already uncovered, flagged, or contains a mine
            return #stop if the cell should not be revealed

        cell.state = 2 #uncover the current cell

        if cell.adjacent_mines != 0: #check if the cell has adjacent mines
            return #stop recursion when a numbered cell is reached

        neighbors = self.board.get_neighbors(row, col) #get the neighboring cells

        for neighbor_row in range(max(0, row - 1), min(self.board.rows, row + 2)): #loop through the surrounding rows within the board
            for neighbor_col in range(max(0, col - 1), min(self.board.cols, col + 2)): #loop through the surrounding columns within the board
                neighbor = self.board.get_cell(neighbor_row, neighbor_col) #get the neighboring cell

                if neighbor in neighbors: #check if the cell is in the neighbor list
                    self.recursive_reveal(neighbor_row, neighbor_col) #recursively reveal the neighboring cell

    def toggle_flag(self, row: int, col: int) -> None:
        # Checks if the row and column are inside of the board.
        # Ignores coordinates ouside of the board.
        if row < 0 or row >= self.board.rows or col < 0 or col >= self.board.cols:
            return
        
        # Gets the cell object at the selected row and column.
        cell = self.board.get_cell(row, col)

        # This doesn't allow revealed cells to be flagged.
        # 2 = revealed safe cell and 3 = revealed mine.
        if cell.state == 2 or cell.state == 3:
            return
        
        # Removes an existing flag, it already flagged.
        # 1 = cell currently has a flag.
        if cell.state == 1:
            cell.state = 0
            self.remaining_flags += 1       # Removing the flag gives the player one more flag.

        # If the cell is hiiden and there are flags available, places a flag on the cell.
        # 0 = cell is currently hidden.
        elif cell.state == 0 and self.remaining_flags > 0:
            cell.state = 1
            self.remaining_flags -= 1       # Placed flag means using the player's available flags.
        

    def check_game_state(self) -> str:
        # Goes through every cell on the board to check if the player 
        # has revealed a mine.
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                cell = self.board.get_cell(row, col)

                # 3 = mine had been revealed.
                # Played has lost the game.
                if cell.state == 3:
                    self.game_state = "Game Over: Loss"
                    return self.game_state
                
        # If no mine has been revealed, checks whether the player
        # has revealed every cell that is not a mine.
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                cell = self.board.get_cell(row, col)

                # If the cell is not a mine and it hasn't been revealed,
                # there are more safe cells to be uncovered.
                if not cell.is_mine and cell.state != 2:
                    self.game_state = "Playing"
                    return self.game_state
                
        # All safe cells have been revealed.
        # The player has won.
        self.game_state = "Victory"
        return self.game_state    

    def start_timer(self):
        self.elapsed.start()

    def get_timer(self):
        if not self.elapsed.isValid():
            return "00:00:00"
        
        ms = self.elapsed.elapsed()
        minutes, ms = divmod(ms, 60_000)
        seconds, ms = divmod(ms, 1000)
        return f"{minutes:02}:{seconds:02}.{ms // 10:02}"