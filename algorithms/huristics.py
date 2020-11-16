import numpy as np
from moves import Moves


class Heuristics:

    # naive, manhattan, hamming
    def __init__(self, puzzle, height, width, heuristic=None, ):
        self.heuristic = heuristic
        self.puzzle = puzzle
        self.width = width
        self.moves = Moves(height, width)

    def get_heuristic_weight(self, goal_state):
        if self.heuristic is None:
            return 0

        if self.heuristic == "naive":
            return 1

        if self.heuristic == "manhattan":
            return self.manhattan_distance(goal_state)

        if self.heuristic == "hamming":
            return self.hamming(goal_state)

    def hamming(self, goal_state):
        heuristic = 0
        for i in range(0, self.puzzle.size):
            if self.puzzle[i] != goal_state[i] and self.puzzle[i] != 0:
                heuristic += 1

        print(heuristic)
        return 0

    def manhattan_distance(self, goal_state):
        heuristic = 0
        for i in range(0, self.puzzle.size):

            value = self.puzzle[i]

            destination_index = np.where(np.isclose(goal_state, value))[0][0]

            value_row = self.moves.row_index(i)
            value_col = self.moves.col_index(i)

            dest_row = self.moves.row_index(destination_index)
            dest_col = self.moves.col_index(destination_index)

            distance = abs(value_row - dest_row) + abs(dest_col - value_col)

            if value == 0:
                distance = 0

            print("value:", int(value), ": ", distance, " | i: ", i)
            heuristic += distance

        print(heuristic)
        return heuristic


puzzle = np.loadtxt('../input/samplePuzzles.txt')[0]

h = Heuristics(puzzle, 2, 4, heuristic='hamming')
goalState1 = [1, 2, 3, 4, 5, 6, 7, 0]
goalState2 = [1, 3, 5, 7, 2, 4, 6, 0]

p = np.array(puzzle).reshape(2, 4)
gs = np.array(goalState1).reshape(2, 4)
print(p)
print(gs)

h.get_heuristic_weight(goalState1)
