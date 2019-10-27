from tkinter import *
from source.game.rps_game import *
import logging
logging.getLogger().setLevel(logging.DEBUG)

N_ROUND = 0
INPUT1 = []
INPUT2 = []
OUTCOMES = []

def rps(player_input, strategy='random'):
    global OPTIONS
    global N_ROUND
    # Computer chooses strategy before human (not that it matters, but makes it harder
    # to accidently code a cheating computer)
    # Strategy for the first round is always random
    if N_ROUND == 0:
        INPUT2.append(select_strategy('random', INPUT1, INPUT2, OUTCOMES))
    else:
        INPUT2.append(select_strategy(strategy, INPUT1, INPUT2, OUTCOMES))

    # Player input
    INPUT1.append(player_input)
    OUTCOMES.append(rps_round(INPUT1[N_ROUND], INPUT2[N_ROUND]))


# command for button press
def button_press(last_player_input):
    global N_ROUND
    button_to_throw = OPTIONS[last_player_input - 1]
    rps(button_to_throw)
    N_ROUND += 1
    message = f'You: {INPUT1[-1]}. Opponent: {INPUT2[-1]}. {game_message(OUTCOMES[-1])}'
    output.insert(END, message + '\n')


##### UI
window = Tk()
window.title('Rock, Paper, Scissors!')
window.configure(background='black')


##### Input buttons

# Button for "Rock"
button_rock = Button(window, text='Rock (1)', width=10, height=3, command= lambda: button_press(1))
button_rock.grid(row=4, column=0, sticky=W)
window.bind('1', lambda event=None: button_rock.invoke())

# Button for "Paper"
button_paper = Button(window, text='Paper (2)', width=10, height=3, command= lambda: button_press(2))
button_paper.grid(row=4, column=0, sticky=N)
window.bind('2', lambda event=None: button_paper.invoke())

# Button for "Scissors"
button_scissors = Button(window, text='Scissors (3)', width=10, height=3, command= lambda: button_press(3))
button_scissors.grid(row=4, column=0, sticky=E)
window.bind('3', lambda event=None: button_scissors.invoke())


####

# Create an output box
Label(window, text='History', fg='white', bg='black').grid(row=0, column=0, sticky=W)
output = Text(window, wrap=CHAR, background='white', width=40)
output.grid(row=1, column=0, sticky=N)




window.mainloop()