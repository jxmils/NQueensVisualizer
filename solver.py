class Solver:
    def __init__(self, n):
        self.n = n
        self.solutions = []
        self.steps = []  # Store the algorithm's steps for visualization
        self.current_board = [-1] * n  # Track the current board state (which column each row's queen is placed)

    def solve(self):
        board = [-1] * self.n  # Store column positions of queens in each row
        self.steps = []  # Reset steps for visualization
        self.current_board = [-1] * self.n  # Reset the current board
        self.backtrack(board, 0)
        return self.solutions

    def is_safe(self, board, row, col):
        for i in range(row):
            if board[i] == col or abs(board[i] - col) == row - i:
                return False
        return True

    def backtrack(self, board, row):
        if row == self.n:
            solution = [(i, board[i]) for i in range(self.n)]
            self.solutions.append(solution)
            self.steps.append(("solution", solution))
        else:
            for col in range(self.n):
                self.steps.append(("try", row, col))  # Store step
                if self.is_safe(board, row, col):
                    board[row] = col
                    self.backtrack(board, row + 1)
                    board[row] = -1
                self.steps.append(("backtrack", row, col))  # Store backtrack step