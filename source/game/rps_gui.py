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


def click():
    global N_ROUND
    # collect text from textbox
    entered_text = text_entry.get()
    text_entry.delete(0, 'end')
    try:  # Check input is valid
        entered_text = entered_text[0].upper()
        logging.debug("entered_text " + entered_text)
        OPTIONS.index(entered_text)
        logging.debug("blah")
        rps(player_input=entered_text)
        N_ROUND += 1
        message = f'You: {INPUT1[-1]}. Opponent: {INPUT2[-1]}. {game_message(OUTCOMES[-1])}'
    except:
        message = 'Your input must be "R", "P", or "S".'
    output.insert(END, message + '\n')




window = Tk()
window.title('Test')
window.configure(background='black')

# Create a text entry box
text_entry = Entry(window, width = 10, bg='white')
text_entry.grid(row=2, column=0, sticky=N)
button_entry = Button(window, text='Enter', width=0, command=click)
button_entry.grid(row=3, column=0, sticky=N)
#
window.bind('<Return>', lambda event=None: button_entry.invoke())

# Create an output box
Label(window, text='History', fg='white', bg='black').grid(row=0, column=0, sticky=W)
output = Text(window, wrap=CHAR, background='white')
output.grid(row=1, column=0, sticky=N)


window.mainloop()