from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGridLayout, QLabel, QHBoxLayout, QSlider
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QTimer

class Board(QWidget):
    def __init__(self, n, queens=None):
        super().__init__()
        self.n = n
        self.queens = queens if queens else []
        self.highlighted_cell = (-1, -1)  # Cell to highlight for visual feedback
        self.setMinimumSize(400, 400)

    def set_queens(self, queens):
        self.queens = queens
        self.update()

    def highlight_cell(self, row, col):
        self.highlighted_cell = (row, col)
        self.update()

    def clear_highlight(self):
        self.highlighted_cell = (-1, -1)
        self.update()

    def paintEvent(self, event):
        qp = QPainter(self)
        size = self.size()
        cell_width = size.width() // self.n
        cell_height = size.height() // self.n

        for row in range(self.n):
            for col in range(self.n):
                self.draw_cell(qp, row, col, cell_width, cell_height)

        for row, col in self.queens:
            self.draw_queen(qp, row, col, cell_width, cell_height)

        # Highlight the current cell
        if self.highlighted_cell != (-1, -1):
            self.draw_highlight(qp, self.highlighted_cell[0], self.highlighted_cell[1], cell_width, cell_height)

    def draw_cell(self, qp, row, col, cell_width, cell_height):
        color = QColor(240, 240, 240) if (row + col) % 2 == 0 else QColor(100, 100, 100)
        qp.setBrush(QBrush(color, Qt.SolidPattern))
        qp.drawRect(col * cell_width, row * cell_height, cell_width, cell_height)

    def draw_queen(self, qp, row, col, cell_width, cell_height):
        qp.setBrush(QBrush(QColor(255, 0, 0), Qt.SolidPattern))
        qp.drawEllipse(col * cell_width, row * cell_height, cell_width, cell_height)

    def draw_highlight(self, qp, row, col, cell_width, cell_height):
        color = QColor(0, 255, 0, 150)  # Light green for highlight
        qp.setBrush(QBrush(color, Qt.SolidPattern))
        qp.drawRect(col * cell_width, row * cell_height, cell_width, cell_height)
