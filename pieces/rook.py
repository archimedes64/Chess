from typing import List, Tuple
from . import PieceType
from .long_movement_piece import LongMovementPiece


class Rook(LongMovementPiece):
    @property
    def piece_type(self) -> PieceType:
        return PieceType.ROOK

    @property
    def value(self) -> int:
        return 5

    @property
    def directions(self) -> List[Tuple[int, int]]:
        return [(-1, 0), (1, 0), (0, -1), (0, 1)]
