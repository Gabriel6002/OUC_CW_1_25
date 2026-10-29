# Sudoku solver

## Requirements

- Python 3.10 or later
- No external libraries

## Run

From the submission root:

```bash
python3 sudoku/solver.py <puzzle-file>
```

Or, after changing into the `sudoku` directory:

```bash
python3 solver.py <puzzle-file>
```

The puzzle file may be either a space-separated `.txt` file or a comma-separated `.csv` file. It must contain nine rows of nine integers. Digits 1--9 are givens and 0 represents an empty cell.

The default method is backtracking with Minimum Remaining Values and forward checking. The solved grid is printed to the terminal. If the puzzle is valid but unsatisfiable, the program prints `No solution exists for this puzzle.`

Optional strategy and measurement arguments are:

```bash
python3 sudoku/solver.py <puzzle-file> --strategy plain --metrics
python3 sudoku/solver.py <puzzle-file> --strategy mrv --metrics
python3 sudoku/solver.py <puzzle-file> --strategy mrv-fc --metrics
```
