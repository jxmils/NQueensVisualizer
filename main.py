from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QSpinBox
import sys

from board import Board
from solver import Solver


class NQueensApp(QWidget):
    def __init__(self):
        super().__init__()

        self.n = 8  # Default board size
        self.solver = Solver(self.n)
        self.solutions = []

        # UI Elements
        self.board = Board(self.n)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.board)

        self.controls_layout = QVBoxLayout()

        self.size_selector = QSpinBox()
        self.size_selector.setMinimum(4)
        self.size_selector.setValue(self.n)
        self.size_selector.valueChanged.connect(self.change_board_size)
        self.controls_layout.addWidget(self.size_selector)

        self.solve_button = QPushButton("Solve")
        self.solve_button.clicked.connect(self.solve)
        self.controls_layout.addWidget(self.solve_button)

        self.next_button = QPushButton("Next Solution")
        self.next_button.clicked.connect(self.show_next_solution)
        self.controls_layout.addWidget(self.next_button)

        self.layout.addLayout(self.controls_layout)

        self.setLayout(self.layout)
        self.current_solution_index = -1

    def change_board_size(self):
        self.n = self.size_selector.value()
        self.board.n = self.n
        self.solver = Solver(self.n)
        self.solutions = []
        self.board.set_queens([])

    def solve(self):
        self.solutions = self.solver.solve()
        if self.solutions:
            self.current_solution_index = 0
            self.board.set_queens(self.solutions[0])

    def show_next_solution(self):
        if self.solutions:
            self.current_solution_index = (self.current_solution_index + 1) % len(self.solutions)
            self.board.set_queens(self.solutions[self.current_solution_index])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NQueensApp()
    window.show()
    sys.exit(app.exec_())
