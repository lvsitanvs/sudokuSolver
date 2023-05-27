# Sudoku Solver
This script solves a sudoku puzzle using two different algorithms:
- Genetic Algorithm
- Simulated Annealing Algorithm

Performing a subsquent analisys of the algorithms and comparing the results ploting the 
number of ierations and scores for the *simulated annealing*, and the number of generations and fitness
for the *genetic algoritm*.

![Alt text](img/sudoku.png?raw=true "Screenshot")

## Requirements
- Python 3.6 or higher
- matplotlib
- numpy

## How to run
- install dependencies:
```
pip3 install -r requirements.txt
```
- to run the program:
```
python3 sudoku_solver.py
```

- to kill the program:
press CTRL + C

## Multiprocessing Implementation
The script uses the multiprocessing library to run the algorithms in parallel.
Each algorithm will plot a graph with matplotlib to show the progress of the algorithm.
If not running in parallel, each graph will ocupy the main thread and the user will have to close the graph to continue the program.
The script will run until the solution is found or the user kills the program.

## Simulated Annealing Algorithm
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
- puzzle_input    : The puzzle to solve as n^2 x n^2 list with zeros marking the empty cells
- maxIterations   : (Optional) The number fo iterations to try before giving up (int), default = 5000000
- T               : (Optional) The temperature (double) , default = 0.5
- coolingRate     : (Optional) The rate at which to reduce the temperature. The temperature is reduced geometrically. (double), default = 0.0001

## Genetic Algorithm
- It creates a population of numCandidates and uniquely fills every nxn block in a n^2xn^2 puzzle randomly for each candidate.
- It claculates the fitness for every candidate, counting the number of repeated elements in every row, column and block, without any duplicates; if there are any
  duplicates then the fitness will be lowed.
- Sort the candidates by fitness and keep the top 5% best candidates (Elites).
- For the rest of the candidates, it randomly selects two candidates and creates a new candidate by selecting an element throw a tournment between two candidates.
- After creating to new candidates, it crosses over them. It randomly selects a croosover point and swaps the elements from the two candidates.
- It mutates the new cross overed candidate by randomly selecting two elements in a row and changing it.
- If the fitness of the new candidate is better than the old, it increments the phi by 1, used to calculate the next population mutation rate.
- To calculate the next population mutation rate, it uses the following formula:
```
if num_mutations == 0:
    phi = 0  # Avoid divide by zero.
else:
    phi = phi / num_mutations

if phi > 0.2:
    # sigma is the variance in a normal distribution
    sigma = sigma / 0.998
elif phi < 0.2:
    sigma = sigma * 0.998

# mutation_rate is an absolute (positive) random number from a normal distribution with mean 0 and variance sigma
mutation_rate = abs(numpy.random.normal(loc=0.0, scale=sigma, size=None))
```
this formula is based in on Rechenberg's 1/5 success rule, that will stop too much mutation as the fitness progresses towards unity.
- Append all candidates to the new population and repeat from step 2 till the fitness is 1 (solution found) or the maximum number of generations is reached.
- In case of blocking at a local maximum, the algorithm will restart with a new population of candidates.

The idea is that over time, the algorithm will find the solution by selecting the best candidates and crossing over them, and mutating the new candidates.
Sometimes the algorithm can get stuck at a local maximum, in this case, the algorithm will restart with a new population of candidates.

Input:
- puzzle_input    : The puzzle to solve as n^2 x n^2 list with zeros marking the empty cells
- numGenerations  : (Optional) The number of generations to try before giving up (int), default = 10000
- numCandidates   : (Optional) The number of candidates to generate per generation (int), default = 100
- percentElites   : (Optional) The percentage of candidates to keep for the next generation (double), default = 0.05
- mutationRate    : (Optional) The rate at which to mutate the candidates (double), default = 0.06
