from typing import Iterable, List
import math


class Sudoku:
    def __init__(self, data) -> None:
        self.size = len(data)
        self.data = data

    def _check_sequence(self, sequence: Iterable) -> None:
        if not sorted(sequence) == range(1, self.size + 1):
            raise ValueError("Sequence is not valid")

    def _iter_rows(self) -> Iterable[Iterable[int]]:
        for row in self.data:
            yield row

    def _iter_columns(self) -> Iterable[Iterable[int]]:
        for column in zip(*self.data):
            yield column

    def _iter_squares(self) -> Iterable[Iterable[int]]:
        if not math.sqrt(self.size).is_integer():
            raise ValueError("Sudoku can not be splitted to little squares")

        little_square_size = int(math.sqrt(self.size))

        for i in range(self.size):
            x, y = divmod(i, little_square_size)

            square: List[int] = []

            for row in self.data[x * little_square_size : (x + 1) * little_square_size]:
                square.extend(
                    row[y * little_square_size : (y + 1) * little_square_size]
                )

            yield square

    def is_valid(self) -> bool:
        if not all(
            (
                len(row) == self.size
                and all(type(cell) == int and 0 < cell <= self.size for cell in row)
            )
            for row in self.data
        ):
            return False

        try:
            for row in self._iter_rows():
                self._check_sequence(row)

            for col in self._iter_columns():
                self._check_sequence(col)

            for square in self._iter_squares():
                self._check_sequence(square)
        except ValueError:
            return False

        return True