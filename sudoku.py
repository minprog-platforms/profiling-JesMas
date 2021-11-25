from __future__ import annotations
from typing import Iterable


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):
        self._grid: list[str] = []

        for puzzle_row in puzzle:
            row = ""

            for element in puzzle_row:
                row += str(element)

            self._grid.append(row)

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        row = self._grid[y]
        new_row = ""

        for i in range(9):
            if i == x:
                new_row += str(value)
            else:
                new_row += row[i]

        self._grid[y] = new_row

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""
        row = self._grid[y]
        new_row = row[:x] + "0" + row[x + 1:]
        self._grid[y] = new_row

    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""

        # value_at is not needed because the value can be retrieved directly from self._grid[x][y]. This eliminates
        # the need to call a function every time

        # Removed the nested loop because i and j are not used in the value assignment and do essentially nothing

        value = int(self._grid[y][x])

        return value

    def options_at(self, x: int, y: int) -> Iterable[int]:
        """Returns all possible values (options) at x,y."""
        options = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        # made options a set instead of a list, the difference between the sets of every row, column and block now give
        # all the remaining options.

        # Remove all values from the row
        options = options.difference(self.set_row_values(y))

        # Remove all values from the column
        options = options.difference(self.set_column_values(x))

        # Get the index of the block based from x,y
        block_index = (y // 3) * 3 + x // 3

        # Remove all values from the block
        options = options.difference(self.set_block_values(block_index))

        return options

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        next_x, next_y = -1, -1

        for y in range(9):
            for x in range(9):

                if int(self._grid[y][x]) == 0 and next_x == -1 and next_y == -1:
                    next_x, next_y = x, y

        return next_x, next_y

    def set_row_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th row."""
        values = set()

        for j in range(9):
            values.add(int(self._grid[i][j]))

        return values

    def row_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th row."""
        values = []

        for j in range(9):
            values.append(int(self._grid[i][j]))

        return values

    def set_column_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th column."""
        values = set()

        for j in range(9):
            values.add(int(self._grid[j][i]))

        return values

    def column_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th column."""
        values = []

        for j in range(9):
            values.append(int(self._grid[j][i]))

        return values

    def set_block_values(self, i: int) -> Iterable[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """
        values = set()

        x_start = (i % 3) * 3
        y_start = (i // 3) * 3

        for x in range(x_start, x_start + 3):
            for y in range(y_start, y_start + 3):
                values.add(int(self._grid[y][x]))

        return values

    def block_values(self, i: int) -> Iterable[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """
        values = []

        x_start = (i % 3) * 3
        y_start = (i // 3) * 3

        for x in range(x_start, x_start + 3):
            for y in range(y_start, y_start + 3):
                values.append(int(self._grid[y][x]))

        return values

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """
        values = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        result = True

        for i in range(9):
            if values != values.union(self.set_column_values(i)):
                result = False
            if values != values.union(self.set_row_values(i)):
                result = False
            if values != values.union(self.set_block_values(i)):
                result = False

        # changed data structure of column_values, row_values and block_values to sets. The list values was also changed
        # to a set. now a union between the sets is performed to check if the union is equal to the values set. This way is
        # faster than iterating over lists.

        return result

    def __str__(self) -> str:
        representation = ""

        for row in self._grid:
            representation += row + "\n"

        return representation.strip()


def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle: list[str] = []

    with open(filename) as f:
        for line in f:

            # strip newline and remove all commas
            line = line.strip().replace(",", "")

            puzzle.append(line)

    return Sudoku(puzzle)
