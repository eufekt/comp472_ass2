import numpy as np
from moves import Moves


class Heuristics:

    # naive, manhattan, semi naive
    def __init__(self, puzzle, height, width, heuristic=None,):
        self.heuristic = heuristic
        self.puzzle = puzzle
        self.width = width
        self.moves = Moves(height, width)

    def get_heuristic_weight(self, index):
        if self.heuristic is None:
            return 0

        if self.heuristic == "naive":
            return 1

        if self.heuristic == "manhattan":
            return self.manhattan_distance(index)

    def manhattan_distance(self, goal_state):
        sum = 0
        for i in range(0, self.puzzle.size):

            value = self.puzzle[i]
            v = np.where(np.isclose(goal_state, value))[0][0]

            distance = abs((v+1) - (value))
            if distance > (self.width - 1):
                distance = distance - (self.width - 1)
            if value == 0:
                distance = 0
            if distance > value:
                distance = distance - (distance - value)
            sum += distance
            print(i, ": ", distance, " | value: ", value)

        print(sum)
        return 0


puzzle = np.loadtxt('../input/samplePuzzles.txt')[0]

h = Heuristics(puzzle, 2, 4, heuristic='manhattan')
goalState1 = [1, 2, 3, 4, 5, 6, 7, 0]
goalState2 = [1, 3, 5, 7, 2, 4, 6, 0]
print(puzzle)
print(goalState2)

h.manhattan_distance(goalState2)