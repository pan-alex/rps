class InvalidInput_RPS(Exception): pass

# Possible game inputs
OPTIONS = [1, 2, 3]
INPUTS_TO_STRINGS = {1:'R', 2:'P', 3:'S'}

def game_message(outcome):
    if outcome == 0: message = "It's a draw."
    elif outcome == -1: message = "You lose :("
    elif outcome == 1: message = "You win!"
    return message


def rps_round(input1, input2, print_message=False):
    '''
    # Evaluates one round of RPS. This is the lowest level function for the game.
    :param input1: This is the player input. String. 1, 2, or 3.
    :param input2: This is the computer (opponent) input. String. 1, 2, or 3.
    :return:
    '''
    global OPTIONS

    if (input1 not in OPTIONS) or (input2 not in OPTIONS):
        raise InvalidInput_RPS('Input must be 1 (Rock), 2 (Paper), or 3 (Scissors).')

    if input1 == 1:
        if input2 == 1: outcome = 0
        elif input2 == 2: outcome = -1
        elif input2 == 3: outcome = 1
    elif input1 == 2:
        if input2 == 2: outcome = 0
        elif input2 == 3: outcome = -1
        elif input2 == 1: outcome = 1
    elif input1 == 3:
        if input2 == 3: outcome = 0
        elif input2 == 1: outcome = -1
        elif input2 == 2: outcome = 1

    if print_message == True: print(game_message(outcome))
    return outcome
