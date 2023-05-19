import string
import random
import numpy
import annealing_sudoku_solve as sa
import genetic_algo_sudoku_solver as ga


num_digits = 9
def load(path):
    """Load a configuration to solve."""
    print("\nUnsolved Sudoku puzzle:")
    with open(path, "r") as file:
        lines = file.readlines()    # A list containing all the lines (100)

        # Choose random line between 0 and 99
        line = lines[random.randint(0, 99)]

        # format the line
        f = format_line(line)

        # create a 9x9 matrix
        values = numpy.fromstring(f, dtype=int, sep=' ').reshape((num_digits, num_digits)).astype(int)

    return values

def format_line(line):
    f = ''
    for c in line:
        if c == '.':
            f += '0 '
        else:
            f += c + ' '
    return f[:-1]


def print_grid(values):
    print()
    for i in range(0, num_digits):
        if i % 3 == 0 and i != 0:
            print("------+-------+------")
        for j in range(0, num_digits):
            if j % 3 == 0 and j != 0:
                print("| ", end='')
            if j == num_digits - 1 and values[i, j] == 0:
                print(". ")
            elif j == num_digits - 1 and values[i, j] != 0:
                print("%d" % values[i, j])
            elif values[i, j] == 0:
                print(". ", end='')
            else:
                print("%d " % values[i, j], end='')
    print()

def main():
    difficulty = 'qwerty'  # level difficulty of the puzzle
    algo = 'qwerty'  # algorithm to use
    filename = 'puzzles/'
    print(' --- Sudoku Solver --- ')

    # User can choose the difficulty level and algorithm
    while difficulty not in string.digits and len(difficulty) > 1:
        difficulty = input("Difficulty a number between 0 - 8 (easy - hard): ")

    while algo not in string.digits[1:3]:
        algo = input("Algorithm (1 - Simulated Annealing or 2 - Genetic Algoithm): ")

    #difficulty = str(int(difficulty) - 1)
    filename += difficulty
    unsolved = load(filename)
    print_grid(unsolved)

    if algo == '1':
        sudoku = sa.Sudoku()
        sudoku.solve(unsolved)
    else:
        sudoku = ga.Sudoku()
        sudoku.solve(unsolved)


if __name__ == '__main__':
    main()
