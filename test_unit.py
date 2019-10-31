from typing import Sequence

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
    def test_check_sequence_raisess(self, size: int, sequence: Sequence) -> None:
        s = Sudoku([1 for _ in range(size)])
        with pytest.raises(ValueError):
            s._check_sequence(sequence)
