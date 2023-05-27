import string
import random
import numpy
import multiprocessing
import matplotlib.pyplot as plt
import annealing_sudoku_solve as sa
import genetic_algo_sudoku_solver as ga

num_digits = 9


def load(path):
    """Load a configuration to solve."""
    print("\nUnsolved Sudoku puzzle:")
    with open(path, "r") as file:
        lines = file.readlines()  # A list containing all the lines (100)

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


def plot_graph(x, y, title, x_label, y_label):
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


def genetic_algo(unsolved):
    sudoku = ga.Sudoku()
    puzzle, x, y = sudoku.solve(unsolved)  # puzzle = solved puzzle, x = generations, y = fitness

    print_grid(puzzle)
    plot_graph(x, y, 'Genetic Algorithm', 'Generations', 'Fitness')


def simulated_annealing(unsolved):
    sudoku = sa.Sudoku()
    puzzle, x, y = sudoku.solve(unsolved)  # x = iterations, y = scores, puzzle = solved puzzle

    print_grid(puzzle)
    plot_graph(x, y, 'Simulated Annealing', 'Iterations', 'Scores')


def main():
    pool = multiprocessing.Pool(processes=2)
    difficulty = 'qwerty'  # level difficulty of the puzzle
    filename = 'puzzles/'

    print('\n --- Sudoku Solver --- \n')

    # User can choose the difficulty level and algorithm
    while difficulty not in string.digits or len(difficulty) > 1:
        difficulty = input("Difficulty a number between 0 - 7 (easy - hard): ")

    filename += difficulty
    unsolved = load(filename)
    print_grid(unsolved)

    # ploting a graph blocks the program (the main thread), so we use multiprocessing
    # each algorithm is executed in a different process
    pool.apply_async(simulated_annealing, (unsolved,))
    pool.apply_async(genetic_algo, (unsolved,))

    # don't close the program
    while True:
        pass


# to run the program automatically
if __name__ == '__main__':
    main()
