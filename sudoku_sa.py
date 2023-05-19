import numpy
import random
import time

class Given(Candidate):
    """ The grid containing the given/known values. """

    def __init__(self, values):
        super().__init__()
        self.values = values
        return

    def is_row_duplicate(self, row, value):
        """ Check whether there is a duplicate of a fixed/given value in a row. """
        for column in range(0, numDigits):
            if self.values[row][column] == value:
                return True
        return False

    def is_column_duplicate(self, column, value):
        """ Check whether there is a duplicate of a fixed/given value in a column. """
        for row in range(0, numDigits):
            if self.values[row][column] == value:
                return True
        return False

    def is_block_duplicate(self, row, column, value):
        """ Check whether there is a duplicate of a fixed/given value in a 3 x 3 block. """
        i = 3 * (int(row / 3))
        j = 3 * (int(column / 3))

        if ((self.values[i][j] == value)
                or (self.values[i][j + 1] == value)
                or (self.values[i][j + 2] == value)
                or (self.values[i + 1][j] == value)
                or (self.values[i + 1][j + 1] == value)
                or (self.values[i + 1][j + 2] == value)
                or (self.values[i + 2][j] == value)
                or (self.values[i + 2][j + 1] == value)
                or (self.values[i + 2][j + 2] == value)):
            return True
        else:
            return False




class Sudoku(object):
    """ Solves a given Sudoku puzzle using a genetic algorithm. """

    def __init__(self):
        self.population = Population()
        self.given = None
        return

    def load(self, path):
        # Load a configuration to solve.
        print("Unsolved Sudoku puzzle:")
        with open(path, "r") as f:
            values = numpy.loadtxt(f).reshape((numDigits, numDigits)).astype(int)
            self.given = Given(values)
            print_grid(self.given.values)
        return

    def save(self, path, solution):
        # Save a configuration to a file.
        with open(path, "w") as f:
            numpy.savetxt(f, solution.values.reshape(numDigits * numDigits), fmt='%d')
        return

    def check_solution(self):
        """
        Checks if the matix is a solution.
        The number of unique elements in each row and column is calculated,
        then subtracted from 162, which is the number of  unique elements in each row and column for a solved sudoku.
        Thus, if the calculations return 0, the the sudoku is solved.
        """
        score = 162
        row = []
        col = []
        for i in range(0, 8):
            for j in range(0, 8):
                row[i, j] = population[i, j]
                col[j, i] = population[j, i]
                score -= len(set(row)) + len(set(col))
        return score


    def solve(self):
        """
        Checks if the matix is a solution.
        The number of unique elements in each row and column is calculated,
        then subtracted from 162, which is the number of  unique elements in each row and column for a solved sudoku.
        Thus, if the calculations return 0, the the sudoku is solved.
        """
        start_time = time.time()
        score = 162


        print("No solution found.")
        return None


def print_grid(values):
    print()
    for i in range(0, numDigits):
        if i % 3 == 0 and i != 0:
            print("------+-------+------")
        for j in range(0, numDigits):
            if j % 3 == 0 and j != 0:
                print("| ", end='')
            if j == numDigits - 1 and values[i, j] == 0:
                print(". ")
            elif j == numDigits - 1 and values[i, j] != 0:
                print("%d" % values[i, j])
            elif values[i, j] == 0:
                print(". ", end='')
            else:
                print("%d " % values[i, j], end='')
    print()


if __name__ == "__main__":
    print("Sudoku solver using a genetic algorithm.")
    s = Sudoku()
    # s.load("puzzle_mild.txt")
    s.load("puzzle.txt")
    print("Starting computation.....")
    solution = s.solve()
    # if solution:
    #    s.save("solution.txt", solution)