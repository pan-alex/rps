import random
import numpy as np
OPTIONS = ['R', 'P', 'S']

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
    :param last_input1: Opponent's (player's) last input
    :return: The strategy plays whatever beats the opponent's last play.
    '''
    global OPTIONS
    last_input1 = input1[-1]
    if last_input1 == 'R': return 'P'
    elif last_input1 == 'P': return 'S'
    elif last_input1 == 'S': return 'R'


def strategy_basic_markov(input2):
    print(input2)
    global OPTIONS
    transition_probs = np.array([[0.25, 0.5, 0.25],
                                 [0.25, 0.25, 0.5],
                                 [0.5, 0.25, 0.25]])
    last_input2 = input2[-1]
    i = OPTIONS.index(last_input2)
    n = np.random.choice(len(OPTIONS), p=list(transition_probs[i]))
    return OPTIONS[n]


def select_strategy(strategy, input1, input2):
    if strategy == 'random':
        return strategy_random()
    if strategy == 'beat_last':
        return strategy_beat_last(input1)
    if strategy == 'cycle':
        return strategy_cycle(input2)
    if strategy == 'basic_markov':
        return strategy_basic_markov(input2)
