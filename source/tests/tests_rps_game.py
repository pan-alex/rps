import pytest
from source.game.rps_game import *


def test_rps_round():
    with pytest.raises(InvalidInput_RPS):
        rps_round('e', 'p')
        rps_round('R', '1')
    with pytest.raises(AttributeError):
        rps_round(0, 'S')
    assert rps_round('R', 'P') == -1    # loss
    assert rps_round('S', 'S') == 0    # tie
    assert rps_round('P', 'R') == 1    # win


def test_select_strategy():
    '''
    Since the select_strategy function is called every time a game is played and
        takes in the whole history of inputs, it is the most convenient place to
        check that all inputs are correct and have not gotten messed up somewhere
        along the way.
    '''
    with pytest.raises(InvalidStrategy_RPS):
        select_strategy('RANDOM', ['R'], ['P'], [-1])
        select_strategy('basic markov', ['R'], ['P'], [-1])
    with pytest.raises(AssertionError):
        # Test that inputs and `outcomes` are lists
        select_strategy('random', 'R', ['S'], [-1])
        select_strategy('random', ['R'], 'R', [1])
        select_strategy('random', ['R'], ['S'], 1)
        # Inputs and `outcomes` are always the same length
        select_strategy('basic_markov', ['R', 'R'], ['R'], [1])
        select_strategy('beat_last', ['R'], ['R'], [1, 0])
        select_strategy('beat_last', ['R'], ['R'], [])
        # Inputs should only contain 'R', 'P', 'S'
        select_strategy('random', ['W', 'R'], ['S', 'R'], [0, 0])
        select_strategy('random', ['R', 'R'], ['!', 'R'], [0, 0])
        select_strategy('cycle', ['R', 'R', 'P', 'R'], ['R', 'S', 'S', 'W'], [0, 1, -1, 0])
        select_strategy('beat_last', ['R', 'S', 'P', 'x'], ['R', 'R' 'S', 'P'], [0, -1, -1, 0])


if __name__ == '__main__':
    test_rps_round()
    test_select_strategy()

