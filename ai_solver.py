"""
Module Name: ai_solver.py
Class Name: AI Solver

Description: ai_solver.py is able to play the game. each turn
	it iterates through the board collecting indeces of different states
	into different arrays. 
Inputs: Difficulty value
Outputs: Cell objects and their neighboring cells, updates board with mine
        locations 

Authors: Eyassu Mongalo
Creation Date(s): 9/25/2026
"""
from enum import Enum

class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

class AiSolver:
	def __init__(self, difficulty: Difficulty) -> AiSolver:
		self.difficulty = difficulty;

