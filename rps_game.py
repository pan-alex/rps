# def rps(strategy='random'):
#     input1 = input('Select Rock (R), Paper (P), or Scissors (S).')
#     input1 = input1.upper()
#
#     while input1 not in ['R', 'P', 'S']:
#         input1 = input('Select Rock (R), Paper (P), or Scissors (S).')
#
#     if strategy == 'random':
#         input2 = 'R'


def rps_game(input1, input2):
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
    return outcome, input1, input2

