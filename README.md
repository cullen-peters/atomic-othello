# AOthello - Cullen Peters
This is my othello AI implementation for the Atomic Accelerator Programming Challenge

**Disclaimer**: developed with Python Python 3.11.7

## Instructions

Enter the directory:

    $ cd othello_player

Running the main othello board:

    $ java -jar othello.jar [options]

Make sure you have the requirements:

    $ pip install -r requirements.txt

Running the othello player:

    $ python client.py <port> <hostname>

Unit testing:

    $ python -m unittest

Comparing strategies:

    $ python test_strategies.py <num_games>

## Strategy Comparison
**Strategy.RANDOM**:

$$
{\color{green}█████████}{\color{red}██████████}{\color{yellow}█}
$$

Wins: 234 (**47%**),
Losses: 246 (49%),
Ties: 20 (4%)

**Strategy.GREEDY**:

$$
{\color{green}████████████}{\color{red}███████}{\color{yellow}█}
$$

Wins: 290 (**58%**),
Losses: 188 (38%),
Ties: 22 (4%)

**Strategy.MAX_STABLE**:

$$
{\color{green}██████████████████}{\color{red}██}{\color{yellow}}
$$

Wins: 450 (**90%**),
Losses: 45 (9%),
Ties: 5 (1%)