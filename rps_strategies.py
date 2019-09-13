import random
OPTIONS = ['R', 'P', 'S']

def strategy_random():
    '''
    :return: Randomly selects and returns 'R', 'P', or 'S'.
    '''
    global OPTIONS
    i = random.randint(0, 2)
    return OPTIONS[i]

def strategy_cycle(last_input2):
    global OPTIONS
    if last_input2 == 'R': return 'S'
    elif last_input2 == 'P': return 'R'
    elif last_input2 == 'S': return 'P'

def strategy_beat_last(last_input1):
    global OPTIONS
    if last_input1 == 'R': return 'P'
    elif last_input1 == 'P': return 'S'
    elif last_input1 == 'S': return 'R'

def select_strategy(strategy, input1, input2):
    if strategy == 'random':
        return strategy_random()
    if strategy == 'beat_last':
        # input[-1] is the input for the current round, which would be cheating.
        # Input[-2] is the input for the last round.
        return strategy_beat_last(input1[-2])
    if strategy == 'cycle':
        return strategy_cycle(input2[-2])
