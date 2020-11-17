import numpy as np
from moves import Moves


class Heuristics:

    # naive, manhattan, hamming
    def __init__(self, height, width, heuristic=None):
        self.heuristic = heuristic
        self.width = width
        self.moves = Moves(height, width)

    def get_heuristic_weight(self, current_state_puzzle, goal_state):
        if self.heuristic is None:
            return 0

        if self.heuristic == "naive":
            return 1

        if self.heuristic == "manhattan":
            return self.manhattan_distance(current_state_puzzle, goal_state)

        if self.heuristic == "hamming":
            return self.hamming(current_state_puzzle, goal_state)

    def hamming(self, current_state_puzzle, goal_state):

        current_state_puzzle = np.array(current_state_puzzle)
        current_state_puzzle.astype(int)

        heuristic = 0
        for i in range(0, current_state_puzzle.size):
            if current_state_puzzle[i] != goal_state[i] and current_state_puzzle[i] != 0:
                heuristic += 1

        return heuristic

    # manhattan heuristic that's takes in the current state of the puzzle, the goal state and the possible swap
    # for each tile, it will calculate the distance from it's current position to the destination position
    # needs a array of INTS
    def manhattan_distance(self, state_puzzle, goal_state):

        state_puzzle = np.array(state_puzzle)
        heuristic = 0

        # iterates through the entire current state puzzle
        for i in range(0, state_puzzle.size):

            # gets the value
            value = state_puzzle[i]

            # finds the location of destination index
            destination_index = np.where(goal_state == value)[0][0]

            value_row = self.moves.row_index(i)  # finds which row the value is located
            value_col = self.moves.col_index(i)  # finds which column the value is located

            dest_row = self.moves.row_index(destination_index)  # finds which row the destination is located
            dest_col = self.moves.col_index(destination_index)  # finds which column the destination is located

            # calculates the distance
            distance = abs(value_row - dest_row) + abs(dest_col - value_col)

            # ignores distance if it's the empty tile
            if value == 0:
                distance = 0

            # print("value:", int(value), ": ", distance, " | i: ", i)
            heuristic += distance

        return heuristic

