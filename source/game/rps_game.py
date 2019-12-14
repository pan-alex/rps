class InvalidInput_RPS(Exception): pass

# Possible game inputs
OPTIONS = [1, 2, 3]
INPUTS_TO_STRINGS = {1:'R', 2:'P', 3:'S'}    # Not sure if I'll even use these dicts
STRINGS_TO_INPUTS = {string: input for input, string in INPUTS_TO_STRINGS.items()}    # Reverse the dict above


def rps_round(input1, input2):
    '''
    # Evaluates one round of RPS. This is the lowest level function for the game.
    :param input1: This is the player input. String. 1, 2, or 3.
    :param input2: This is the computer (opponent) input. String. 1, 2, or 3.
    :return:
    '''
    global OPTIONS
    if (input1 not in OPTIONS) or (input2 not in OPTIONS):
        raise InvalidInput_RPS('Input must be 1 (Rock), 2 (Paper), or 3 (Scissors).')

    r, p, s = OPTIONS
    win_matrix = {r: {r: 0,  # i.e., if input1 is rock, input2 is rock = tie
                      p: -1,  # input2 is paper = loss
                      s: 1},  # input2 is scissors = win
                  p: {r: 1,
                      p: 0,
                      s: -1},
                  s: {r: -1,
                      p: 1,
                      s: 0}
                  }

    outcome = win_matrix[input1][input2]
    return outcome
