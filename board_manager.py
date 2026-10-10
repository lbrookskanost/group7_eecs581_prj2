"""
Module Name: board_manager.py
Class Name: BoardManager

Description: board_manager.py manages the 10x10 grid. Creates and stores
            Cell objects, returns cells and their neighboring cells, 
            handles mine placements
Inputs: Row and column coordinates and mines
Outputs: Cell objects and their neighboring cells, updates board with mine
        locations 

Authors: Kaitlyn Bedgood, Lauren Lee, Sean Crosby, Eyassu Mongalo, Lillian Brooks-Kanost
Creation Date(s): 9/12/2026
External Sources:https://www.geeksforgeeks.org/python/python-using-2d-arrays-lists-the-right-way/
                https://www.geeksforgeeks.org/python/multi-dimensional-lists-in-python/
                I used these two GeeksforGeeks articles to help traverse through 2D Lists

Basic Code Template/Outline: Marie Biernacki, Gemini
"""

import random # need for random mine placement

class Cell:
    """    
    Attributes:
    - state (int): 0=covered, 1=flagged, 2=uncovered number, 3=mine
    - is_mine (bool): True if mine, False otherwise
    - adjacent_mines (int): Number of adjacent mines (0-8)
    """
    def __init__(self):
        # Initialize the following attributes to their default starting values:
        # self.state
        # self.is_mine
        # self.adjacent_mines
        self.state = 0
        self.is_mine = False
        self.adjacent_mines = 0

    def is_covered(self) -> bool:
        self.state == 0

class BoardManager:
    """
    Tasks: Board Management (Kaitlyn) & Mine Placement (Lauren)
    """
    def __init__(self):

        self.rows = 10
        self.cols = 10
        self.grid = [] #empty list that will hold rows of the board

        for row in range(self.rows): #loops ten times to create each row of board
            new_row = [] #empty list for cells in current row

            for col in range(self.cols): #loops 10 times to create col in current row
                new_row.append(Cell()) #create new cell object

            self.grid.append(new_row) #add row of cell objects to board

    def get_cell(self, row: int, col: int) -> Cell:
        
        return self.grid[row][col] #return cell object when given row and column

    def get_flagged_neighbors(self, row: int, col: int) -> int:
        flagged_neighbors = 0
        if (row < 0 or row >= self.rows or
          col < 0 or col >= self.cols): #check if row/col is outside board
            return flagged_neighbors

        for row_off in range(-1, 2):
            for col_off in range(-1, 2):
                neighbor_row = row + row_off #find row position of neighbor
                neighbor_col = col + col_off #find column position of neighbor
                if ((row_off != 0 or col_off != 0) and
                  0 <= neighbor_row < self.rows and
                  0 <= neighbor_col < self.cols and
					        self.grid[neighbor_row][neighbor_col].state == 1):
                    flagged_neighbors+=1

        return flagged_neighbors

    def covered_neighbors(self, row: int, col: int) -> list[(int, int)]:
        neighbors = []
        if (row < 0 or row >= self.rows or
          col < 0 or col >= self.cols): #check if row/col is outside board
            return neighbors

        for row_off in range(-1, 2):
            for col_off in range(-1, 2):
                neighbor_row = row + row_off #find row position of neighbor
                neighbor_col = col + col_off #find column position of neighbor
                if ((row_off != 0 or col_off != 0) and
                  0 <= neighbor_row < self.rows and
                  0 <= neighbor_col < self.cols and
					        self.grid[neighbor_row][neighbor_col].state == 0):
                    neighbors.append((neighbor_row, neighbor_col))

        return neighbors

    def get_potential_1_2_1(self, row: int, col: int) -> ([int], [int], [int]):
        unflag, uncover, flag = [], [], []
        if (row < 0 or row >= self.rows or
          col < 0 or col >= self.cols): #check if row/col is outside board
            return (unflag, uncover, flag)

        vert = True
        # Vertical Neighbors
        for row_off in range(-1, 2, 2): #skips 0
          neighbor_row = row + row_off
          vert = vert and ( 0 <= neighbor_row < self.rows and
			  self.grid[neighbor_row][col].state == 2 and # Want to find an uncovered 1
			  self.grid[neighbor_row][col].adjacent_mines == 1)
        if vert:
            if col - 1 >= 0:
                if self.grid[row][col - 1].state == 1:
                    unflag.append((row, col-1))
                uncover.append((row, col-1))
            
            if col + 1 < self.cols:
                if self.grid[row][col + 1].state == 1:
                    unflag.append((row, col+1))
                uncover.append((row, col+1))

            for col_off in range(-1, 2, 2): #skips 0
                for row_off in range(-1, 2, 2): #skips 0
                    neighbor_row = row + row_off
                    neighbor_col = col + col_off
                    if ( 0 <= neighbor_row < self.rows and
                      0 <= neighbor_col < self.cols and
                      self.grid[neighbor_row][neighbor_col].state == 2):
                        if self.grid[neighbor_row][col - col_off].state == 0:
                            # we guarantee that col - offset exists if the value at col+offset is uncovered       
                            flag.append((neighbor_row, col - col_off)) 
        hori = True
        # Horizontal Neighbors
        for col_off in range(-1, 2, 2): #skips 0
          neighbor_col = col + col_off
          hori = hori and ( 0 <= neighbor_col < self.cols and
					  self.grid[row][neighbor_col].state == 2 and
					  self.grid[row][neighbor_col].adjacent_mines == 1)
        if hori:
            if row - 1 >= 0:
                if self.grid[row - 1][col].state == 1:
                    unflag.append((row - 1, col))
                uncover.append((row - 1, col))
            
            if row + 1 < self.rows:
                if self.grid[row + 1][col].state == 1:
                    unflag.append((row+1, col))
                uncover.append((row+1, col))

            for col_off in range(-1, 2, 2): #skips 0
                for row_off in range(-1, 2, 2): #skips 0
                    neighbor_row = row + row_off
                    neighbor_col = col + col_off
                    if ( 0 <= neighbor_row < self.rows and
                      0 <= neighbor_col < self.cols and
                      self.grid[neighbor_row][neighbor_col].state == 2):
                        if self.grid[row - row_off][neighbor_col].state == 0:
                            # we guarantee that col - offset exists if the value at col+offset is uncovered
                            flag.append((row - row_off, neighbor_col)) 
        return (unflag, uncover, flag)

    def get_neighbors(self, row: int, col: int) -> list:
        
        neighbors = [] #empty list
        if row < 0 or row >= self.rows: #check if row is outside board
            return neighbors

        if col < 0 or col >= self.cols: #check if column is outside board
            return neighbors

        for row_offset in range(-1, 2): #check row above, current row, and row below
            for col_offset in range(-1, 2): #check col left, current col, and right col
                neighbor_row = row+ row_offset #find row position of neighbor
                neighbor_col = col + col_offset #find column position of neighbor
                if row_offset != 0 or col_offset != 0: #make sure original cell is not counted as its neighbor
                    if neighbor_row >= 0 and neighbor_row < self.rows: #check neighbor row is in board
                        if neighbor_col >=0  and neighbor_col < self.cols: #check if neighbor col is in board
                            neighbors.append(self.grid[neighbor_row][neighbor_col]) #append valid neighbor cell to list

        return neighbors


    def place_mines(self, num_mines: int, first_row: int, first_col: int) -> None:
        # Validate num_mines is between 10-20.
        # Randomly place mines, ensuring (first_row, first_col) is mine-free.
        # Validate that the number of mines is between 10 and 20.
        if num_mines < 10 or num_mines > 20:
            raise ValueError("Number of mines must be between 10 and 20.")

        self.num_mines = num_mines
        # Create a list of all board coordinates that can contain mines.
        # The first clicked cell is excluded to guarantee first-click safety.
        available_cells = []

        safe_spots = [(first_row-1, first_col-1), (first_row-1, first_col), (first_row-1, first_col+1), 
                      (first_row, first_col-1), (first_row, first_col), (first_row, first_col+1), 
                      (first_row+1, first_col-1), (first_row+1, first_col), (first_row+1, first_col+1)]

        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) not in safe_spots:
                    available_cells.append((row, col))

        # Randomly select locations for the mines.
        mine_locations = random.sample(available_cells, num_mines)

        # Place a mine in each randomly selected cell.
        for row, col in mine_locations:
            self.grid[row][col].is_mine = True

        # Calculate the number of mines surrounding every cell.
        for row in range(self.rows):
            for col in range(self.cols):
                # The mine itself does not need a neighbor mine count.
                # so if mine -> skip and continue to next cell
                if self.grid[row][col].is_mine:
                    continue
                
                # Count the number of mines in neighboring cells.
                mine_count = 0

                # Check every neighboring cell.
                for neighbor in self.get_neighbors(row, col):
                    # If the neighbor is a mine, increment the count.
                    if neighbor.is_mine:
                        mine_count += 1

                # Set the neighbor mine count for the current cell.
                self.grid[row][col].adjacent_mines = mine_count




