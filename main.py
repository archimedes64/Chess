from board import GameState, Position, Square, BOARD_WIDTH, BOARD_HEIGHT
from player import Player, Color
from typing import Dict
from starting_positions import WHITE_STARTING_POSITIONS, BLACK_STARTING_POSITIONS


def main():
    white: Player = Player(color=Color.WHITE, pieces_gone=[], pieces_left=[])
    black: Player = Player(color=Color.BLACK, pieces_gone=[], pieces_left=[])

    board: Dict[Position, Square] = {}
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            position = Position(x, y)

            board[position] = Square(position=position)
            if position in WHITE_STARTING_POSITIONS:
                board[position].piece = WHITE_STARTING_POSITIONS[position](
                    owner=white, current_position=position
                )

            if position in BLACK_STARTING_POSITIONS:
                board[position].piece = BLACK_STARTING_POSITIONS[position](
                    owner=black, current_position=position
                )
    print(board)

    game_state = GameState(board=board, white=white, black=black)


if __name__ == "__main__":
    main()
