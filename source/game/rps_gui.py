from tkinter import *
from source.game.rps_game import *

# define `click`
def click():
    # collect text from textbox
    entered_text = text_entry.get()
    text_entry.delete(0, 'end')
    try:    # Check input is valid
        entered_text = entered_text[0].upper()
        OPTIONS.index(entered_text)
        outcome, input1, input2 = rps_round(input1=entered_text)
        message = f'You: {input1}. Opponent: {input2}. {game_message(outcome)}'
    except:
        message = 'Your input must be "R", "P", or "S".'
    output.insert(END, message + '\n')


window = Tk()
window.title('Test')
window.configure(background='black')

# # Add a photo
# im1 = PhotoImage(file="rock_paper_scissors.gif")
# photo1 = Label(window, image=im1, bg='black')
# photo1.grid(row=0, column=0, sticky=W)


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