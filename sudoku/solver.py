#!/usr/bin/env python3
"""Sudoku solver using backtracking, MRV and forward checking."""

import argparse
import os
from time import perf_counter


SIZE = 9
DIGITS = set(range(1, 10))
STRATEGIES = ("plain", "mrv", "mrv-fc")


class PuzzleFormatError(ValueError):
    pass


class Metrics:
    def __init__(self):
        self.nodes = 0
        self.assignments = 0
        self.backtracks = 0
        self.forward_checks = 0
        self.peer_checks = 0
        self.runtime_ms = 0.0


def read_puzzle(path):
    # Both the txt and csv examples use one row per line.
    if not os.path.isfile(path):
        raise PuzzleFormatError(f"Input file does not exist: {path}")

    with open(path, "r", encoding="utf-8") as puzzle_file:
        lines = [line.strip() for line in puzzle_file.readlines()]
    lines = [line for line in lines if line]
    if len(lines) != SIZE:
        raise PuzzleFormatError(f"Expected 9 non-empty rows, found {len(lines)}")

    grid = []
    for row_number, line in enumerate(lines, start=1):
        raw_values = line.split(",") if "," in line else line.split()
        if len(raw_values) != SIZE:
            raise PuzzleFormatError(
                f"Row {row_number} must contain 9 values, found {len(raw_values)}"
            )
        try:
            row = [int(value.strip()) for value in raw_values]
        except ValueError:
            raise PuzzleFormatError(f"Row {row_number} contains a non-integer value")
        if any(value < 0 or value > 9 for value in row):
            raise PuzzleFormatError(f"Row {row_number} contains a value outside 0..9")
        grid.append(row)

    validate_givens(grid)
    return grid


def validate_givens(grid):
    # Zero means an empty square, so it is ignored here.
    if len(grid) != SIZE or any(len(row) != SIZE for row in grid):
        raise PuzzleFormatError("Grid must be exactly 9x9")

    def no_duplicates(values):
        givens = [value for value in values if value != 0]
        return len(givens) == len(set(givens))

    for index in range(SIZE):
        if not no_duplicates(grid[index]):
            raise PuzzleFormatError(f"Duplicate given in row {index + 1}")
        column = [grid[row][index] for row in range(SIZE)]
        if not no_duplicates(column):
            raise PuzzleFormatError(f"Duplicate given in column {index + 1}")

    for box_row in range(0, SIZE, 3):
        for box_col in range(0, SIZE, 3):
            box = [
                grid[row][col]
                for row in range(box_row, box_row + 3)
                for col in range(box_col, box_col + 3)
            ]
            if not no_duplicates(box):
                raise PuzzleFormatError(
                    f"Duplicate given in box ({box_row // 3 + 1}, {box_col // 3 + 1})"
                )


class SudokuSolver:
    def __init__(self, grid, strategy="mrv-fc"):
        validate_givens(grid)
        if strategy not in STRATEGIES:
            raise ValueError(f"Unknown strategy {strategy!r}; choose from {STRATEGIES}")
        self.strategy = strategy
        self.grid = [row[:] for row in grid]
        self.metrics = Metrics()
        self.row_used = [set() for _ in range(SIZE)]
        self.col_used = [set() for _ in range(SIZE)]
        self.box_used = [set() for _ in range(SIZE)]
        for row in range(SIZE):
            for col in range(SIZE):
                value = self.grid[row][col]
                if value:
                    self.row_used[row].add(value)
                    self.col_used[col].add(value)
                    self.box_used[self.box_index(row, col)].add(value)

    def box_index(self, row, col):
        return (row // 3) * 3 + col // 3

    def candidates(self, row, col):
        if self.grid[row][col] != 0:
            return set()
        used = self.row_used[row] | self.col_used[col] | self.box_used[self.box_index(row, col)]
        return DIGITS - used

    def select_mrv_cell(self):
        # MRV picks the empty square with the fewest legal values.
        best = None
        for row in range(SIZE):
            for col in range(SIZE):
                if self.grid[row][col] != 0:
                    continue
                values = self.candidates(row, col)
                if not values:
                    return row, col, values
                if best is None or len(values) < len(best[2]):
                    best = row, col, values
                    if len(values) == 1:
                        return best
        return best

    def select_first_cell(self):
        for row in range(SIZE):
            for col in range(SIZE):
                if self.grid[row][col] == 0:
                    return row, col, self.candidates(row, col)
        return None

    def assign(self, row, col, value):
        self.grid[row][col] = value
        self.row_used[row].add(value)
        self.col_used[col].add(value)
        self.box_used[self.box_index(row, col)].add(value)

    def unassign(self, row, col, value):
        self.grid[row][col] = 0
        self.row_used[row].remove(value)
        self.col_used[col].remove(value)
        self.box_used[self.box_index(row, col)].remove(value)

    def forward_check(self, row, col):
        # Stop early if a related empty square has no value left.
        self.metrics.forward_checks += 1
        peers = {(row, c) for c in range(SIZE)} | {(r, col) for r in range(SIZE)}
        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        peers |= {
            (r, c)
            for r in range(box_row, box_row + 3)
            for c in range(box_col, box_col + 3)
        }
        for peer_row, peer_col in peers:
            if self.grid[peer_row][peer_col] == 0:
                self.metrics.peer_checks += 1
                if not self.candidates(peer_row, peer_col):
                    return False
        return True

    def search(self):
        self.metrics.nodes += 1
        selected = self.select_first_cell() if self.strategy == "plain" else self.select_mrv_cell()
        if selected is None:
            return True
        row, col, values = selected
        if not values:
            return False

        for value in sorted(values):
            self.metrics.assignments += 1
            self.assign(row, col, value)
            inference_ok = self.forward_check(row, col) if self.strategy == "mrv-fc" else True
            if inference_ok and self.search():
                return True
            self.unassign(row, col, value)
            self.metrics.backtracks += 1
        return False

    def solve(self):
        start = perf_counter()
        solved = self.search()
        self.metrics.runtime_ms = (perf_counter() - start) * 1000
        return solved


def is_complete_solution(grid):
    if len(grid) != SIZE or any(len(row) != SIZE for row in grid):
        return False
    for row in grid:
        if set(row) != DIGITS:
            return False
    for col in range(SIZE):
        if {grid[row][col] for row in range(SIZE)} != DIGITS:
            return False
    for box_row in range(0, SIZE, 3):
        for box_col in range(0, SIZE, 3):
            box = {
                grid[row][col]
                for row in range(box_row, box_row + 3)
                for col in range(box_col, box_col + 3)
            }
            if box != DIGITS:
                return False
    return True


def format_grid(grid):
    rows = []
    for row_index, row in enumerate(grid):
        if row_index and row_index % 3 == 0:
            rows.append("------+-------+------")
        groups = [" ".join(str(value) for value in row[start : start + 3]) for start in (0, 3, 6)]
        rows.append(" | ".join(groups))
    return "\n".join(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("puzzle", help="Path to a whitespace-separated .txt or comma-separated .csv grid")
    parser.add_argument("--metrics", action="store_true", help="Print search measurements")
    parser.add_argument(
        "--strategy",
        choices=STRATEGIES,
        default="mrv-fc",
        help="plain row-major backtracking, MRV, or MRV with forward checking",
    )
    args = parser.parse_args()

    try:
        original = read_puzzle(args.puzzle)
    except PuzzleFormatError as exc:
        print(f"Invalid puzzle: {exc}")
        return 2

    solver = SudokuSolver(original, strategy=args.strategy)
    if not solver.solve():
        print("No solution exists for this puzzle.")
        if args.metrics:
            print_metrics(solver.metrics)
        return 1

    if not is_complete_solution(solver.grid):
        print("Internal error: the produced grid is not a valid solution.")
        return 3

    for row in range(SIZE):
        for col in range(SIZE):
            if original[row][col] and solver.grid[row][col] != original[row][col]:
                print("Internal error: a given value was changed.")
                return 3

    print(format_grid(solver.grid))
    if args.metrics:
        print_metrics(solver.metrics)
    return 0


def print_metrics(metrics):
    print(
        "Metrics: "
        f"runtime_ms={metrics.runtime_ms:.3f}, "
        f"nodes={metrics.nodes}, "
        f"assignments={metrics.assignments}, "
        f"backtracks={metrics.backtracks}, "
        f"forward_checks={metrics.forward_checks}, "
        f"peer_checks={metrics.peer_checks}"
    )


if __name__ == "__main__":
    raise SystemExit(main())
