from source.game.rps_strategies import *

def get_player_input_console():
    player_input = input('Select Rock (R), Paper (P), or Scissors (S).')
    player_input = player_input.upper()

    while player_input not in OPTIONS:    # Not R, P, or S
        player_input = input('Select Rock (R), Paper (P), or Scissors (S).')
        player_input = player_input.upper()
    return player_input


def rps(strategy='random', n_rounds=10):
    global OPTIONS
    input1 = []
    input2 = []
    outcomes = []

    for n in range(0, n_rounds):
        # Computer chooses strategy before human (not that it matters, but makes it harder
        # to accidently code a cheating computer)
        # Strategy for the first round is always random
        if n == 0:
            input2.append(select_strategy('random', input1, input2, outcomes))
        else:
            input2.append(select_strategy(strategy, input1, input2, outcomes))

        # Player input
        input1.append(get_player_input_console())
        outcomes.append(rps_round(input1[n], input2[n]))
    return outcomes, input1, input2


def rps_round(input1, input2):
    '''
    # Evaluates one round of RPS. This is the lowest level function for the game.
    :param input1: This is the player input. String. 'R', 'P', or 'S'.
    :param input2: This is the computer (opponent) input. String. 'R', 'P', or 'S'.
    :return:
    '''
    input1, input2 = input1.upper(), input2.upper()

    if input1 == 'R':
        if input2 == 'R': outcome = 0
        elif input2 == 'P': outcome = -1
        elif input2 == 'S': outcome = 1
    elif input1 == 'P':
        if input2 == 'P': outcome = 0
        elif input2 == 'S': outcome = -1
        elif input2 == 'R': outcome = 1
    elif input1 == 'S':
        if input2 == 'S': outcome = 0
        elif input2 == 'R': outcome = -1
        elif input2 == 'P': outcome = 1

    if outcome == 0: message = "It's a draw."
    elif outcome == -1: message = "You lose :("
    elif outcome == 1: message = "You win!"

    print(f'You: {input1}. Opponent: {input2}. {message}')
    return outcome

