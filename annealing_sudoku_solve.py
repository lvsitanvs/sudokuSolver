import numpy as np
import copy
import time
from random import sample, randint


class Sudoku(object):
    """ Solves a given Sudoku puzzle using a genetic algorithm. """

    def __init__(self):
        self.puzzle = None
        self.max_iterations = 0
        return

    # Swap in blocks and score rows,columns
    def solve(self, values=None, max_iterations=5000000, T=0.5, cooling_rate=1.0 - 1e-5):
        """
        Solves sudoku using simulated annealing. Ref(https://en.wikipedia.org/wiki/Simulated_annealing)
        Method:
         - It uniquely fills every nxn block in an n^2xn^2 puzzle randomly.
         - It counts the number of unique elements in every row and column, assigning a score of -1 to each unique element.
         - It picks a random nxn square in the puzzle and swaps two entries in it to calculate a "neighboring state".
         - Calculates the score for the neighbor state and accepts/rejects with a certain probability that the new state has a lower score.
         - Cools the temperature by some cooling rate (T= 0.99999T)
         - Repeat from step 2 till minimum score is reached.

         The idea is that over time, as the temperature cools, it becomes less likely to accept a worse state of the
         puzzle so that given enough iterations, the annealer will solve the puzzle.
         Sometimes anneal can get stuck. In this case, a reheating condition is included, so that the temperature is
         increased, and it will accept a less likely state and travel a different random path to get to the solution.

         Input:
          puzzle_input    : The puzzle to solve as n^2 x n^2 list with zeros marking the empty cells
          maxIterations   : (Optional) The number fo iterations to try before giving up (int)
          T               : (Optional) The temperature (double)
          coolingRate     : (Optional) The rate at which to reduce the temperature. The temperature is reduced geometrically. (double)

         Output:
          Returns solved puzzle
        """
        print("Simulated Annealing")
        # x and y for plotting ---------------------------------
        x = []  # Iterations
        y = []  # Scores
        # -------------------------------------------------------
        self.max_iterations = max_iterations

        if values is not None:
            self.puzzle = values

        reheat_rate = T / 0.3

        start_time = time.time()
        puzzle = copy.deepcopy(self.puzzle)
        side = len(puzzle)
        sq_size = int(np.sqrt(side))

        empty_cells = self.initialize(puzzle)

        # Start annealing
        score = self.calc_score()
        best_score = score
        stuck_count = 0

        idx_rem = 10
        decimal = 0
        for i in range(self.max_iterations):
            x.append(i)
            y.append(score)

            # Print iteraction at exponential indexes (i.e., 10, 100, 1000, 10000...)
            if i % idx_rem == 0:
                # To DEBUG, uncoment the line below
                # print("Iteration " + str(i) + ", current score:" + str(score) + "  Best score: " + str(best_score) + "  Temperature:  ", T)
                print('.', end='', flush=True)  # print a dot for each generation, just to see the script is running :)
                decimal += 1

            if decimal > 9:
                idx_rem *= 10
                decimal = 0

            # Adjust temperature
            if score == 0 or T == 0:
                break

            # If stuck then reheat the annealer
            if stuck_count > 5000 or T < 1e-4:
                # To DEBUG, uncoment the line below
                # print("Annealer is stuck at T={} and stuck_count={}, so re-initializing...".format(T, stuck_count))
                T = T * reheat_rate
                puzzle = copy.deepcopy(self.puzzle)
                empty_cells = self.initialize(puzzle)
                stuck_count = 0

            neighbor_puzzle = self.find_neighbor(puzzle, empty_cells)  # Find neighbouring state
            s2 = self.calc_score(neighbor_puzzle)  # Energy of neighbouring state
            delta_s = float(score - s2)  # Energy difference
            probability = np.exp(delta_s / T)  # Acceptance probability

            random_probability = np.random.uniform(low=0, high=1, size=1)

            if probability > random_probability:  # Acceptance condition, accept-reject sampling
                puzzle = copy.deepcopy(neighbor_puzzle)
                score = s2
                if score < best_score:
                    best_score = score
                stuck_count = 0

            stuck_count += 1

            T = cooling_rate * T

        end_time = time.time()
        print("\nNum iteractions:", i + 1, "with a temperature of", T)
        print("Time taken: %f seconds" % (end_time - start_time))

        return puzzle, x, y

    def calc_score(self, puzzle=None):
        """
        Calculate the score for a puzzle.
        Puzzle is scored by number of unique elements in every row and column.
        The sum of all unique row numbers = 9, so 9 rows = 81, same for columns, which gives 162
        If score equals 0, the puzzle is solved
        """
        if puzzle is None:
            puzzle = self.puzzle

        score = 162

        # Count in the columns
        puzzle_transpose = list(zip(*puzzle))
        for i in range(9):
            # Score by unique elements
            score -= len(list(set(puzzle[i])))
            score -= len(list(set(puzzle_transpose[i])))

        return score

    def map_empty_cell(self, empty_cells, dim, sqcount):
        empty_puzzle_cells = []

        for row in range(dim):
            for col in empty_cells[row]:
                r = row + dim * (sqcount // dim)
                c = col + dim * (sqcount % dim)
                empty_puzzle_cells.append((r, c))
        return empty_puzzle_cells

    def initialize(self, puzzle):
        """
        Initialize a puzzle and return the empty indices

        Input:
         puzzle : ndarray (NxN) containing the puzzle

        Output:
         Initializes the puzzle in place.
         Returns a list containing the empty cells in the puzzle.
         The convention in empty_cells is as below
         For the first 2 square blocks of a puzzle shown below:

         5|0|7 || 1|0|0
         6|1|2 || 0|3|4
         0|0|0 || 9|5|8

         empty_cells = [[(0,1),(2,0),(2,1),(2,2)],
                        [(0,4),(0,5),(1,3)]]
        i.e, each row corresponds to empty cells in a square block
        """
        side = len(puzzle)
        sq_size = int(np.sqrt(side))

        i = 0
        j = 0
        empty_cells = []
        square = []
        square_count = 0
        while i < side and j < side:

            square.append(puzzle[i][j:j + sq_size])

            if (i + 1) % sq_size == 0 and (j + sq_size) % sq_size == 0:

                fixed_cells = []
                empty = []

                values = list(range(1, side + 1))
                # Find empty cells and fixed cells in the block
                for row in range(sq_size):
                    empty.append(np.where(np.array(square)[row] == 0)[0].tolist())
                    fixed_cells.append(np.where(np.array(square)[row] != 0)[0].tolist())

                    # Find fixed values in the block
                    for f in fixed_cells[row]:
                        values.remove(square[row][f])

                # Map empty cell to puzzle indices
                index_map = self.map_empty_cell(empty, sq_size, square_count)
                empty_cells.append(index_map)

                # Fill empty cells in the block uniquely
                for cell in index_map:
                    random_val = sample(values, 1)[0]

                    puzzle[cell[0]][cell[1]] = random_val

                    values.remove(random_val)

                square_count += 1
                j += sq_size
                i -= sq_size
                square = []
                if j % side == 0:
                    i += sq_size
                    j = 0

            i += 1

        return empty_cells

    def find_neighbor(self, puzzle, empty_cells):
        """
        Find a neighboring state of the puzzle by swapping two of its entries in a random block.

        Input:
         puzzle      : grid of values
         empty_cells : list of empty cells in the format returned by Initialize()

        Output:
         new_puzzle  : Next nearest neighbor by swapping 2 entries
        """

        side = len(puzzle)
        sq_size = int(np.sqrt(side))
        new_puzzle = copy.deepcopy(puzzle)

        empty_block_size = 0
        while empty_block_size < 2:
            # Pick a random block
            block = randint(0, side - 1)
            empty_block_size = len(empty_cells[block])

        # Randomly find 2 cells in the block to swap
        a, b = sample(range(len(empty_cells[block])), 2)
        cell1, cell2 = empty_cells[block][a], empty_cells[block][b]

        # Swap entries
        new_puzzle[cell1[0]][cell1[1]], new_puzzle[cell2[0]][cell2[1]] = new_puzzle[cell2[0]][cell2[1]], \
            new_puzzle[cell1[0]][cell1[1]]

        return new_puzzle
