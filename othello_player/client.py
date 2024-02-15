#!/usr/bin/env python3

import socket
import sys

from player import Player, Strategy

if __name__ == "__main__":
    """
    Run the AI player.

    Parameters
    ----------
    port (int): The port to connect to.
    host (str): The host to connect to.
    """
    if len(sys.argv) != 3 or not sys.argv[1].isnumeric():
        print("Usage: python client.py <port> <host>")
        sys.exit(1)
    port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337
    host = sys.argv[2] if (
        len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname()
    ai_player = Player(Strategy.MAX_STABLE)
    ai_player.play_game(port, host)
