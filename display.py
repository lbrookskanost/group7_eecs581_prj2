from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from game_logic import Game
from styles import NUMBER_COLORS, covered, flagged, uncovered


class CellButton(QPushButton):
    rightClicked = pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.rightClicked.emit()
        else:
            super().mousePressEvent(event)  # keep normal left-click/clicked() behavior


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

        for col in range(board.cols):
            label = QLabel(chr(ord("A") + col))
            label.setAlignment(Qt.AlignCenter)
            grid.addWidget(label, 0, col + 1)

        for row in range(board.rows):
            label = QLabel(str(row + 1))
            label.setAlignment(Qt.AlignCenter)
            grid.addWidget(label, row + 1, 0)

        self.buttons = []
        for row in range(board.rows):
            button_row = []
            for col in range(board.cols):
                button = CellButton()
                button.setFixedSize(QSize(32, 32))
                button.setStyleSheet(covered)
                button.clicked.connect(lambda _, r=row, c=col: self.cell_clicked(r, c))
                button.rightClicked.connect(lambda r=row, c=col: self.cell_right_clicked(r, c))
                grid.addWidget(button, row + 1, col + 1)
                button_row.append(button)
            self.buttons.append(button_row)

        self.flag_label = QLabel(f"Flags: {self.game.remaining_flags}")
        self.timer_label = QLabel("PUT TIMER HERE")
        self.state_label = QLabel(self.game.check_game_state())

        top_bar = QHBoxLayout()
        top_bar.addWidget(self.flag_label)
        top_bar.addStretch()
        top_bar.addWidget(self.state_label)
        top_bar.addStretch()
        top_bar.addWidget(self.timer_label)

        layout = QVBoxLayout()
        layout.addLayout(top_bar)
        layout.addLayout(grid)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def cell_clicked(self, row, col):
        self.game.uncover_cell(row, col)
        self.update_ui()

    def cell_right_clicked(self, row, col):
        self.game.toggle_flag(row, col)
        self.update_ui()

    def update_ui(self):
        board = self.game.board
        self.state_label.setText(self.game.check_game_state())
        self.flag_label.setText(f"Flags: {self.game.remaining_flags}")
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
