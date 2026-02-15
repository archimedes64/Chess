from typing import Dict
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.queen import Queen
from pieces import Piece


from board import Position

WHITE_STARTING_POSITIONS: Dict[Position, type[Piece]] = {
    Position(0, 0): Rook,
    Position(1, 0): Knight,
    Position(2, 0): Bishop,
    Position(3, 0): Queen,
    Position(4, 0): Pawn,  # place holder
    Position(5, 0): Bishop,
    Position(6, 0): Knight,
    Position(7, 0): Rook,
    Position(0, 1): Pawn,
    Position(1, 1): Pawn,
    Position(2, 1): Pawn,
    Position(3, 1): Pawn,
    Position(4, 1): Pawn,
    Position(5, 1): Pawn,
    Position(6, 1): Pawn,
    Position(7, 1): Pawn,
}


BLACK_STARTING_POSITIONS: Dict[Position, type[Piece]] = {
    Position(0, 7): Rook,
    Position(1, 7): Knight,
    Position(2, 7): Bishop,
    Position(3, 7): Queen,
    Position(4, 7): Pawn,  # place holder
    Position(5, 7): Bishop,
    Position(6, 7): Knight,
    Position(7, 7): Rook,
    Position(0, 6): Pawn,
    Position(1, 6): Pawn,
    Position(2, 6): Pawn,
    Position(3, 6): Pawn,
    Position(4, 6): Pawn,
    Position(5, 6): Pawn,
    Position(6, 6): Pawn,
    Position(7, 6): Pawn,
}