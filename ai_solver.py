"""
Module Name: ai_solver.py
Class Name: AI Solver

Description: ai_solver.py is able to play the game. each turn
	it iterates through the board collecting indeces of different states
	into different arrays. 
Inputs: Difficulty value
Outputs: Changes to be made to the cells

Authors: Eyassu Mongalo
Creation Date(s): 9/25/2026
"""
from enum import Enum
from board_manager import BoardManager

class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

class Mode(Enum):
    INTERACTIVE = 1
    SOLVER = 2
    NONE = 3

class AiSolver:
	def __init__(self, difficulty: Difficulty):
		self.difficulty = difficulty;
		self.covered = set();
		self.fallback = None;
		self.flag = set();


	def clear(self):
		self.covered = set()
		self.fallback = None
		self.flag = set()

	def generate_changes(self, board: BoardManager):
		fallback_set = set()
		for row in range(10):
			for col in range(10):
				covered = board.covered_neighbors(row, col)
				cell = board.get_cell(row, col)
				if cell.state == 0:
					fallback_set.add((row, col))
				if cell.state != 2:
				    continue
				mine_count = cell.adjacent_mines
				flagged = board.get_flagged_neighbors(row, col)
				print(covered, flagged, row, col)
				if flagged == mine_count:
					for cell in covered:
						self.covered.add(cell)
				elif len(covered) + flagged == mine_count:
					for cell in covered:
						self.flag.add(cell)
		if len(self.covered) == len(self.flag) == 0:
			self.fallback = fallback_set.pop()

