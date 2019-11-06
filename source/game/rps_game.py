from source.game.rps_strategies import *

class InvalidInput_RPS(Exception):
    pass

def game_message(outcome):
    if outcome == 0: message = "It's a draw."
    elif outcome == -1: message = "You lose :("
    elif outcome == 1: message = "You win!"
    return message


def rps_round(input1, input2='R'):
    '''
    # Evaluates one round of RPS. This is the lowest level function for the game.
    :param input1: This is the player input. String. 'R', 'P', or 'S'.
    :param input2: This is the computer (opponent) input. String. 'R', 'P', or 'S'.
    :return:
    '''
    global OPTIONS
    input1, input2 = input1.upper(), input2.upper()

    if (input1 not in OPTIONS) or (input2 not in OPTIONS):
        raise InvalidInput_RPS('Input must be "R", "P", or "S".')

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

    # print(game_message(outcome))
    return outcome
