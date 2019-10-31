from typing import Iterable, Sequence

import pytest

from sudoku import Sudoku


class TestSudoku:
    @pytest.mark.parametrize(
        ("data", "expected_size"), [([], 0), ([1, 2, 3], 3), ([[0, 1], [2, 3]], 2),]
    )
    def test_init_size(self, data: Sequence, expected_size: int) -> None:
        s = Sudoku([])
        assert s.size == 0

    @pytest.mark.parametrize(
        ("size", "sequence"),
        [
            (1, [1]),
            (2, [1, 2]),
            (2, [2, 1]),
            (3, [1, 2, 3]),
            (3, [1, 3, 2]),
            (3, [3, 2, 1]),
            (4, [1, 2, 3, 4]),
        ],
    )
    def test_check_sequence_succeeds(self, size: int, sequence: Sequence) -> None:
        s = Sudoku([1 for _ in range(size)])
        s._check_sequence(sequence)

    @pytest.mark.parametrize(
        ("size", "sequence"),
        [
            (1, [1, 2]),
            (1, [2]),
            (2, [1, 3]),
            (2, [1, 3, 4]),
            (3, [1, 2, 4]),
            (3, [3, 3, 3]),
        ],
    )
    def test_check_sequence_raises_if_sequence_is_not_valid(
        self, size: int, sequence: Sequence
    ) -> None:
        s = Sudoku([1 for _ in range(size)])
        with pytest.raises(ValueError):
            s._check_sequence(sequence)

    @pytest.mark.parametrize(
        ("size", "sequence"),
        [(3, [1, 2, None]), (3, [1, 2, 3.0]), (3, [1, 2, "three"]),],
    )
    def test_check_sequence_raises_if_sequence_contains_not_ints(
        self, size: int, sequence: Sequence
    ) -> None:
        s = Sudoku([1 for _ in range(size)])
        with pytest.raises(ValueError):
            s._check_sequence(sequence)

    @pytest.mark.parametrize(
        "data", [[[1, 2], [3, 4]], [[1, 2, 3], [4, 5, 6], [7, 8, 9]],]
    )
    def test_iter_rows(self, data: Sequence[Sequence[int]]) -> None:
        s = Sudoku(data)
        rows_iter = s._iter_rows()
        for row, expected_row in zip(rows_iter, data):
            assert row == expected_row

        with pytest.raises(StopIteration):
            next(rows_iter)

    @pytest.mark.parametrize(
        ("data", "expected_columns"),
        [
            ([[1, 2], [3, 4]], [[1, 3], [2, 4]]),
            ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[1, 4, 7], [2, 5, 8], [3, 6, 9]]),
        ],
    )
    def test_iter_columns(
        self, data: Sequence[Sequence[int]], expected_columns: Iterable[Sequence[int]]
    ) -> None:
        s = Sudoku(data)
        columns_iter = s._iter_columns()
        for column, expected_column in zip(columns_iter, expected_columns):
            assert list(column) == expected_column

        with pytest.raises(StopIteration):
            next(columns_iter)

    @pytest.mark.parametrize(
        ("data", "expected_squares"),
        [
            (
                [[1, 1, 2, 2], [1, 1, 2, 2], [3, 3, 4, 4], [3, 3, 4, 4],],
                [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4],],
            ),
            (
                [
                    [1, 1, 1, 2, 2, 2, 3, 3, 3],
                    [1, 1, 1, 2, 2, 2, 3, 3, 3],
                    [1, 1, 1, 2, 2, 2, 3, 3, 3],
                    [4, 4, 4, 5, 5, 5, 6, 6, 6],
                    [4, 4, 4, 5, 5, 5, 6, 6, 6],
                    [4, 4, 4, 5, 5, 5, 6, 6, 6],
                    [7, 7, 7, 8, 8, 8, 9, 9, 9],
                    [7, 7, 7, 8, 8, 8, 9, 9, 9],
                    [7, 7, 7, 8, 8, 8, 9, 9, 9],
                ],
                [
                    [1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [2, 2, 2, 2, 2, 2, 2, 2, 2],
                    [3, 3, 3, 3, 3, 3, 3, 3, 3],
                    [4, 4, 4, 4, 4, 4, 4, 4, 4],
                    [5, 5, 5, 5, 5, 5, 5, 5, 5],
                    [6, 6, 6, 6, 6, 6, 6, 6, 6],
                    [7, 7, 7, 7, 7, 7, 7, 7, 7],
                    [8, 8, 8, 8, 8, 8, 8, 8, 8],
                    [9, 9, 9, 9, 9, 9, 9, 9, 9],
                ],
            ),
        ],
    )
    def test_iter_squares(
        self, data: Sequence[Sequence[int]], expected_squares: Iterable[Sequence[int]]
    ) -> None:
        s = Sudoku(data)
        squares_iter = s._iter_squares()
        for square, expected_column in zip(squares_iter, expected_squares):
            assert list(square) == expected_column

        with pytest.raises(StopIteration):
            next(squares_iter)

    def test_ter_squares_raises(self) -> None:
        s = Sudoku([[1, 2], [3, 4]])
        with pytest.raises(ValueError):
            gen = s._iter_squares()
            next(gen)
