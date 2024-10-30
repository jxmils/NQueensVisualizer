class Solver:
    def __init__(self, n):
        self.n = n
        self.solutions = []

    def solve(self):
        board = [-1] * self.n  # This will store the column positions of queens in each row
        self.backtrack(board, 0)
        return self.solutions

    def is_safe(self, board, row, col):
        for i in range(row):
            if board[i] == col or abs(board[i] - col) == row - i:
                return False
        return True

    def backtrack(self, board, row):
        if row == self.n:
            # We found a solution
            solution = [(i, board[i]) for i in range(self.n)]
            self.solutions.append(solution)
        else:
            for col in range(self.n):
                if self.is_safe(board, row, col):
                    board[row] = col
                    self.backtrack(board, row + 1)
                    board[row] = -1
