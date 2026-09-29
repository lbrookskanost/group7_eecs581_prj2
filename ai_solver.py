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

	def _collect():
		pass
	


