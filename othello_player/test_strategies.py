#!/usr/bin/env python3

import os
import subprocess
import sys
import time

import numpy as np
from board import Board
from player import Player, Strategy
from tqdm import tqdm


def update_board(line, board, verbose):
    """
    Update the board based on the output from the Othello game.

    Parameters
    ----------
    line (str): The line of output from the Othello game.
    board (Board): The current state of the Othello board.
    verbose (bool): Whether to print the output from the game.

    Returns
    -------
    tuple[int, int]: The scores of the two players if the game is over, otherwise False.
    """
    if line.startswith("INFO  othello.server.text-ui:"):
        if "Player one played" in line:
            row = int(line[-5])
            col = int(line[-3])
            board.make_move(row, col, 1)
        elif "Player two played" in line:
            row = int(line[-5])
            col = int(line[-3])
            board.make_move(row, col, 2)
        elif "Game over..." in line:
            if not board.check_game_over():
                raise ValueError("Game over, but the board is not full.")
            p1_score = board.score(1)
            p2_score = board.score(2)
            if verbose:
                board.print_board()
                print("\033[31mPlayer One\033[0m:", p1_score)
                print("\033[34mPlayer Two\033[0m:", p2_score)
            return (p1_score, p2_score)
    else:
        if verbose:
            print(line, end='')
    return False


def run_othello(othello_jar_path):
    board = Board()
    args = ["java", "-jar", othello_jar_path, "--p1-type",
            "random", "--p2-type", "random", "--min-turn-time", "500"]
    with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
        for line in proc.stdout:
            status = update_board(line.decode('utf-8'), board)
            if status:
                proc.kill()
                return status


def run_othello_remote(othello_jar_path, player, player_number, verbose=False):
    """
    Run an Othello game with a remote player.

    Parameters
    ----------
    othello_jar_path (str): The path to the Othello jar file.
    player (Player): The remote player.
    player_number (int): The number of the remote player (1 or 2).
    verbose (bool): Whether to print the output from the game.

    Returns
    -------
    tuple[int, int]: The scores of the two players.
    """
    assert (player_number in [1, 2])
    board = Board()
    player_port = "4321"
    ui_port = "8888"
    if player_number == 1:
        args = ["java", "-jar", othello_jar_path, "--p1-type", "remote", "--p1-port",
                player_port, "--p2-type", "random", "--min-turn-time", "1", "--ui-port", ui_port]
    else:
        args = ["java", "-jar", othello_jar_path, "--p1-type", "random", "--p2-type",
                "remote", "--p2-port", player_port, "--min-turn-time", "1", "--ui-port", ui_port]
    with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
        for line in proc.stdout:
            line = line.decode('utf-8')
            if "Listening for player" in line and "port "+str(player_port) in line:
                if verbose:
                    print(line, end='')
                time.sleep(0.1)
                player.play_game(int(player_port), "localhost", verbose)
            else:
                status = update_board(line, board, verbose)
                if status:
                    proc.kill()
                    return status


def run_many_othello_remote(othello_jar_path, player, player_numbers, verbose=False):
    """
    Run multiple Othello games with a remote player.

    Parameters
    ----------
    othello_jar_path (str): The path to the Othello jar file.
    player (Player): The remote player.
    player_numbers (list[int]): The numbers of the remote players (1 or 2).
    verbose (bool): Whether to print the output from the game.

    Returns
    -------
    list[tuple[int, int]]: The scores of the two players for each game.
    """
    scores = []
    for player_number in tqdm(player_numbers):
        assert (player_number in [1, 2])
        if player_number == 1:
            if verbose:
                print("\033[31mPlayer One\033[0m is Remote...")
            scores.append(run_othello_remote(
                othello_jar_path, player, player_number, verbose))
        else:
            if verbose:
                print("\033[34mPlayer Two\033[0m is Remote...")
            scores.append(run_othello_remote(othello_jar_path,
                          player, player_number, verbose)[::-1])
    return scores


def process_scores(scores):
    """
    Process the scores from multiple games.

    Parameters
    ----------
    scores (list[tuple[int, int]]): The scores of the two players for each game.

    Returns
    -------
    tuple[int, int, int]: The number of wins, losses, and ties for the first player.
    """
    p1_wins = 0
    p2_wins = 0
    ties = 0
    for score in scores:
        if score[0] > score[1]:
            p1_wins += 1
        elif score[0] < score[1]:
            p2_wins += 1
        else:
            ties += 1
    return (p1_wins, p2_wins, ties)


def display_results(wins, losses, ties):
    """
    Display the results of multiple games with a bar chart.

    Parameters
    ----------
    wins (int): The number of wins for the first player.
    losses (int): The number of losses for the first player.
    ties (int): The number of ties.
    """
    total = wins + losses + ties
    num_stars = os.get_terminal_size().columns
    frac_win = wins / total
    frac_lose = losses / total
    frac_tie = ties / total
    stars_win = round(frac_win * num_stars)
    stars_lose = round(frac_lose * num_stars)
    stars_tie = num_stars - stars_win - stars_lose
    star_char = '█'
    for i in range(stars_win):
        print(f"\033[32m{star_char}\033[0m", end='')
    for i in range(stars_lose):
        print(f"\033[31m{star_char}\033[0m", end='')
    for i in range(stars_tie):
        print(f"\033[33m{star_char}\033[0m", end='')
    print()
    print(f"\033[32mWins\033[0m: {wins} ({frac_win:.0%}), \
          \033[31mLosses\033[0m: {losses} ({frac_lose:.0%}), \
          \033[33mTies\033[0m: {ties} ({frac_tie:.0%})")


if __name__ == "__main__":
    """
    Run multiple Othello games with different strategies.
    Randomly choose player 1 or 2 for each game.    

    Parameters
    ----------
    num_games (int): The number of games to run.
    """
    num_games = 100
    if len(sys.argv) > 1:
        if sys.argv[1].isnumeric() and int(sys.argv[1]) > 0:
            num_games = int(sys.argv[1])
        else:
            print("Usage: python test_strategies.py <num_games>")
            sys.exit(1)
    for strategy in Strategy:
        if strategy == Strategy.HUMAN:
            continue
        print(f"\033[1m{strategy}\033[0m")
        othello_jar_path = "othello.jar"
        remote_player = Player(strategy)
        player_numbers = np.random.choice([1, 2], num_games)
        verbose = False
        wins, losses, ties = process_scores(run_many_othello_remote(
            othello_jar_path, remote_player, player_numbers, verbose))
        display_results(wins, losses, ties)
