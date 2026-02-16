from typing import TYPE_CHECKING, Dict, List
from . import MoveInfo, Piece, LineOfSight, PieceType

from board import Position, GameState, BOARD_HEIGHT, Square
from player import Color

if TYPE_CHECKING:
    from ..player import Player


class Pawn(Piece):
    @property
    def piece_type(self) -> PieceType:
        return PieceType.PAWN

    @property
    def value(self) -> int:
        return 1

    def __init__(self, owner: "Player", current_position: "Position"):
        self._starting_rank = current_position.y
        if owner.color is Color.WHITE:
            self.move_direction = 1
            self.end_rank = BOARD_HEIGHT - 1
        else:
            self.move_direction = -1
            self.end_rank = 0

        super().__init__(owner, current_position)

    def _potential_moves(self, game_state: "GameState") -> Dict[Position, MoveInfo]:
        potential_moves: Dict[Position, MoveInfo] = {}
        """having each one mutate potential_moves may be better for preformance"""
        potential_moves.update(self._get_potential_vertical_moves(game_state))
        potential_moves.update(self._get_potential_en_pessant(game_state))
        potential_moves.update(self._get_potential_captures(game_state))

        return potential_moves

    def _get_potential_vertical_moves(
        self, game_state: "GameState"
    ) -> Dict[Position, MoveInfo]:
        potential_moves: Dict[Position, MoveInfo] = {}

        on_starting_rank = self._starting_rank == self.current_position.y

        one_up = Position(
            x=self.current_position.x, y=self.current_position.y + self.move_direction
        )

        if on_starting_rank:
            two_up = Position(
                x=self.current_position.x,
                y=self.current_position.y + self.move_direction * 2,
            )

            if (
                game_state.board[one_up].piece is None
                and game_state.board[two_up].piece is None
            ):
                # the first move can never be a promotion
                potential_moves[two_up] = MoveInfo(is_double_move=True)

        if game_state.board[one_up].piece is None:
            potential_moves[one_up] = MoveInfo(is_promotion=one_up.y == self.end_rank)
        return potential_moves

    def _get_potential_captures(
        self, game_state: "GameState"
    ) -> Dict[Position, MoveInfo]:
        potential_captures: Dict[Position, MoveInfo] = {}

        potential_capture_positions = [
            Position(
                x=self.current_position.x - 1,
                y=self.current_position.y + self.move_direction,
            ),
            Position(
                x=self.current_position.x + 1,
                y=self.current_position.y + self.move_direction,
            ),
        ]

        for position in potential_capture_positions:
            if position not in game_state.board:
                continue

            piece = game_state.board[position].piece

            if piece is None or piece.owner is self.owner:
                continue  # square does not have an enemy piece to capture so its no longer a valid move

            potential_captures[position] = MoveInfo(
                capture=piece, is_promotion=position.y == self.end_rank
            )

        return potential_captures

    def _get_potential_en_pessant(
        self, game_state: "GameState"
    ) -> Dict[Position, MoveInfo]:
        if (
            not game_state.double_pawn_move
            or game_state.double_pawn_move.position.y != self.current_position.y
            or game_state.double_pawn_move.position.x
            not in [self.current_position.x - 1, self.current_position.x + 1]
        ):
            return {}

        return {
            Position(
                x=game_state.double_pawn_move.position.x,
                y=self.current_position.y + self.move_direction,
            ): MoveInfo(
                capture=game_state.double_pawn_move.piece
            )  # en pessant can never be a promotion
        }

    def get_los(self, game_state: "GameState") -> LineOfSight:
        line_of_sight: LineOfSight = LineOfSight(
            hard_los=set(),
            pieces_in_hard_los=set(),
            hard_sees_king=False,
            full_los=set(),
            pieces_in_full_los=set(),
            full_sees_king=False,
        )

        left: Position = Position(
            x=self.current_position.x - 1,
            y=self.current_position.y + self.move_direction,
        )
        right: Position = Position(
            x=self.current_position.x + 1,
            y=self.current_position.y + self.move_direction,
        )

        squares: List[Square] = []

        if left in game_state.board:
            line_of_sight.hard_los.add(left)
            squares.append(game_state.board[left])

        if right in game_state.board:
            line_of_sight.hard_los.add(right)
            squares.append(game_state.board[right])

        for square in squares:
            piece = square.piece

            if piece is None:
                continue

            if piece.owner is not self.owner and piece.piece_type is PieceType.KING:
                line_of_sight.hard_sees_king = True

            line_of_sight.pieces_in_hard_los.add(piece)

        return line_of_sight
