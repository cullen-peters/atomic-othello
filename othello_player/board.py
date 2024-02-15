from copy import deepcopy
from enum import Enum


class GameResult(Enum):
    """Enum for the different possible results of a game."""
    TIE = 0
    WIN = 1
    LOSE = 2


# Directions for checking valid moves
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0),
              (1, 1), (-1, -1), (1, -1), (-1, 1)]


class Board:
    """
    Class to represent the state of the Othello board and perform operations on it.
    """

    def __init__(self, board_state=None):
        """
        Parameters
        ----------
        board_state (list[list[int]]): The current state of the board.
            0 represents an empty space, 1 represents a piece belonging to player 1,
            and 2 represents a piece belonging to player 2.
        """
        if board_state is not None:
            self.board_state = deepcopy(board_state)
        else:
            self.board_state = [[0 for _ in range(8)] for _ in range(8)]
            self.board_state[3][3] = 1
            self.board_state[3][4] = 2
            self.board_state[4][3] = 2
            self.board_state[4][4] = 1

    def print_board(self, moves=[]):
        """
        Print the current state of the board with optional highlighting of valid moves.

        Parameters
        ----------
        moves (list[list[int]]): A list of valid moves for the current player.
            Each move is represented as a list of two integers, [row, column].
        """
        alphabet = 'abcdefgh'
        print(end='   ')
        for i in range(len(self.board_state)):
            print(alphabet[i], end='  ')
        print()
        for row in range(len(self.board_state)):
            print(row, end=' ')
            for col in range(len(self.board_state[row])):
                if [row, col] in moves:
                    print(' ◉', end=' ')
                elif self.board_state[row][col] == 0:
                    print(' ▢', end=' ')
                elif self.board_state[row][col] == 1:
                    print(' \033[31m1\033[0m', end=' ')
                else:
                    print(' \033[34m2\033[0m', end=' ')
            print(' '+str(row))
        print(end='   ')
        for i in range(len(self.board_state)):
            print(alphabet[i], end='  ')
        print()

    def score(self, player_number):
        """
        Calculate the score of a player.

        Parameters
        ----------
        player_number (int): The number of the player (1 or 2).

        Returns
        -------
        int: The score of the player.
        """
        return sum(row.count(player_number) for row in self.board_state)

    def check_game_over(self):
        """
        Check if the game is over.

        Returns
        -------
        bool: True if the game is over, False otherwise.
        """
        player_1_no_moves = self.get_valid_moves(1) == []
        player_2_no_moves = self.get_valid_moves(2) == []
        return player_1_no_moves and player_2_no_moves

    def get_game_result(self, player_number):
        """
        Get the result of the game for a player.

        Parameters
        ----------
        player_number (int): The number of the player (1 or 2).

        Returns
        -------
        GameResult: The result of the game for the player.
        """
        opponent_number = 1 if player_number == 2 else 2
        player_score = self.score(player_number)
        opponent_score = self.score(opponent_number)
        if player_score > opponent_score:
            return GameResult.WIN
        elif player_score < opponent_score:
            return GameResult.LOSE
        return GameResult.TIE

    def is_in_bounds(self, row, col):
        """
        Check if a position is within the bounds of the board.

        Parameters
        ----------
        row (int): The row index.
        col (int): The column index.

        Returns
        -------
        bool: True if the position is within the bounds of the board, False otherwise.
        """
        return 0 <= row < len(self.board_state) and 0 <= col < len(self.board_state[row])

    def is_valid_direction(self, row, col, direction, player_number):
        """
        Check if a move is valid in a given direction.

        Parameters
        ----------
        row (int): The row index of the move.
        col (int): The column index of the move.
        direction (tuple[int, int]): A tuple representing the direction to check.
            The first element is the change in row, and the second element is the change in column.
        player_number (int): The number of the current player (1 or 2).

        Returns
        -------
        bool: True if the move is valid in the given direction, False otherwise.
        """
        dx, dy = direction
        x, y = row + dx, col + dy
        opponent_number = 1 if player_number == 2 else 2
        if not self.is_in_bounds(x, y) or self.board_state[x][y] != opponent_number:
            return False
        while self.is_in_bounds(x, y):
            if self.board_state[x][y] == player_number:
                return True
            elif self.board_state[x][y] == 0:
                return False
            x += dx
            y += dy
        return False

    def is_valid_move(self, row, col, player_number):
        """
        Check if a move is valid for a player.

        Parameters
        ----------
        row (int): The row index of the move.
        col (int): The column index of the move.
        player_number (int): The number of the current player (1 or 2).

        Returns
        -------
        bool: True if the move is valid, False otherwise.
        """
        # Check if the move is available
        if self.board_state[row][col] != 0:
            return False
        # Check if the move is valid in any direction
        for direction in DIRECTIONS:
            if self.is_valid_direction(row, col, direction, player_number):
                return True
        return False

    def get_valid_moves(self, player_number):
        """
        Get a list of valid moves for a player.

        Parameters
        ----------
        player_number (int): The number of the current player (1 or 2).

        Returns
        -------
        list[list[int]]: A list of valid moves for the player.
            Each move is represented as a list of two integers, [row, column].
        """
        valid_moves = []
        for row in range(len(self.board_state)):
            for col in range(len(self.board_state[row])):
                if self.is_valid_move(row, col, player_number):
                    valid_moves.append([row, col])
        return valid_moves

    def flip_pieces(self, row, col, direction, player_number):
        """
        Flip pieces in a given direction after a move is made.

        Parameters
        ----------
        row (int): The row index of the move.
        col (int): The column index of the move.
        direction (tuple[int, int]): A tuple representing the direction to check.
            The first element is the change in row, and the second element is the change in column.
        player_number (int): The number of the current player (1 or 2).
        """
        dx, dy = direction
        x, y = row + dx, col + dy
        opponent_number = 1 if player_number == 2 else 2
        if not self.is_in_bounds(x, y) or self.board_state[x][y] != opponent_number:
            return
        pieces_to_flip = []
        while self.is_in_bounds(x, y):
            if self.board_state[x][y] == player_number:
                for piece in pieces_to_flip:
                    self.board_state[piece[0]][piece[1]] = player_number
                return
            elif self.board_state[x][y] == 0:
                return
            pieces_to_flip.append([x, y])
            x += dx
            y += dy

    def make_move(self, row, col, player_number):
        """
        Make a move for a player.

        Parameters
        ----------
        row (int): The row index of the move.
        col (int): The column index of the move.
        player_number (int): The number of the current player (1 or 2).
        """
        assert (self.is_valid_move(row, col, player_number))
        self.board_state[row][col] = player_number
        for direction in DIRECTIONS:
            self.flip_pieces(row, col, direction, player_number)

    def is_corner_piece(self, row, col):
        """
        Check if a position is a corner piece.

        Parameters
        ----------
        row (int): The row index.
        col (int): The column index.

        Returns
        -------
        bool: True if the position is a corner piece, False otherwise.
        """
        return (row == 0 or row == 7) and (col == 0 or col == 7)

    def count_stable_discs(self, player_number):
        """
        Count the number of stable discs for a player.

        Parameters
        ----------
        player_number (int): The number of the player (1 or 2).

        Returns
        -------
        int: The number of stable discs for the player.
        """
        # check if corner pieces are not stable for the player
        if self.board_state[0][0] != player_number and \
                self.board_state[0][7] != player_number and \
                self.board_state[7][0] != player_number and \
                self.board_state[7][7] != player_number:
            return 0
        board_stable = [[False for _ in range(8)] for _ in range(8)]
        board_stable_prev = [[True for _ in range(8)] for _ in range(8)]
        while (board_stable != board_stable_prev):
            board_stable_prev = deepcopy(board_stable)
            for row in range(len(self.board_state)):
                for col in range(len(self.board_state[row])):
                    if self.board_state[row][col] == player_number:
                        if self.is_corner_piece(row, col):
                            board_stable[row][col] = True
                        else:
                            # check if the piece can be flipped vertically
                            x1, y1 = row+1, col
                            stable1 = (not self.is_in_bounds(x1, y1)
                                       ) or board_stable[x1][y1] == True
                            x2, y2 = row-1, col
                            stable2 = (not self.is_in_bounds(x2, y2)
                                       ) or board_stable[x2][y2] == True
                            # check if the piece can be flipped horizontally
                            x3, y3 = row, col+1
                            stable3 = (not self.is_in_bounds(x3, y3)
                                       ) or board_stable[x3][y3] == True
                            x4, y4 = row, col-1
                            stable4 = (not self.is_in_bounds(x4, y4)
                                       ) or board_stable[x4][y4] == True
                            # check if the piece can be flipped diagonally (up)
                            x5, y5 = row+1, col+1
                            stable5 = (not self.is_in_bounds(x5, y5)
                                       ) or board_stable[x5][y5] == True
                            x6, y6 = row-1, col-1
                            stable6 = (not self.is_in_bounds(x6, y6)
                                       ) or board_stable[x6][y6] == True
                            # check if the piece can be flipped diagonally (down)
                            x7, y7 = row+1, col-1
                            stable7 = (not self.is_in_bounds(x7, y7)
                                       ) or board_stable[x7][y7] == True
                            x8, y8 = row-1, col+1
                            stable8 = (not self.is_in_bounds(x8, y8)
                                       ) or board_stable[x8][y8] == True
                            board_stable[row][col] = (stable1 or stable2) and (stable3 or stable4) and \
                                (stable5 or stable6) and (stable7 or stable8)
        return sum(_.count(True) for _ in board_stable)
