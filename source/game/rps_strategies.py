import random
import numpy as np
import logging
# logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.CRITICAL)
OPTIONS = ['R', 'P', 'S']    # Possible game inputs.

def strategy_random():
    '''
    :return: Randomly selects and returns 'R', 'P', or 'S'.
    '''
    global OPTIONS
    i = random.randint(0, 2)
    return OPTIONS[i]

def strategy_cycle(input2):
    '''
    :param input2: Computer's input
    :return: Cycles through the options. The strategy plays whatever loses to what it just played.
    '''
    global OPTIONS
    last_input2 = input2[-1]
    if last_input2 == 'R': return 'S'
    elif last_input2 == 'P': return 'R'
    elif last_input2 == 'S': return 'P'


def strategy_beat_last(input1):
    '''
    :param last_input1: Opponent's (player's) inputs. This function only uses the last input.
    :return: This is a non-adaptive strategy that just plays whatever beats the
        opponent's last play.
    '''
    global OPTIONS
    last_input1 = input1[-1]
    if last_input1 == 'R': return 'P'
    elif last_input1 == 'P': return 'S'
    elif last_input1 == 'S': return 'R'


def strategy_basic_markov(input1, outcomes):
    '''
    :param input1: Opponent's (player's) inputs. This function only uses the last input.
    :param outcomes: The outcome of the last game (if the player or computer won).
        This function only utilizes the outcome of the last game.
    :return: This is a non-adaptive strategy, but it makes a decision based
        on the player's last move; the transition probabilities are based on
        the moves that have the highest probability of winning based on historical results
        from 100k games of roshambo.me (see source/data/explore.R)
    Clarifying note: If the function plays R with a probability of 0.321,
        it is because it expects the player to play S with a probability of 0.321
    '''
    global OPTIONS
    last_input1 = input1[-1]
    last_outcome =  outcomes[-1]
    row = OPTIONS.index(last_input1)    # row 0 = R, row 1 = P, row 2 = S
    col =  last_outcome + 1

    transition_probs = np.array(
            #                          Outcome of last round
            #       Lost (-1)      ;          Draw (0)    ;          Won (1)
            [ #  R  ,   P  ,   S                                                      Player 1's last throw
             [[0.321, 0.369, 0.310], [0.340, 0.380, 0.280], [0.356, 0.376, 0.268]],    # Player played R
             [[0.298, 0.349, 0.353], [0.287, 0.367, 0.346], [0.379, 0.362, 0.259]],    # Player played P
             [[0.334, 0.314, 0.352], [0.349, 0.305, 0.346], [0.253, 0.387, 0.360]]     # Player played S
            ])
    probs = list(transition_probs[row, col])
    n = np.random.choice(len(OPTIONS), p=probs)
    logging.debug(probs)
    return OPTIONS[n]


def select_strategy(strategy, input1, input2, outcomes):
    if strategy == 'random':
        return strategy_random()
    if strategy == 'beat_last':
        return strategy_beat_last(input1)
    if strategy == 'cycle':
        return strategy_cycle(input2)
    if strategy == 'basic_markov':
        return strategy_basic_markov(input1, outcomes)
    else:
        print('INVALID STRATEGY')
        return 'R'
