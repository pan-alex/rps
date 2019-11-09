from tkinter import *
from source.game.rps_game import *


class rps_gui:

    def __init__(self, master):
        frame = Frame(master)
        frame.grid(row=0, column=0)

        self.n_round = 0
        self.input1, self.input2, self.outcomes = [], [], []
        self.wins, self.losses, self.draws = 0, 0, 0
        self.strategies = {'Strategy 1': 'random', 'Strategy 2': 'beat_last', 'Strategy 3': 'cycle',
                      'Strategy 4': 'basic_markov'}
        self.selected_strategy = StringVar(frame)
        self.selected_strategy.set('Strategy 2')  # Set default strategy

        ##### Input buttons
        # Button for "Rock"
        self.button_rock = Button(frame, text='Rock (1)', width=10, height=3, command=lambda: game_button(1))
        self.button_rock.grid(row=6, column=0, sticky=W)
        # frame.bind('1', lambda event=None: self.button_rock.invoke())

        # # Button for "Paper"
        self.button_paper = Button(frame, text='Paper (2)', width=10, height=3, command=lambda: game_button(2))
        self.button_paper.grid(row=6, column=0, sticky=N)
        # window.bind('2', lambda event=None: button_paper.invoke())

        # # Button for "Scissors"
        self.button_scissors = Button(frame, text='Scissors (3)', width=10, height=3, command=lambda: game_button(3))
        self.button_scissors.grid(row=6, column=0, sticky=E)
        # window.bind('3', lambda event=None: button_scissors.invoke())

        # Create an output box
        Label(frame, text='History', fg='white', bg='black').grid(row=3, column=0, sticky=N)
        self.game_output = Text(frame, wrap=CHAR, background='white', width=60)
        self.game_output.grid(row=4, column=0, sticky=N)


    # command for button press
    def game_button(self, button):
        global N_ROUND, INPUT1, INPUT2, OUTCOMES, WINS, LOSSES, DRAWS, STRATEGIES
        throw = OPTIONS[button - 1]    # Player inputs are 1, 2, 3 (to keep buttons close together)
        strategy = self.strategies[self.selected_strategy.get()]
        rps(throw, strategy)
        self.n_round += 1

        message = f'Round {self.n_round}: You: {self.input1[-1]}. Opponent: {self.input2[-1]}. {game_message(self.outcomes[-1])}'
        self.game_output.insert(END, message + '\n')
        self.game_output.see(END)

        WINS, LOSSES, DRAWS = count_wins_losses_draws(OUTCOMES)
        label_wins.config(text=WINS)
        label_losses.config(text=LOSSES)
        label_draws.config(text=DRAWS)





# Initialize UI
window = Tk()
window.title('Rock, Paper, Scissors!')
window.configure(background='black')


##### Functions
def count_wins_losses_draws(outcome):
    wins = outcome.count(1)
    losses = outcome.count(-1)
    draws = outcome.count(0)
    return wins, losses, draws


def rps(player_input, strategy):
    global OPTIONS
    global N_ROUND, INPUT1, INPUT2, OUTCOMES
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



def reset_game():
    '''
    Resets all globals to 0 or empty, except for STRATEGY
    Resets all buttons. Prints a message that the game has reset and prints the final score.
    '''
    global N_ROUND, INPUT1, INPUT2, OUTCOMES, WINS, LOSSES, DRAWS
    # Output message:
    game_output.insert(END, f'===FINAL SCORE: {WINS} WINS, {LOSSES} LOSSES, AND {DRAWS} TIES.===\n')
    game_output.see(END)
    # Reset globals
    N_ROUND = 0
    INPUT1, INPUT2, OUTCOMES = [], [], []
    WINS, LOSSES, DRAWS = 0, 0, 0
    # Reset buttons
    label_wins.config(text=WINS)
    label_losses.config(text=LOSSES)
    label_draws.config(text=DRAWS)





####


# Box to keep track of score
Label(window, text='Wins', fg='white', bg='black').grid(row=1, column=0, sticky=W)
label_wins = Label(window, text=WINS, fg='white', bg='black')
label_wins.grid(row=2, column=0, sticky=W)

Label(window, text='Losses', fg='white', bg='black').grid(row=1, column=0, sticky=N)
label_losses = Label(window, text=LOSSES, fg='white', bg='black')
label_losses.grid(row=2, column=0, sticky=N)

Label(window, text='Ties', fg='white', bg='black').grid(row=1, column=0, sticky=E)
label_draws = Label(window, text=DRAWS, fg='white', bg='black')
label_draws.grid(row=2, column=0, sticky=E)


##### Buttons for Settings
# Reset game button
Label(window, text='Settings', fg='white', bg='black', width=30).grid(row=3, column=1, sticky=N)
button_reset = Button(window, text='Reset Score', width=12, height=3, command=reset_game)
button_reset.grid(row=4, column=1, sticky=N)

# Select computer strategy
Label(window, text="Computer Strategy", fg='white', bg='black').grid(row=5, column=1, sticky=N)
picklist_strategy = OptionMenu(window, selected_strategy, *STRATEGIES)
picklist_strategy.grid(row=6, column=1, sticky=N)


blah = rps_gui(window)
window.mainloop()
