from rps_strategies import *

def rps(strategy='random'):
    global OPTIONS
    input1 = []
    input2 = []
    outcomes = []

    for n in range(0, 10):
        input1.append(input('Select Rock (R), Paper (P), or Scissors (S).'))
        input1[n] = input1[n].upper()
        while input1[n] not in OPTIONS:
            input1[n] = input('Select Rock (R), Paper (P), or Scissors (S).')

        # Strategy for the first round is always random
        if n == 0:
            input2.append(select_strategy('random', input1, input2))
        else:
            input2.append(select_strategy(strategy, input1, input2))

        outcomes.append(rps_base_game(input1[n], input2[n]))
    return outcomes



def rps_base_game(input1, input2):
    '''
    :param input1: This is the player input. String. 'R', 'P', or 'S'.
    :param input2: This is the computer (opponent) input. String. 'R', 'P', or 'S'.
    :return:
    '''
    input1, input2 = input1.upper(), input2.upper()

    if input1 == 'R':
        if input2 == 'R': outcome = 'draw'
        elif input2 == 'P': outcome = 'loss'
        elif input2 == 'S': outcome = 'win'
    elif input1 == 'P':
        if input2 == 'P': outcome = 'draw'
        elif input2 == 'S': outcome = 'loss'
        elif input2 == 'R': outcome = 'win'
    elif input1 == 'S':
        if input2 == 'S': outcome = 'draw'
        elif input2 == 'R': outcome = 'loss'
        elif input2 == 'P': outcome = 'win'

    if outcome == 'draw': message = "It's a draw."
    elif outcome == 'loss': message = "You lose :("
    elif outcome == 'win': message = "You win!"

    print('You: ' + input1 + '. Opponent: ' + input2 + '. ' + message)
    return outcome

