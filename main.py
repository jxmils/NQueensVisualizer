from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QSlider, QLabel, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt, QTimer
import sys

from board import Board
from solver import Solver

class NQueensApp(QWidget):
    def __init__(self):
        super().__init__()

        self.n = 8  # Default board size
        self.solver = Solver(self.n)
        self.solutions = []
        self.current_step = 0
        self.final_solution_shown = False

        # UI Elements
        self.main_layout = QHBoxLayout()  # Main layout to hold board and pseudocode

        # Chessboard on the left
        self.board_layout = QVBoxLayout()
        self.board = Board(self.n)
        self.board_layout.addWidget(self.board)

        # Controls below the board
        self.controls_layout = QHBoxLayout()

        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(10, 1000)
        self.speed_slider.setValue(500)
        self.controls_layout.addWidget(self.speed_slider)

        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_algorithm)
        self.controls_layout.addWidget(self.play_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_algorithm)
        self.controls_layout.addWidget(self.pause_button)

        self.step_button = QPushButton("Step")
        self.step_button.setAutoRepeat(True)
        self.step_button.setAutoRepeatDelay(100)
        self.step_button.setAutoRepeatInterval(100)
        self.step_button.clicked.connect(self.step_algorithm)
        self.controls_layout.addWidget(self.step_button)

        self.skip_button = QPushButton("Skip")
        self.skip_button.clicked.connect(self.skip_to_solution)
        self.controls_layout.addWidget(self.skip_button)

        self.board_layout.addLayout(self.controls_layout)

        # Pseudocode display on the right
        self.pseudocode_display = QTextEdit()
        self.pseudocode_display.setReadOnly(True)  # Make it non-editable

        # Descriptive pseudocode with modern styling and lighter unhighlighted text
        self.pseudocode = """
<pre style="font-family: 'Courier New', monospace; font-size: 14px; color: #999999;">
1.  NQueens(n):
2.    Call PlaceQueen(row = 0)
3.    
4.    PlaceQueen(row):
5.      If row == n:
6.        A valid solution is found, store the solution
7.        Return to explore other possibilities (backtrack)
8.      For each column from 0 to n-1:
9.        Check if placing a queen at (row, col) is safe:
10.         - Ensure no queens threaten this position
11.       If safe:
12.         Place Queen at (row, col)
13.         Call PlaceQueen(row + 1) to place the next queen
14.         Remove Queen from (row, col) (backtrack to explore other options)
15.       Continue checking the next column
</pre>
"""
        self.pseudocode_display.setHtml(self.pseudocode)  # Set initial modern pseudocode

        # Add the board and pseudocode layouts to the main layout
        self.main_layout.addLayout(self.board_layout)
        self.main_layout.addWidget(self.pseudocode_display)

        # Set up the window layout
        self.setLayout(self.main_layout)

        # Add a status label
        self.status_label = QLabel("Ready")
        self.board_layout.addWidget(self.status_label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.step_algorithm)

    def solve(self):
        self.solutions = self.solver.solve()
        self.current_step = 0
        print(f"Total steps: {len(self.solver.steps)}")  # Debugging print

    def play_algorithm(self):
        if not self.solutions:
            self.solve()
        if self.final_solution_shown:
            self.reset_board()
        else:
            self.status_label.setText("Solving...")
            self.timer.start(self.speed_slider.value())

    def pause_algorithm(self):
        self.timer.stop()

    def step_algorithm(self):
        if self.current_step < len(self.solver.steps):
            step = self.solver.steps[self.current_step]
            self.current_step += 1

            # Update pseudocode highlighting based on the current step type
            if step[0] == "try":
                self.highlight_pseudocode(11)  # Trying to place a queen
                self.solver.current_board[step[1]] = step[2]
                self.board.set_queens([(i, self.solver.current_board[i]) for i in range(self.n) if self.solver.current_board[i] != -1])
                self.board.highlight_cell(step[1], step[2])
                self.board.update()
            elif step[0] == "backtrack":
                self.highlight_pseudocode(14)  # Backtracking (removing a queen)
                self.solver.current_board[step[1]] = -1
                self.board.clear_highlight()
                self.board.set_queens([(i, self.solver.current_board[i]) for i in range(self.n) if self.solver.current_board[i] != -1])
                self.board.update()
            elif step[0] == "solution":
                self.highlight_pseudocode(6)  # Solution found
                self.board.set_queens(step[1])
                self.board.update()
        else:
            self.timer.stop()
            self.status_label.setText("Solving complete!")
            self.show_completion_dialog()
            self.final_solution_shown = True
            self.play_button.setText("New")
            self.disable_control_buttons()

    def highlight_pseudocode(self, line):
        """Highlight the given line number in the pseudocode."""
        lines = self.pseudocode.splitlines()
        highlighted_code = ""
        for i, code_line in enumerate(lines):
            if i + 1 == line:
                highlighted_code += f'<span style="font-weight: bold; color: #ffffff;">{code_line}</span>\n'  # Highlight the current line with bold and lighter color
            else:
                highlighted_code += f"{code_line}\n"
        
        formatted_code = f"""
<pre style="font-family: 'Courier New', monospace; font-size: 14px; color: #999999;">
{highlighted_code}
</pre>
"""
        self.pseudocode_display.setHtml(formatted_code)  # Update the display with modern styling

    def skip_to_solution(self):
        if not self.solutions:
            self.solve()
        self.timer.stop()
        final_solution = self.solver.solutions[-1]
        self.board.set_queens(final_solution)
        self.board.update()
        self.status_label.setText("Final solution shown!")
        self.final_solution_shown = True
        self.play_button.setText("New")
        self.disable_control_buttons()

    def disable_control_buttons(self):
        self.skip_button.setEnabled(False)
        self.step_button.setEnabled(False)
        self.pause_button.setEnabled(False)

    def show_completion_dialog(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText("The N-Queens problem is solved!")
        msg_box.setWindowTitle("Solving Complete")
        msg_box.exec_()

    def reset_board(self):
        self.solver = Solver(self.n)
        self.solutions = []
        self.current_step = 0
        self.final_solution_shown = False
        self.board.set_queens([])
        self.status_label.setText("Ready")
        self.play_button.setText("Play")
        self.skip_button.setEnabled(True)
        self.step_button.setEnabled(True)
        self.pause_button.setEnabled(True)
        self.pseudocode_display.setHtml(self.pseudocode)  # Reset the pseudocode display

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NQueensApp()
    window.show()
    sys.exit(app.exec_())
