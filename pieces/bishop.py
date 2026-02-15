from typing import List, Tuple
from . import PieceType
from .long_movement_piece import LongMovementPiece


class Bishop(LongMovementPiece):
    @property
    def piece_type(self) -> PieceType:
        return PieceType.BISHOP

    @property
    def value(self) -> int:
        return 3

    @property
    def directions(self) -> List[Tuple[int, int]]:
        return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
