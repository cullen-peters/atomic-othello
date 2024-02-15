import sys
import unittest
from io import StringIO
from unittest.mock import patch

from board import Board, GameResult
from player import Player, Strategy


class TestBoard(unittest.TestCase):
    def test_board_init(self):
        test_board = Board()
        self.assertEqual(test_board.board_state, [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [
                         0, 0, 0, 1, 2, 0, 0, 0], [0, 0, 0, 2, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])
        board = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 1, 0, 0, 0], [
            0, 0, 0, 2, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
        test_board = Board(board)
        self.assertEqual(test_board.board_state, board)

    def test_print_board(self):
        test_board = Board()
        moves = [[2, 4], [3, 5], [4, 2], [5, 3]]
        printed_board = "   a  b  c  d  e  f  g  h  \n0  ▢  ▢  ▢  ▢  ▢  ▢  ▢  ▢  0\n1  ▢  ▢  ▢  ▢  ▢  ▢  ▢  ▢  1\n2  ▢  ▢  ▢  ▢  ◉  ▢  ▢  ▢  2\n3  ▢  ▢  ▢  \033[31m1\033[0m  \033[34m2\033[0m  ◉  ▢  ▢  3\n4  ▢  ▢  ◉  \033[34m2\033[0m  \033[31m1\033[0m  ▢  ▢  ▢  4\n5  ▢  ▢  ▢  ◉  ▢  ▢  ▢  ▢  5\n6  ▢  ▢  ▢  ▢  ▢  ▢  ▢  ▢  6\n7  ▢  ▢  ▢  ▢  ▢  ▢  ▢  ▢  7\n   a  b  c  d  e  f  g  h  \n"
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        test_board.print_board(moves)
        sys.stdout = sys.__stdout__
        self.assertEqual(capturedOutput.getvalue(), printed_board)

    def test_score(self):
        board = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 1, 0, 0, 0], [
            0, 0, 0, 2, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
        test_board = Board(board)
        self.assertEqual(test_board.score(1), 4)
        self.assertEqual(test_board.score(2), 1)

    def test_check_game_over(self):
        test_board = Board()
        self.assertFalse(test_board.check_game_over())
        board = [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [
            1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]]
        test_board = Board(board)
        self.assertTrue(test_board.check_game_over())

    def test_get_game_result(self):
        test_board = Board()
        self.assertEqual(test_board.get_game_result(1), GameResult.TIE)
        board_1 = [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [
            1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]]
        test_board = Board(board_1)
        self.assertEqual(test_board.get_game_result(1), GameResult.WIN)
        self.assertEqual(test_board.get_game_result(2), GameResult.LOSE)
        board_2 = [[2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2], [
            2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2]]
        test_board = Board(board_2)
        self.assertEqual(test_board.get_game_result(1), GameResult.LOSE)
        self.assertEqual(test_board.get_game_result(2), GameResult.WIN)
        board_tie = [[1, 2, 1, 2, 1, 2, 1, 2], [2, 1, 2, 1, 2, 1, 2, 1], [1, 2, 1, 2, 1, 2, 1, 2], [2, 1, 2, 1, 2, 1, 2, 1], [
            1, 2, 1, 2, 1, 2, 1, 2], [2, 1, 2, 1, 2, 1, 2, 1], [1, 2, 1, 2, 1, 2, 1, 2], [2, 1, 2, 1, 2, 1, 2, 1]]
        test_board = Board(board_tie)
        self.assertEqual(test_board.get_game_result(1), GameResult.TIE)
        self.assertEqual(test_board.get_game_result(2), GameResult.TIE)

    def test_is_in_bounds(self):
        test_board = Board()
        self.assertTrue(test_board.is_in_bounds(0, 0))
        self.assertTrue(test_board.is_in_bounds(7, 7))
        self.assertFalse(test_board.is_in_bounds(8, 8))
        self.assertFalse(test_board.is_in_bounds(-1, -1))

    def test_is_valid_direction(self):
        test_board = Board()
        p1 = 1
        p2 = 2
        self.assertTrue(test_board.is_valid_direction(2, 4, (1, 0), p1))
        self.assertTrue(test_board.is_valid_direction(3, 5, (0, -1), p1))
        self.assertTrue(test_board.is_valid_direction(4, 2, (0, 1), p1))
        self.assertTrue(test_board.is_valid_direction(5, 3, (-1, 0), p1))
        self.assertTrue(test_board.is_valid_direction(2, 3, (1, 0), p2))
        self.assertTrue(test_board.is_valid_direction(3, 2, (0, 1), p2))
        self.assertTrue(test_board.is_valid_direction(4, 5, (0, -1), p2))
        self.assertTrue(test_board.is_valid_direction(5, 4, (-1, 0), p2))
        self.assertFalse(test_board.is_valid_direction(2, 4, (1, 0), p2))
        self.assertFalse(test_board.is_valid_direction(3, 5, (0, -1), p2))
        self.assertFalse(test_board.is_valid_direction(4, 2, (0, 1), p2))
        self.assertFalse(test_board.is_valid_direction(5, 3, (-1, 0), p2))
        self.assertFalse(test_board.is_valid_direction(2, 3, (1, 1), p1))
        self.assertFalse(test_board.is_valid_direction(3, 2, (-1, -1), p1))
        self.assertFalse(test_board.is_valid_direction(4, 5, (1, -1), p1))
        self.assertFalse(test_board.is_valid_direction(5, 4, (-1, 1), p1))
        # edge case where the direction goes out of bounds
        board = [[0, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [
            1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]]
        test_board = Board(board)
        self.assertFalse(test_board.is_valid_direction(0, 0, (0, 1), p2))

    def test_is_valid_move(self):
        test_board = Board()
        p1_moves = [[2, 4], [3, 5], [4, 2], [5, 3]]
        p2_moves = [[2, 3], [3, 2], [4, 5], [5, 4]]
        for move in p1_moves:
            self.assertTrue(test_board.is_valid_move(move[0], move[1], 1))
            self.assertFalse(test_board.is_valid_move(move[0], move[1], 2))
        for move in p2_moves:
            self.assertTrue(test_board.is_valid_move(move[0], move[1], 2))
            self.assertFalse(test_board.is_valid_move(move[0], move[1], 1))
        self.assertFalse(test_board.is_valid_move(0, 0, 1))
        self.assertFalse(test_board.is_valid_move(3, 3, 2))

    def test_get_valid_moves(self):
        test_board = Board()
        p1_moves = [[2, 4], [3, 5], [4, 2], [5, 3]]
        p2_moves = [[2, 3], [3, 2], [4, 5], [5, 4]]
        for move in test_board.get_valid_moves(1):
            self.assertIn(move, p1_moves)
        for move in test_board.get_valid_moves(2):
            self.assertIn(move, p2_moves)

    def test_flip_pieces(self):
        test_board = Board()
        test_board.flip_pieces(2, 4, (1, 0), 1)
        self.assertEqual(test_board.board_state, [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [
                         0, 0, 0, 1, 1, 0, 0, 0], [0, 0, 0, 2, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])
        test_board.flip_pieces(2, 3, (1, 0), 2)
        self.assertEqual(test_board.board_state, [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [
                         0, 0, 0, 2, 1, 0, 0, 0], [0, 0, 0, 2, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])

    def test_make_move(self):
        test_board = Board()
        test_board.make_move(2, 4, 1)
        self.assertEqual(test_board.board_state, [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [
                         0, 0, 0, 1, 1, 0, 0, 0], [0, 0, 0, 2, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])
        test_board.make_move(2, 3, 2)
        self.assertEqual(test_board.board_state, [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 1, 0, 0, 0], [
                         0, 0, 0, 2, 1, 0, 0, 0], [0, 0, 0, 2, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])
        test_board.make_move(4, 2, 1)
        self.assertEqual(test_board.board_state, [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 1, 0, 0, 0], [
                         0, 0, 0, 1, 1, 0, 0, 0], [0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])
        self.assertRaises(AssertionError, test_board.make_move, 2, 4, 1)

    def test_is_corner_piece(self):
        test_board = Board()
        self.assertTrue(test_board.is_corner_piece(0, 0))
        self.assertTrue(test_board.is_corner_piece(0, 7))
        self.assertTrue(test_board.is_corner_piece(7, 0))
        self.assertTrue(test_board.is_corner_piece(7, 7))
        self.assertFalse(test_board.is_corner_piece(0, 1))
        self.assertFalse(test_board.is_corner_piece(1, 0))
        self.assertFalse(test_board.is_corner_piece(7, 6))
        self.assertFalse(test_board.is_corner_piece(6, 7))

    def test_count_stable_discs(self):
        test_board = Board()
        self.assertEqual(test_board.count_stable_discs(1), 0)
        self.assertEqual(test_board.count_stable_discs(2), 0)
        board = [[1, 2, 1, 1, 1, 1, 2, 1], [2, 1, 1, 2, 2, 2, 2, 1], [1, 1, 2, 2, 1, 2, 1, 1], [2, 2, 2, 1, 1, 2, 1, 1], [
            2, 1, 1, 1, 2, 2, 1, 2], [2, 1, 2, 2, 2, 1, 1, 1], [2, 2, 2, 2, 1, 2, 2, 1], [1, 1, 1, 1, 2, 2, 2, 2]]
        test_board = Board(board)
        self.assertEqual(test_board.count_stable_discs(1), 9)
        self.assertEqual(test_board.count_stable_discs(2), 4)
        board = [[1, 2, 2, 1, 2, 1, 1, 2], [1, 2, 2, 1, 2, 1, 2, 2], [1, 2, 1, 1, 2, 2, 1, 1], [1, 1, 2, 2, 2, 1, 1, 1], [
            1, 2, 2, 2, 1, 2, 1, 1], [2, 2, 2, 2, 1, 1, 1, 2], [2, 2, 2, 1, 2, 1, 1, 1], [2, 2, 2, 2, 2, 1, 2, 1]]
        test_board = Board(board)
        self.assertEqual(test_board.count_stable_discs(1), 7)
        self.assertEqual(test_board.count_stable_discs(2), 12)


class TestPlayer(unittest.TestCase):
    def test_prepare_response_returns_a_valid_response(self):
        test_player = Player(Strategy.RANDOM)
        self.assertEqual(test_player.prepare_response([2, 3]), b'[2, 3]\n')

    @patch('builtins.input', return_value='-1')
    def test_human_select(self, input):
        test_player = Player(Strategy.HUMAN)
        test_board = Board()
        printed_board = "   a  b  c  d  e  f  g  h  \n0  ▢  ▢  ▢  ▢  ▢  ▢  ▢  ▢  0\n1  ▢  ▢  ▢  ▢  ▢  ▢  ▢  ▢  1\n2  ▢  ▢  ▢  ▢  ◉  ▢  ▢  ▢  2\n3  ▢  ▢  ▢  \033[31m1\033[0m  \033[34m2\033[0m  ◉  ▢  ▢  3\n4  ▢  ▢  ◉  \033[34m2\033[0m  \033[31m1\033[0m  ▢  ▢  ▢  4\n5  ▢  ▢  ▢  ◉  ▢  ▢  ▢  ▢  5\n6  ▢  ▢  ▢  ▢  ▢  ▢  ▢  ▢  6\n7  ▢  ▢  ▢  ▢  ▢  ▢  ▢  ▢  7\n   a  b  c  d  e  f  g  h  \n"
        player_text = "Possible moves:\n\t-1 : End this game\n\t 0 : [2, e]\n\t 1 : [3, f]\n\t 2 : [4, c]\n\t 3 : [5, d]\n"
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        test_player.human_select(test_board.board_state, 1)
        sys.stdout = sys.__stdout__
        self.assertEqual(capturedOutput.getvalue(), printed_board+player_text)

    @patch('builtins.input', return_value='0')
    def test_human_select_returns_a_valid_move(self, input):
        test_player = Player(Strategy.HUMAN)
        test_board = Board()
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        self.assertIn(test_player.human_select(
            test_board.board_state, 1), test_board.get_valid_moves(1))
        sys.stdout = sys.__stdout__

    def test_get_move(self):
        for strategy in Strategy:
            if strategy == Strategy.HUMAN:
                continue
            test_player = Player(strategy)
            test_board = Board()
            self.assertIn(test_player.get_move(
                test_board.board_state, 1), test_board.get_valid_moves(1))
