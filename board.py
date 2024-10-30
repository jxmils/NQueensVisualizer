from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt

class Board(QWidget):
    def __init__(self, n, queens=None):
        super().__init__()
        self.n = n
        self.queens = queens if queens else []
        self.setMinimumSize(400, 400)

    def set_queens(self, queens):
        self.queens = queens
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

    def draw_cell(self, qp, row, col, cell_width, cell_height):
        color = QColor(255, 255, 255) if (row + col) % 2 == 0 else QColor(100, 100, 100)
        qp.setBrush(QBrush(color, Qt.SolidPattern))
        qp.drawRect(col * cell_width, row * cell_height, cell_width, cell_height)

    def draw_queen(self, qp, row, col, cell_width, cell_height):
        qp.setBrush(QBrush(QColor(255, 0, 0), Qt.SolidPattern))
        qp.drawEllipse(col * cell_width, row * cell_height, cell_width, cell_height)
