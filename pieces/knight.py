from typing import Dict
from . import MoveInfo, Piece, LineOfSight, PieceType

from board import Position, GameState


class Knight(Piece):
    OFFSETS = (
        (-1, -2),
        (-2, -1),
        (-1, 2),
        (-2, 1),
        (1, -2),
        (2, -1),
        (1, 2),
        (2, 1),
    )

    @property
    def piece_type(self) -> PieceType:
        return PieceType.KNIGHT

    @property
    def value(self) -> int:
        return 3

    def _potential_moves(self, game_state: "GameState") -> Dict[Position, MoveInfo]:
        potential_moves: Dict[Position, MoveInfo] = {}
        for x_offset, y_offset in self.OFFSETS:
            position = Position(
                self.current_position.x + x_offset, self.current_position.y + y_offset
            )

            if position not in game_state.board:
                continue

            piece = game_state.board[position].piece

            if piece is None:
                potential_moves[position] = MoveInfo()
                continue

            if piece.owner.color is self.owner.color:
                continue

            potential_moves[position] = MoveInfo(capture=piece)

        return potential_moves

    def get_los(self, game_state: "GameState") -> LineOfSight:
        line_of_sight = LineOfSight(
            hard_los=set(),
            pieces_in_hard_los=set(),
            hard_sees_king=False,
            full_los=set(),
            pieces_in_full_los=set(),
            full_sees_king=False,
        )
        for x_offset, y_offset in self.OFFSETS:
            position: Position = Position(
                self.current_position.x + x_offset, self.current_position.y + y_offset
            )

            if position not in game_state.board:
                continue

            line_of_sight.hard_los.add(position)

            piece = game_state.board[position].piece
            if piece is not None:
                if (
                    piece.owner.color is not self.owner.color
                    and piece.piece_type == PieceType.KING
                ):
                    line_of_sight.hard_sees_king = True
                line_of_sight.pieces_in_hard_los.add(piece)

        return line_of_sight
