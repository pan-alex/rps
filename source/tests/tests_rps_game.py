import pytest
from source.game.rps_game import *

def rps_round(input1, input2='R'):
    global OPTIONS

    try:
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


def test_rps_round():
    with pytest.raises(InvalidInput_RPS):
        rps_round('e', 'p')
    with pytest.raises(InvalidInput_RPS):
        rps_round('R', '1')
    assert rps_round('R', 'P') == -1    # loss
    assert rps_round('S', 'S') == 0    # tie
    assert rps_round('P', 'R') == 1    # win




