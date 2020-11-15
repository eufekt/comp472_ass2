import numpy as np

# file = np.loadtxt("samplePuzzles.txt", dtype="int64")
# puzzle = file[0]
# puzzle_2d = puzzle.reshape(height, width)

reg_cost = 1
wrap_cost = 2
diag_cost = 3


# global height
# global width
# # height = 2
# # width = 4
# global puzzle_2d

class Moves:

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.puzzle_2d = np.arange(height * width).reshape(height, width)

    def emtpy_index(self):
        return np.asarray(np.where(self.puzzle_2d == 0)).T[0]

    def row_index(self, index):
        if index < self.puzzle_2d.size:
            return (index // self.width) % self.height

    def col_index(self, index):
        if index < self.puzzle_2d.size:
            return index % self.width

    def index_to_2d(self, index):
        if index < self.puzzle_2d.size:
            return [index % self.width, (index // self.width) % self.height]

    def get_right_index(self, index):
        col = self.col_index(index)
        if col != (self.width - 1):
            return [self.row_index(index), col + 1]

    def get_left_index(self, index):
        col = self.col_index(index)
        if col != 0:
            return [self.row_index(index), col - 1]

    def get_up_index(self, index):
        col = self.col_index(index)
        row = self.row_index(index)
        if row != 0:
            return [row - 1, col]

    def get_down_index(self, index):
        col = self.col_index(index)
        row = self.row_index(index)
        if row != self.height - 1:
            return [row + 1, col]

    def get_wrap_up_index(self, index):
        col = self.col_index(index)
        row = self.row_index(index)
        if row == 0 and self.height > 2:
            return [self.height - 1, col]

    def get_wrap_down_index(self, index):
        col = self.col_index(index)
        row = self.row_index(index)
        if row == self.height - 1 and self.height > 2:
            return [0, col]

    def get_wrap_left_index(self, index):
        col = self.col_index(index)
        row = self.row_index(index)
        if col == 0:
            return [row, self.width - 1]

    def get_wrap_right_index(self, index):
        col = self.col_index(index)
        row = self.row_index(index)
        if col == self.width - 1:
            return [row, 0]

    def get_diag_index(self, index):
        col = self.col_index(index)
        row = self.row_index(index)
        if index == 0:
            return [1, 1]
        if index == self.width - 1:
            return [1, self.width - 2]
        if index == self.puzzle_2d.size - self.width:
            return [row - 1, col + 1]
        if index == self.puzzle_2d.size - 1:
            return [row - 1, col - 1]

    def get_wrap_diag_index(self, index):
        col = self.col_index(index)
        row = self.row_index(index)
        if index == 0:
            return [self.height - 1, self.width - 1]
        if index == self.width - 1:
            return [self.height - 1, 0]
        if index == self.puzzle_2d.size - self.width:
            return [0, self.width - 1]
        if index == self.puzzle_2d.size - 1:
            return [0, 0]

    def get_value(self, coordinates):
        if coordinates is not None: return self.puzzle_2d[coordinates[0], coordinates[1]]
        return "-"

    def print_all_possible_moves(self):
        print("printing children of each position")
        for i in range(0, self.puzzle_2d.size):
            print(self.puzzle_2d[i], end=": ")
            print("[", end=" right: ")
            print(self.get_value(self.get_right_index(i)), end=", left: ")
            print(self.get_value(self.get_left_index(i)), end=", up: ")
            print(self.get_value(self.get_up_index(i)), end=", down: ")
            print(self.get_value(self.get_down_index(i)), end=", wrap up: ")
            print(self.get_value(self.get_wrap_up_index(i)), end=", wrap down: ")
            print(self.get_value(self.get_wrap_down_index(i)), end=", wrap left: ")
            print(self.get_value(self.get_wrap_left_index(i)), end=", wrap right: ")
            print(self.get_value(self.get_wrap_right_index(i)), end=", inner diag: ")
            print(self.get_value(self.get_diag_index(i)), end=", wrap diag: ")
            print(self.get_value(self.get_wrap_diag_index(i)), end=", ")
            print("]", end=" ")
            print()

    def index_1d(self, index):
        return (index[0] * self.width) + index[1]

    def check_moves(self, index):
        left = self.get_left_index(index)
        right = self.get_right_index(index)
        up = self.get_up_index(index)
        down = self.get_down_index(index)
        w_up = self.get_wrap_up_index(index)
        w_down = self.get_wrap_down_index(index)
        w_left = self.get_wrap_left_index(index)
        w_right = self.get_wrap_right_index(index)
        inner_diag = self.get_diag_index(index)
        wrap_diag = self.get_wrap_diag_index(index)

        a = np.empty(0).astype("int64")
        a = np.append(a, [999, 999])

        if left: a = np.vstack([a, [self.index_1d(left), reg_cost]])
        if right: a = np.vstack([a, [self.index_1d(right), reg_cost]])
        if up: a = np.vstack([a, [self.index_1d(up), reg_cost]])
        if down: a = np.vstack([a, [self.index_1d(down), reg_cost]])
        if w_up: a = np.vstack([a, [self.index_1d(w_up), wrap_cost]])
        if w_down: a = np.vstack([a, [self.index_1d(w_down), wrap_cost]])
        if w_left: a = np.vstack([a, [self.index_1d(w_left), wrap_cost]])
        if w_right: a = np.vstack([a, [self.index_1d(w_right), wrap_cost]])
        if inner_diag: a = np.vstack([a, [self.index_1d(inner_diag), diag_cost]])
        if wrap_diag: a = np.vstack([a, [self.index_1d(wrap_diag), diag_cost]])

        a = np.delete(a, 0, axis=0)
        return a
