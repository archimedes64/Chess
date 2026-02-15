from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from pieces import Piece


class Color(Enum):
    WHITE = "white"
    BLACK = "black"


@dataclass
class Player:
    color: Color
    pieces_gone: List["Piece"]
    pieces_left: List["Piece"]
    score: int = 0
    in_check: bool = False
