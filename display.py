from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from game_logic import Game
from styles import NUMBER_COLORS, covered, flagged, uncovered

class BombInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Minesweeper Setup")
        self.num_mines = None

        self.input = QLineEdit()
        self.input.setMaxLength(2)
        self.input.setPlaceholderText("10 - 20")
        self.error = QLabel("")
        self.start_button = QPushButton("Start Game")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Enter number of mines (10-20):"))
        layout.addWidget(self.input)
        layout.addWidget(self.error)
        layout.addWidget(self.start_button)
        self.setLayout(layout)

        self.input.returnPressed.connect(self.submit)
        self.start_button.clicked.connect(self.submit)

    def check_bomb_input(self, input_text):
        try:
            num_mines = int(input_text)
        except ValueError:
            self.error.setText("Please enter a valid number.")
            return None

        if 10 <= num_mines <= 20:
            return num_mines

        self.error.setText("Please enter a number between 10 and 20.")
        return None

    def submit(self):
        num_mines = self.check_bomb_input(self.input.text())
        if num_mines is None:
            return
        self.num_mines = num_mines
        self.accept()


class GameWindow(QMainWindow):
    def __init__(self, num_mines):
        super().__init__()

        self.setWindowTitle("Minesweeper")
        self.game = Game(num_mines)

        board = self.game.board
        grid = QGridLayout()
        grid.setSpacing(1)

        self.buttons = []
        for row in range(board.rows):
            button_row = []
            for col in range(board.cols):
                button = QPushButton()
                button.setFixedSize(QSize(32, 32))
                button.setStyleSheet(covered)
                button.clicked.connect(lambda _, r=row, c=col: self.cell_clicked(r, c))
                grid.addWidget(button, row, col)
                button_row.append(button)
            self.buttons.append(button_row)

        container = QWidget()
        container.setLayout(grid)
        self.setCentralWidget(container)

    def cell_clicked(self, row, col):
        self.game.uncover_cell(row, col)
        self.update_ui()

    def update_ui(self):
        board = self.game.board
        for row in range(board.rows):
            for col in range(board.cols):
                cell = board.get_cell(row, col)
                button = self.buttons[row][col]
                if cell.state == 0:
                    button.setStyleSheet(covered)
                elif cell.state == 1:
                    button.setStyleSheet(flagged)
                elif cell.state == 2:
                    if cell.adjacent_mines == 0:
                        button.setText(" ")
                        button.setStyleSheet(uncovered)
                    else:
                        button.setText(str(cell.adjacent_mines))
                        number_color = NUMBER_COLORS.get(cell.adjacent_mines)
                        button.setStyleSheet(f"{uncovered}\nQPushButton {{ color: {number_color}; }}")
                elif cell.state == 3:
                    button.setText("*")
                    button.setStyleSheet(uncovered)
                else:
                    raise ValueError("Invalid cell state.")
