from tkinter import *
from source.game.rps_strategies import *


class rps_gui:

    def __init__(self, master):
        self.frame = Frame(master, bg='black')
        self.frame.grid(row=0, column=0)

        ##### Define global attributes
        # Globals that must be reset when the game resets
        self.p1_throw_history = []
        self.p2_throw_history = []
        self.n_round = 0
        self.input1, self.input2, self.outcomes = [], [], []
        self.wins, self.losses, self.draws = 0, 0, 0

        # Strategy doesn't change until the player chooses a new one
        self.strategies = {'Strategy 1': 'random', 'Strategy 2': 'beat_last', 'Strategy 3': 'cycle',
                      'Strategy 4': 'basic_markov'}
        self.selected_strategy = StringVar(self.frame)
        self.selected_strategy.set('Strategy 2')  # Set default strategy


        ##### Define basic elements of GUI (buttons, canvas)  [Column 0]
        # Canvas for RPS image outputs
        self.game_output_canvas = Canvas(self.frame, height=700, width=400)
        self.game_output_canvas.grid(row=4, column=0, rowspan=10, sticky=N)

        # Button for "Rock"
        self.button_rock = Button(self.frame, text='Rock (1)', width=10, height=3,
                                  command=lambda: self.game_button(1))
        self.button_rock.grid(row=14, column=0, sticky=W)
        master.bind('1', lambda event=None: self.button_rock.invoke())

        # Button for "Paper"
        self.button_paper = Button(self.frame, text='Paper (2)', width=10, height=3,
                                   command=lambda: self.game_button(2))
        self.button_paper.grid(row=14, column=0, sticky=N)
        master.bind('2', lambda event=None: self.button_paper.invoke())

        # Button for "Scissors"
        self.button_scissors = Button(self.frame, text='Scissors (3)', width=10, height=3,
                                      command=lambda: self.game_button(3))
        self.button_scissors.grid(row=14, column=0, sticky=E)
        master.bind('3', lambda event=None: self.button_scissors.invoke())


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

        ##### Buttons for Settings [Column 1]
        Label(self.frame, text='Settings', fg='white', bg='black', width=30).grid(row=1, column=1, sticky=S)

        # Reset game button
        button_reset = Button(self.frame, text='Reset Score', width=12, height=3, command=self.reset_game)
        button_reset.grid(row=4, column=1, sticky=N)

        # Select computer strategy
        Label(self.frame, text="Computer Strategy", fg='white', bg='black').grid(row=5, column=1, sticky=S)
        picklist_strategy = OptionMenu(self.frame, self.selected_strategy, *self.strategies)
        picklist_strategy.grid(row=6, column=1, sticky=N)


    def game_button(self, button):
        '''
        This is the function that gets called when the player clicks on one of the
            "Rock", "Paper", or "Scissors" buttons on the GUI. Calls on `rps()`
            to evaluate the outcome of the round. Then it updates the canvas to
            show what moves were played and who won, it updates the score labels,
            and it increments n_round by +1.

        :param button: Receives an input of 1, 2, or 3 when the Rock, Paper, or
            Scissor button is pressed (or if the corresponding number [1, 2, 3] is pressed).
        '''
        global OPTIONS
        input_as_number = button - 1     # Player inputs are 1, 2, 3 (to keep buttons close together)
        throw = OPTIONS[input_as_number]
        strategy = self.strategies[self.selected_strategy.get()]
        self.rps(throw, strategy)
        self.n_round += 1

        # self.update_text_output()
        # Update the dashboard (move images, insert new image, change scores)
        # Note the move of -70 is based on images of height 70px.
        self.game_output_canvas.move(ALL, 0, -70)
        self.add_rps_image_to_canvas()
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


    def add_rps_image_to_canvas(self):
        '''
        :return: Adds images of rock, paper, of scissors hands to the bottom of the canvas.
            The hand is red for the player that won.
        '''
        # Note the canvas image coordinates are based on a 400x700 canvas, and
        # is designed to fit 10 rounds worth of images in the canvas.
        # Add player 1 image
        image_path1 = self.determine_image_path(player=1)
        pi_throw1 = PhotoImage(master=self.game_output_canvas, file=image_path1)
        self.game_output_canvas.create_image(75, 665, image=pi_throw1)
        self.p1_throw_history.append(pi_throw1)    # Keeps track of image representations on the Canvas
        # Add player 2 image
        image_path2 = self.determine_image_path(player=2)
        pi_throw2 = PhotoImage(master=self.game_output_canvas, file=image_path2)
        self.game_output_canvas.create_image(272, 665, image=pi_throw2)
        self.p2_throw_history.append(pi_throw2)    # Keeps track of image representations on the Canvas


    def determine_image_path(self, player):
        global INPUTS_TO_STRINGS
        assert player == 1 or player == 2
        # Path to images folder
        folder_path = 'data/images/'
        if player == 1:
            # Use player 1 input; 1 represents P1 win
            last_input = self.input1[-1]
            if self.outcomes[-1] == 1: won = '_won'
            else: won = ''
        elif player == 2:
            # Use player 2 input; -1 represents P2 win
            last_input = self.input2[-1]
            if self.outcomes[-1] == -1: won = '_won'
            else: won = ''
        # Example path: 'data/images/rps_R1_won.png'
        input_string = INPUTS_TO_STRINGS[last_input]
        image_path = (folder_path + 'rps_' + input_string + str(player) + won + '.png')
        return image_path


    def update_score_buttons(self):
        self.wins, self.losses, self.draws = self.count_wins_losses_draws(self.outcomes)
        self.label_wins.config(text=self.wins)
        self.label_losses.config(text=self.losses)
        self.label_draws.config(text=self.draws)


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
        # Clear canvas
        self.game_output_canvas.delete('all')
        # Reset globals
        self.p1_throw_history = []
        self.p2_throw_history = []
        self.n_round = 0
        self.input1, self.input2, self.outcomes = [], [], []
        self.wins, self.losses, self.draws = 0, 0, 0
        # Reset score labels
        self.label_wins.config(text=self.wins)
        self.label_losses.config(text=self.losses)
        self.label_draws.config(text=self.draws)


# Initialize UI
root = Tk()
root.geometry('+1000+0')    # Make it appear offset
root.title('Rock, Paper, Scissors!')
window = rps_gui(root)
root.mainloop()
