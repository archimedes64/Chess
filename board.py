from dataclasses import dataclass
from typing import Dict, NamedTuple, Union, TYPE_CHECKING, List
from pieces import Piece


if TYPE_CHECKING:
    from player import Player

BOARD_WIDTH = 8
BOARD_HEIGHT = 8


class Position(NamedTuple):
    x: int
    y: int


class Square:
    def __init__(self, position: Position, piece: Union["Piece", None] = None):
        self.position = position
        self.piece: Union[Piece, None] = piece

    def __repr__(self) -> str:
        return f"Piece: {self.piece}"


@dataclass
class GameState:
    board: Dict[Position, Square]
    white: "Player"
    black: "Player"
    double_pawn_move: Union[Square, None] = None
    check: Union[None, List[Piece]] = None
