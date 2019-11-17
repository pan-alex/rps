from tkinter import *
from source.game.rps_game import *
import time

class rps_gui:

    def __init__(self, master):
        self.frame = Frame(master, bg='black')
        self.frame.grid(row=0, column=0)

        self.n_round = 0
        self.input1, self.input2, self.outcomes = [], [], []
        self.wins, self.losses, self.draws = 0, 0, 0
        self.strategies = {'Strategy 1': 'random', 'Strategy 2': 'beat_last', 'Strategy 3': 'cycle',
                      'Strategy 4': 'basic_markov'}
        self.selected_strategy = StringVar(self.frame)
        self.selected_strategy.set('Strategy 2')  # Set default strategy

        ##### Input buttons
        # Button for "Rock"
        self.button_rock = Button(self.frame, text='Rock (1)', width=10, height=3,
                                  command=lambda: self.game_button(1))
        self.button_rock.grid(row=6, column=0, sticky=W)
        master.bind('1', lambda event=None: self.button_rock.invoke())

        # # Button for "Paper"
        self.button_paper = Button(self.frame, text='Paper (2)', width=10, height=3,
                                   command=lambda: self.game_button(2))
        self.button_paper.grid(row=6, column=0, sticky=N)
        master.bind('2', lambda event=None: self.button_paper.invoke())

        # # Button for "Scissors"
        self.button_scissors = Button(self.frame, text='Scissors (3)', width=10, height=3,
                                      command=lambda: self.game_button(3))
        self.button_scissors.grid(row=6, column=0, sticky=E)
        master.bind('3', lambda event=None: self.button_scissors.invoke())

        # Create an output box
        # Label(self.frame, text='History', fg='white', bg='black').grid(row=3, column=0, sticky=N)
        # self.game_output = Text(self.frame, wrap=CHAR, background='white', width=60)
        # self.game_output.grid(row=4, column=0, sticky=N)


##################### Trying to do something with images

        self.game_output_canvas = Canvas(self.frame, height=700, width=700)
        self.game_output_canvas.grid(row=4, column=0, sticky=N)

        self.button_move = Button(self.frame, text='Move image', command = self.move_image)
        self.button_move.grid(row=4, column=1)
#####################

        # Box to keep track of score
        Label(self.frame, text='Wins', fg='white', bg='black').grid(row=1, column=0, sticky=W)
        self.label_wins = Label(self.frame, text=self.wins, fg='white', bg='black')
        self.label_wins.grid(row=2, column=0, sticky=W)

        Label(self.frame, text='Losses', fg='white', bg='black').grid(row=1, column=0, sticky=N)
        self.label_losses = Label(self.frame, text=self.losses, fg='white', bg='black')
        self.label_losses.grid(row=2, column=0, sticky=N)

        Label(self.frame, text='Ties', fg='white', bg='black').grid(row=1, column=0, sticky=E)
        self.label_draws = Label(self.frame, text=self.draws, fg='white', bg='black')
        self.label_draws.grid(row=2, column=0, sticky=E)


        ##### Buttons for Settings
        # Reset game button
        Label(self.frame, text='Settings', fg='white', bg='black', width=30).grid(row=3, column=1, sticky=N)
        button_reset = Button(self.frame, text='Reset Score', width=12, height=3, command=self.reset_game)
        button_reset.grid(row=4, column=1, sticky=N)

        # Select computer strategy
        Label(self.frame, text="Computer Strategy", fg='white', bg='black').grid(row=5, column=1, sticky=N)
        picklist_strategy = OptionMenu(self.frame, self.selected_strategy, *self.strategies)
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
        input_as_number = button - 1     # Player inputs are 1, 2, 3 (to keep buttons close together)
        throw = OPTIONS[input_as_number]
        strategy = self.strategies[self.selected_strategy.get()]
        self.rps(throw, strategy)
        self.n_round += 1

        # self.update_text_output()
        self.move_image()
        self.update_image_output(input_as_number)
        self.update_score_buttons()


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

##################### Trying to do something with images
    def add_image_to_canvas(self, input_as_number):
        if input_as_number == 0:
            file = 'rps_rock1.png'
        elif input_as_number == 1:
            file = 'rps_paper1.png'
        elif input_as_number == 2:
            file = 'rps_scissors1.png'
        else:
            raise InvalidInput_RPS('Cannot select image; invalid input')
        self.rock_pi = PhotoImage(master=self.game_output_canvas, file=file)
        # paper_pi = PhotoImage(master=game_output_canvas, file='rps_paper1.png')
        # scissors_pi = PhotoImage(master=game_output_canvas, file='rps_scissors1.png')
        self.rock_image = self.game_output_canvas.create_image(100, 600, image=self.rock_pi)
        # paper_image = game_output_canvas.create_image(500, 500, image=paper_pi)
        # scissors_image = game_output_canvas.create_image(500, 500, image=scissors_pi)


    def update_image_output(self, input_as_number):
        self.add_image_to_canvas(input_as_number)


    def move_image(self):
        try:
            self.game_output_canvas.move(0, -100)
            print('moved object')
        except:
            print('no object to move')
            pass

#####################


    def update_text_output(self):
        message = (f'Round {self.n_round}: You: {self.input1[-1]}. '
                   f'Opponent: {self.input2[-1]}. {game_message(self.outcomes[-1])}')
        self.game_output.insert(END, message + '\n')
        self.game_output.see(END)


    def update_score_buttons(self):
        self.wins, self.losses, self.draws = self.count_wins_losses_draws(self.outcomes)
        self.label_wins.config(text=self.wins)
        self.label_losses.config(text=self.losses)
        self.label_draws.config(text=self.draws)


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
root.geometry('880x850+1000+0')
root.title('Rock, Paper, Scissors!')
window = rps_gui(root)
root.mainloop()
