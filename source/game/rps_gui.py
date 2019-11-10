from tkinter import *
from source.game.rps_game import *


class rps_gui:

    def __init__(self, master):
        frame = Frame(master, bg='black')
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
        self.button_rock = Button(frame, text='Rock (1)', width=10, height=3,
                                  command=lambda: self.game_button(1))
        self.button_rock.grid(row=6, column=0, sticky=W)
        master.bind('1', lambda event=None: self.button_rock.invoke())

        # # Button for "Paper"
        self.button_paper = Button(frame, text='Paper (2)', width=10, height=3,
                                   command=lambda: self.game_button(2))
        self.button_paper.grid(row=6, column=0, sticky=N)
        master.bind('2', lambda event=None: self.button_paper.invoke())

        # # Button for "Scissors"
        self.button_scissors = Button(frame, text='Scissors (3)', width=10, height=3,
                                      command=lambda: self.game_button(3))
        self.button_scissors.grid(row=6, column=0, sticky=E)
        master.bind('3', lambda event=None: self.button_scissors.invoke())

        # Create an output box
        Label(frame, text='History', fg='white', bg='black').grid(row=3, column=0, sticky=N)
        self.game_output = Text(frame, wrap=CHAR, background='white', width=60)
        self.game_output.grid(row=4, column=0, sticky=N)

        # Box to keep track of score
        Label(frame, text='Wins', fg='white', bg='black').grid(row=1, column=0, sticky=W)
        self.label_wins = Label(frame, text=self.wins, fg='white', bg='black')
        self.label_wins.grid(row=2, column=0, sticky=W)

        Label(frame, text='Losses', fg='white', bg='black').grid(row=1, column=0, sticky=N)
        self.label_losses = Label(frame, text=self.losses, fg='white', bg='black')
        self.label_losses.grid(row=2, column=0, sticky=N)

        Label(frame, text='Ties', fg='white', bg='black').grid(row=1, column=0, sticky=E)
        self.label_draws = Label(frame, text=self.draws, fg='white', bg='black')
        self.label_draws.grid(row=2, column=0, sticky=E)


        ##### Buttons for Settings
        # Reset game button
        Label(frame, text='Settings', fg='white', bg='black', width=30).grid(row=3, column=1, sticky=N)
        button_reset = Button(frame, text='Reset Score', width=12, height=3, command=self.reset_game)
        button_reset.grid(row=4, column=1, sticky=N)

        # Select computer strategy
        Label(frame, text="Computer Strategy", fg='white', bg='black').grid(row=5, column=1, sticky=N)
        picklist_strategy = OptionMenu(frame, self.selected_strategy, *self.strategies)
        picklist_strategy.grid(row=6, column=1, sticky=N)


    def game_button(self, button):
        '''
        :param button: Receives an input of 1, 2, or 3 when the Rock, Paper, or
            Scissor button is pressed (or if the corresponding number [1, 2, 3] is pressed).

        :return: Calls on `rps()` to evaluate the outcome of the round. Then it
            returns a message indicating who won in the game_output text widget,
            updates the score labels, and increments n_round by +1.
        '''
        global OPTIONS
        throw = OPTIONS[button - 1]    # Player inputs are 1, 2, 3 (to keep buttons close together)
        strategy = self.strategies[self.selected_strategy.get()]
        self.rps(throw, strategy)
        self.n_round += 1

        message = (f'Round {self.n_round}: You: {self.input1[-1]}. '
                   f'Opponent: {self.input2[-1]}. {game_message(self.outcomes[-1])}')
        self.game_output.insert(END, message + '\n')
        self.game_output.see(END)

        self.wins, self.losses, self.draws = self.count_wins_losses_draws(self.outcomes)
        self.label_wins.config(text=self.wins)
        self.label_losses.config(text=self.losses)
        self.label_draws.config(text=self.draws)


    def rps(self, player_input, strategy):
        '''
        :param player_input: The player's most recent input (i.e., for hte current round).
            The class already stores past inputs and outcomes.

        :param strategy: Strategy selected that the computer should use.

        :return: Calls on `select_strategy()` from rps_strategies.py to evaluate
            the game round. The function returns nothing, but appends the most
            recent player and computer inputs and the outcome to the input/outcome
            lists (stored as class attributes).
        '''
        global OPTIONS
        # Computer chooses strategy before human (not that it matters, but makes it harder
        # to accidently code a cheating computer)
        # Strategy for the first round is always random
        if self.n_round == 0:
            self.input2.append(select_strategy('random', self.input1, self.input2, self.outcomes))
        else:
            self.input2.append(select_strategy(strategy, self.input1, self.input2, self.outcomes))

        # Player input
        self.input1.append(player_input)
        self.outcomes.append(rps_round(self.input1[self.n_round], self.input2[self.n_round]))


    def count_wins_losses_draws(self, outcome):
        '''
        Counts the number of wins, losses, and draws in `outcome`
        '''
        wins = outcome.count(1)
        losses = outcome.count(-1)
        draws = outcome.count(0)
        return wins, losses, draws


    def reset_game(self):
        '''
        Resets all globals (i.e., class attributes that track the game state) to
            0 or empty, except for self.strategy. Resets score labels. Prints a
            message that the game has reset and prints the final score.
        '''
        # Output message:
        reset_message = f'===FINAL SCORE: {self.wins} WINS, {self.losses} LOSSES, AND {self.draws} TIES.===\n'
        self.game_output.insert(END, reset_message)
        self.game_output.see(END)
        # Reset globals
        self.n_round = 0
        self.input1, self.input2, self.outcomes = [], [], []
        self.wins, self.losses, self.draws = 0, 0, 0
        # Reset score labels
        self.label_wins.config(text=self.wins)
        self.label_losses.config(text=self.losses)
        self.label_draws.config(text=self.draws)


# Initialize UI
root = Tk()
root.title('Rock, Paper, Scissors!')
window = rps_gui(root)
root.mainloop()
