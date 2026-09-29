from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QButtonGroup,
    QVBoxLayout,
    QWidget,
)
from game_logic import Game
from ai_solver import Difficulty, Mode
from styles import NUMBER_COLORS, covered, flagged, uncovered


class CellButton(QPushButton):
    rightClicked = pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.rightClicked.emit()
        else:
            super().mousePressEvent(event)  # keep normal left-click/clicked() behavior

class StartGameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Minesweeper Setup")
        self.num_mines = None

        self.bomb_input = QLineEdit()
        self.bomb_input.setMaxLength(2)
        self.bomb_input.setPlaceholderText("10 - 20")
        self.bomb_error = QLabel("")
        self.start_button = QPushButton("Start Game")
        self.mode_btns = []
        self.diff_btns = [QLabel("Choose AI Difficulty:")]
        self.selected_mode = Mode.NONE
        self.selected_difficulty = Difficulty.HARD

        self._initialize_ai_prompt()

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Enter number of mines (10-20):"))
        layout.addWidget(self.bomb_input)
        layout.addWidget(self.bomb_error)
        layout.addWidget(QLabel("Choose AI Mode:"))
        for btn in self.mode_btns:
            layout.addWidget(btn)
        for btn in self.diff_btns:
            layout.addWidget(btn)
        self.setLayout(layout)


        layout.addWidget(self.start_button)
        self.bomb_input.returnPressed.connect(self.submit)
        self.start_button.clicked.connect(self.submit)

    def _initialize_ai_prompt(self):
        options = [
            ("Interactive" , Mode.INTERACTIVE ),
            ("Solver"      , Mode.SOLVER      ),
            ("None"        , Mode.NONE        )
        ]

        ai_difficulty = [
            ("Easy"   , Difficulty.EASY   ),
            ("Medium" , Difficulty.MEDIUM ),
            ("Hard"   , Difficulty.HARD   )
        ]

        btn_set = QButtonGroup(self);
        difficulty_set = QButtonGroup(self);
        self.diff_btns[0].setVisible(False);

        for (txt, val) in options:
            btn = QRadioButton(txt)
            self.mode_btns.append(btn)
            if val == Mode.INTERACTIVE:
                btn.clicked.connect(lambda: self._set_visibility(Mode.INTERACTIVE))
            elif val == Mode.SOLVER:
                btn.clicked.connect(lambda: self._set_visibility(Mode.SOLVER))
            elif val == Mode.NONE:
                btn.clicked.connect(lambda: self._set_visibility(Mode.NONE))
            btn_set.addButton(btn)

        for (txt, val) in ai_difficulty:
            btn = QRadioButton(txt)
            btn.setVisible(False)
            self.diff_btns.append(btn)
            difficulty_set.addButton(btn)
            if val == Difficulty.EASY:
                btn.clicked.connect(lambda: self._set_diff(Difficulty.EASY))
            elif val == Difficulty.MEDIUM:
                btn.clicked.connect(lambda: self._set_diff(Difficulty.MEDIUM))
            elif val == Difficulty.HARD:
                btn.clicked.connect(lambda: self._set_diff(Difficulty.HARD))

        btn_set.buttons()[-1].setChecked(True)
        difficulty_set.buttons()[-1].setChecked(True)


    def _set_visibility(self, value):
        self.selected_mode = value
        if value != Mode.NONE:
            for btns in self.diff_btns:
                btns.setVisible(True)
        else:
            for btns in self.diff_btns:
                btns.setVisible(False)

    def _set_diff(self, value):
        self.diff_mode = value


    def check_bomb_input(self, input_text):
        try:
            num_mines = int(input_text)
        except ValueError:
            self.bomb_error.setText("Please enter a valid number.")
            return None

        if 10 <= num_mines <= 20:
            return num_mines

        self.bomb_error.setText("Please enter a number between 10 and 20.")
        return None

    def submit(self):
        num_mines = self.check_bomb_input(self.bomb_input.text())
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
        #snap to grid
        grid_widget = QWidget()
        grid_widget.setLayout(grid)

        layout = QVBoxLayout()
        layout.addLayout(top_bar)
        #keep it center-aligned
        layout.addWidget(grid_widget, alignment=Qt.AlignHCenter | Qt.AlignVCenter) 
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.adjustSize()

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
