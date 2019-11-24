import pytest
from source.game.rps_strategies import *


def test_rps_round():
    with pytest.raises(InvalidInput_RPS):
        rps_round(4, 5)
        rps_round(1, 0)
        rps_round('R', 'P')
    assert rps_round(1, 2) == -1    # loss
    assert rps_round(3, 3) == 0    # tie
    assert rps_round(2, 1) == 1    # win


def test_select_strategy():
    '''
    Since the select_strategy function is called every time a game is played and
        takes in the whole history of inputs, it is the most convenient place to
        check that all inputs are correct and have not gotten messed up somewhere
        along the way.
    '''
    with pytest.raises(InvalidStrategy_RPS):
        select_strategy('RANDOM', [1], [2], [-1])
        select_strategy('basic markov', [1], [2], [-1])
    with pytest.raises(AssertionError):
        # Test that inputs and `outcomes` are lists
        select_strategy('random', 1, [3], [-1])
        select_strategy('random', [1], 1, [1])
        select_strategy('random', [1], [3], 1)
        # Inputs and `outcomes` are always the same length
        select_strategy('basic_markov', [1, 1], [1], [1])
        select_strategy('beat_last', [1], [1], [1, 0])
        select_strategy('beat_last', [1], [1], [])
        # Inputs should only contain 1, 2, 3
        select_strategy('random', [999, 1], [3, 1], [0, 0])
        select_strategy('random', [1, 1], ['R', 1], [0, 0])
        select_strategy('cycle', [1, 1, 2, 1], [1, 3, 3, 'P'], [0, 1, -1, 0])
        select_strategy('beat_last', [1, 3, 2, 0.0], [1, 1, 3, 2], [0, -1, -1, 0])


if __name__ == '__main__':
    test_rps_round()
    test_select_strategy()

