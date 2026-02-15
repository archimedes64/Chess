from dataclasses import dataclass
from abc import ABC, abstractmethod

from enum import Enum
from typing import TYPE_CHECKING, Set, Union, Dict


if TYPE_CHECKING:
    from ..player import Player
    from ..board import Position, GameState


class PieceType(Enum):
    PAWN = "pawn"
    BISHOP = "bishop"
    KNIGHT = "knight"
    ROOK = "rook"
    QUEEN = "queen"
    KING = "king"


@dataclass
class MoveInfo:  # any extra information about the move so the game can handle the stupid extra rules
    capture: Union["Piece", None] = None
    is_double_move: bool = False
    is_promotion: bool = False
    is_castling: bool = False


@dataclass
class LineOfSight:
    # positions/pieces seen not blocked by a piece. ex (b repersents a blocker, x is not seen squares, _ is seen squares): ____bxxxx
    # its only squres past the blockers that are not seen. The piece's hard los can see the square that blocked
    hard_los: Set["Position"]
    pieces_in_hard_los: Set["Piece"]
    hard_sees_king: bool  # king would now be in check
    # all positions/pieces seen ignoring blockers. is super set of hard_los meaning all items in hard_los are also in soft_los ex: _____b___b___
    # only long movement pieces(bishop, rook, queen) need to add full los
    full_los: Set["Position"]
    pieces_in_full_los: Set["Piece"]
    full_sees_king: bool  # this could cause a pin if true, and only one piece(that is an enemy) is seen


class Piece(ABC):
    @property
    @abstractmethod
    def piece_type(self) -> PieceType:
        pass

    @property
    @abstractmethod
    def value(self) -> int:
        pass

    def __init__(self, owner: "Player", current_position: "Position"):
        self.owner = owner
        self.pinned = False
        self.current_position = current_position
        self._valid_moves: Union[Set["Position"], None] = None

    def set_pin(self, valid_moves: Set["Position"]):
        self.pinned = True
        self._valid_moves = valid_moves

    def remove_pin(self):
        self.pinned = False
        self._valid_moves = None

    def possible_moves(self, game_state: "GameState") -> Dict["Position", MoveInfo]:
        moves: Dict["Position", MoveInfo] = {}
        potential_moves = self._potential_moves(game_state)
        if self._valid_moves is None:
            return potential_moves

        for move in self._valid_moves:
            if move in potential_moves:
                moves[move] = potential_moves[move]

        return moves

    @abstractmethod
    def _potential_moves(self, game_state: "GameState") -> Dict["Position", MoveInfo]:
        pass

    @abstractmethod
    def get_los(self, game_state: "GameState") -> LineOfSight:
        pass

    def __repr__(self) -> str:
        return self.piece_type.value
