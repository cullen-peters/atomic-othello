import json
import socket
from enum import Enum

import numpy as np
from board import Board


class Strategy(Enum):
    """Enum for the different strategies that a player can use to select a move."""
    HUMAN = 0
    RANDOM = 1
    GREEDY = 2
    MAX_STABLE = 3


class Player:
    """
    Class to represent a player in the game of Othello. 
    The player can be a human or use a strategy to select a move. 
    The player can play a game against another player (or robot) over a network connection.
    """

    def __init__(self, strategy):
        """
        Parameters
        ----------
        strategy (Strategy): The strategy that the player will use to select a move.
        """
        assert (type(strategy) == Strategy)
        self.strategy = strategy

    def human_select(self, board_state, player_number):
        """
        User selects a move from the list of valid moves for the current player.

        Parameters
        ----------
        board_state (list[list[int]]) : The current state of the board.
        player_number (int): The number of the current player (1 or 2).

        Returns
        -------
        list[int]: The selected move as a list of two integers, [row, column].
        """
        alphabet = 'abcdefgh'
        board = Board(board_state)
        moves = board.get_valid_moves(player_number)
        board.print_board(moves)
        print("Possible moves:")
        print('\t-1', ':', "End this game")
        for i in range(len(moves)):
            print('\t', i, f": [{moves[i][0]}, {alphabet[moves[i][1]]}]")
        ind = -1
        while not ind in list(range(len(moves))):
            try:
                ind = int(input("Select a move from the list: "))
                if ind == -1:
                    # this move is always invalid, and forfeits the game
                    return [3, 3]
            except:
                print(
                    f"\033[31mInvalid Selection\033[0m: enter a number between -1 and {len(moves)-1}")
        return moves[ind]

    def random_select(self, board_state, player_number):
        """
        Randomly select a move from the list of valid moves for the current player.

        Parameters
        ----------
        board_state (list[list[int]]) : The current state of the board.
        player_number (int): The number of the current player (1 or 2).

        Returns
        -------
        list[int]: The selected move as a list of two integers, [row, column].
        """
        board = Board(board_state)
        moves = board.get_valid_moves(player_number)
        assert (self.strategy == Strategy.RANDOM)
        return moves[np.random.choice(list(range(len(moves))))]

    def greedy_select(self, board_state, player_number):
        """
        Select the move that results in the highest score for the current player.

        Parameters
        ----------
        board_state (list[list[int]]) : The current state of the board.
        player_number (int): The number of the current player (1 or 2).

        Returns
        -------
        list[int]: The selected move as a list of two integers, [row, column].
        """
        board = Board(board_state)
        moves = board.get_valid_moves(player_number)
        max_score = -1
        best_moves = []  # list of moves that result in the highest score
        for move in moves:
            possible_board = Board(board_state)
            possible_board.make_move(move[0], move[1], player_number)
            score = possible_board.score(player_number)
            if score > max_score:  # update the best move
                max_score = score
                best_moves = [move]
            elif score == max_score:
                best_moves.append(move)
        # if there are multiple moves with the same score, select one at random
        return best_moves[np.random.choice(list(range(len(best_moves))))]

    def max_stable_select(self, board_state, player_number):
        """
        Select the move that results in the highest number of stable discs for the current player.
        If there are no stable discs, select a move using the greedy strategy.

        Parameters
        ----------
        board_state (list[list[int]]) : The current state of the board.
        player_number (int): The number of the current player (1 or 2).

        Returns
        -------
        list[int]: The selected move as a list of two integers, [row, column].
        """
        board = Board(board_state)
        moves = board.get_valid_moves(player_number)
        max_stable = -1
        stable_moves = []
        for move in moves:
            possible_board = Board(board_state)
            possible_board.make_move(move[0], move[1], player_number)
            stable = possible_board.count_stable_discs(player_number)
            if stable > max_stable:
                max_stable = stable
                stable_moves = [move]
            elif stable == max_stable:
                stable_moves.append(move)
        if max_stable == 0:
            return self.greedy_select(board_state, player_number)
        return stable_moves[np.random.choice(list(range(len(stable_moves))))]

    def get_move(self, board_state, player_number):
        """
        Select a move based on the player's strategy.

        Parameters
        ----------
        board_state (list[list[int]]) : The current state of the board.
        player_number (int): The number of the current player (1 or 2).

        Returns
        -------
        list[int]: The selected move as a list of two integers, [row, column].
        """
        if self.strategy == Strategy.HUMAN:
            move = self.human_select(board_state, player_number)
        elif self.strategy == Strategy.RANDOM:
            move = self.random_select(board_state, player_number)
        elif self.strategy == Strategy.GREEDY:
            move = self.greedy_select(board_state, player_number)
        elif self.strategy == Strategy.MAX_STABLE:
            move = self.max_stable_select(board_state, player_number)
        return move

    def prepare_response(self, move):
        """Prepare a response to send to the game server."""
        response = '{}\n'.format(move).encode()
        if self.strategy == Strategy.HUMAN:
            print('sending {!r}'.format(response))
        return response

    def play_game(self, port, host, verbose=False):  # pragma: no cover (requires integration testing)
        """
        Play a game of Othello over a network connection.

        Parameters
        ----------
        port (int): The port number to connect to.
        host (str): The host to connect to.
        verbose (bool): If True, print additional information about the connection.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if verbose:
                print(f'connecting to {host} port {port}')
            sock.connect((host, port))
            if verbose:
                print('connected!')
            while True:
                data = sock.recv(1024)
                if not data:
                    if verbose:
                        print('closing connection...')
                    break
                json_data = json.loads(str(data.decode('UTF-8')))
                board_state = json_data['board']
                maxTurnTime = json_data['maxTurnTime']
                player_number = json_data['player']

                if self.strategy == Strategy.HUMAN:
                    display_player = "\033[31m1\033[0m" if player_number == 1 else "\033[34m2\033[0m"
                    print("\nPlayer:", display_player,
                          "maxTurnTime:", maxTurnTime/1000, "s")

                move = self.get_move(board_state, player_number)
                response = self.prepare_response(move)
                sock.sendall(response)
        finally:
            sock.close()
            if verbose:
                print("connection closed")
