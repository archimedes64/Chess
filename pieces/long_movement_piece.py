from typing import List, Tuple, Dict
from . import Piece, PieceType, MoveInfo, LineOfSight
from board import Position, GameState

from abc import abstractmethod


class LongMovementPiece(Piece):
    @property
    @abstractmethod
    def piece_type(self) -> PieceType:
        pass

    @property
    @abstractmethod
    def value(self) -> int:
        pass

    @property
    @abstractmethod
    def directions(self) -> List[Tuple[int, int]]:
        pass

    def _potential_moves(self, game_state: GameState) -> Dict[Position, MoveInfo]:
        possible_moves: Dict[Position, MoveInfo] = {}
        for x_offset, y_offset in self.directions:
            position: Position = Position(
                self.current_position.x + x_offset, self.current_position.y + y_offset
            )

            while position in game_state.board:
                piece = game_state.board[position].piece
                if piece is None:
                    possible_moves[position] = MoveInfo()
                    position = Position(position.x + x_offset, position.y + y_offset)
                    continue

                if piece.owner.color is not self.owner.color:
                    possible_moves[position] = MoveInfo(capture=piece)

                break  # cannot go through pieces obviously

        return possible_moves

    def get_los(self, game_state: GameState) -> LineOfSight:
        line_of_sight: LineOfSight = LineOfSight(
            hard_los=set(),
            pieces_in_hard_los=set(),
            hard_sees_king=False,
            full_los=set(),
            pieces_in_full_los=set(),
            full_sees_king=False,
        )

        for x_offset, y_offset in self.directions:
            position: Position = Position(
                self.current_position.x + x_offset, self.current_position.y + y_offset
            )
            hard_los_blocked = False

            while position in game_state.board:
                piece = game_state.board[position].piece

                if not hard_los_blocked:
                    line_of_sight.hard_los.add(position)
                line_of_sight.full_los.add(position)

                if piece is None:
                    position = Position(position.x + x_offset, position.y + y_offset)
                    continue

                king_seen = (
                    piece.owner is not self.owner and piece.piece_type is PieceType.KING
                )

                if not hard_los_blocked:
                    line_of_sight.pieces_in_hard_los.add(piece)
                    line_of_sight.hard_sees_king = (
                        king_seen or line_of_sight.hard_sees_king
                    )
                    hard_los_blocked = True

                line_of_sight.pieces_in_full_los.add(piece)
                line_of_sight.full_sees_king = king_seen or line_of_sight.full_sees_king

                position = Position(position.x + x_offset, position.y + y_offset)

        return line_of_sight
