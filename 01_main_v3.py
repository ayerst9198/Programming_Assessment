from tkinter import *
from functools import partial  # To prevent unwanted windows
import csv
import random


class Rounds:

    def __init__(self):

        # Set up GUI Frame
        self.rounds_frame = Frame(padx=10, pady=10)
        self.rounds_frame.grid()

        self.rounds_heading = Label(self.rounds_frame,
                                    text="Fear or Fail",
                                    font=("Arial", "30", "bold",)
                                    )
        self.rounds_heading.grid(row=0)

        instructions = "Please enter enter the number of rounds you want to play between 1-113 below, then press play"

        self.rounds_instructions = Label(self.rounds_frame,
                                         text=instructions,
                                         wraplength=300, width=60,
                                         justify="left", font="11")
        self.rounds_instructions.grid(row=1, pady=20)

        self.rounds_error = Label(self.rounds_frame, text="",
                                  fg="#9C0000", font="bold")
        self.rounds_error.grid(row=3)

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        self.entry_rounds_frame = Entry(self.start_frame,
                                        width=9, font=("Arial", "19"))
        self.entry_rounds_frame.grid(row=4, column=0, pady=5)

        self.start_button = Button(self.start_frame, width=12, text="Play",
                                   font=("Arial", "12", "bold",), bg="#429E9D",
                                   command=self.check_rounds)
        self.start_button.grid(row=4, column=1, pady=5)

        # Conversion, help and statistics
        self.button_frame = Frame(self.rounds_frame)
        self.button_frame.grid(row=5)

        self.help_button = Button(self.start_frame, width=12, text="Help",
                                  bg="#FFCC99", font=("Arial", "12", "bold"),
                                  command=self.to_help)
        self.help_button.grid(row=5, column=0, padx=10, pady=10)

        self.statistics_button = Button(self.start_frame, width=12, text="Statistics",
                                        bg="#CCE5FF", font=("Arial", "12", "bold"))
        self.statistics_button.grid(row=5, column=1, padx=10, pady=10)

        self.number_rounds = self.entry_rounds_frame.get()

    def check_rounds(self):
        error = "Please enter the number of rounds rounds \n you want to play between 1 - 113"

        try:
            response = self.entry_rounds_frame.get()
            response = int(response)

            if response < 1 or response > 113:
                self.rounds_error.config(text=error, fg="#9C0000")
            else:
                self.rounds_error.config(text="".format(response))
                self.to_play()
                return response

        except ValueError:
            self.rounds_error.config(text=error, fg="#9C0000")

    def to_help(self):
        DisplayHelp(self)

    def to_play(self):
        self.rounds = self.entry_rounds_frame.get()
        Quiz(root, self.rounds)  # Pass root as the parent window
        root.withdraw()


class Quiz:

    def __init__(self, parent, rounds):
        self.play_box = Toplevel(parent)

        # if users press the cross at the top, closes help and
        # releases help button
        self.play_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_play))

        # Variables used to work out statistics when game ends etc
        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(rounds)

        # Initially set rounds played and won to 0
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        # Set up GUI Frame
        self.quiz_frame = Frame(self.play_box, padx=10, pady=10)
        self.quiz_frame.grid()

        self.all_questions = self.get_list()

        self.rounds_heading = Label(self.quiz_frame,
                                    text="Round {} of {}".format(self.rounds_played.get() + 1,
                                                                 self.rounds_wanted.get()),
                                    font=("Arial", "30", "bold",)
                                    )
        self.rounds_heading.grid(row=0)

        count = 0
        self.button_question = self.get_round_colours()
        question = self.button_question[count][0]
        answer = self.button_question[count][1]
        count += 1

        instructions = "{} is the fear of what?".format(question)

        self.rounds_instructions = Label(self.quiz_frame,
                                         text=instructions,
                                         wraplength=300, width=60,
                                         justify="left", font="11")
        self.rounds_instructions.grid(row=1, pady=10)

        self.question_frame = Frame(self.play_box, padx=10, pady=10)
        self.question_frame.grid()

        self.buttons = []

        # Create buttons using a loop
        right = random.randint(1, 4)
        button_names = ["1", "2", "3", "4"]
        for item, button_name in enumerate(button_names):
            if right != (item + 1):
                self.button_phobia = self.get_round_colours()
                text = self.button_phobia[item][1]
                self.button = Button(self.question_frame, width=15, height=2, text=text,
                                     font=("Arial", "12", "bold",), bg="#484770", fg="#FFFFFF", wraplength=150,
                                     command=lambda name=button_name: self.button_press(name))
                self.button.grid(row=item // 2 + 2, column=item % 2, pady=5, padx=10)
                self.buttons.append(self.button)
            else:
                self.button_phobia = self.get_round_colours()
                text = answer
                self.button_correct = Button(self.question_frame, width=15, height=2, text=text,
                                             font=("Arial", "12", "bold",), bg="#484770", fg="#FFFFFF", wraplength=150,
                                             command=lambda name=button_name: self.button_press(name))
                self.button_correct.grid(row=item // 2 + 2, column=item % 2, pady=5, padx=10)
                self.buttons.append(self.button_correct)

        self.quiz_frame = Frame(self.play_box, padx=10, pady=10)
        self.quiz_frame.grid()

        # help and statistics and next buttons
        self.button_frame = Frame(self.play_box, padx=10, pady=10)
        self.button_frame.grid(row=4)

        self.help_button = Button(self.button_frame, width=12, text="Help",
                                  bg="#FFCC99", font=("Arial", "12", "bold"),
                                  command=self.to_help)
        self.help_button.grid(row=4, column=0, padx=10, pady=10)

        self.statistics_button = Button(self.button_frame, width=12, text="Statistics",
                                        bg="#CCE5FF", font=("Arial", "12", "bold"))
        self.statistics_button.grid(row=4, column=1, padx=10, pady=10)

        self.next_button = Button(self.button_frame, width=16, text="Next Round",
                                  bg="#D5E8D4", font=("Arial", "12", "bold"),
                                  command=self.next_round)
        self.next_button.grid(row=4, column=2, padx=10, pady=10)

    def button_press(self, button_name):
        # Disable all buttons
        for button in self.buttons:
            button.config(state=DISABLED)

        # Find the correct answer button and change its color to green
        correct_answer = self.button_question[0][1]
        for button in self.buttons:
            if button.cget("text") == correct_answer:
                button.config(bg="#008000")  # Green color

        # Find the pressed button and change its color to red if incorrect
        for button in self.buttons:
            if button.cget("text") == button_name:
                if button.cget("text") != correct_answer:
                    button.config(bg="#FF0000")  # Red color
                break

    def get_list(self):
        file = open("fear_list_csv.csv", "r")
        var_all_questions = list(csv.reader(file, delimiter=","))
        # removes first entry in list
        var_all_questions.pop(0)
        return var_all_questions

    def get_round_colours(self):
        round_colour_list = []
        color_scores = []

        # get four unique colours
        while len(round_colour_list) < 4:
            # choose item
            chosen_colour = random.choice(self.all_questions)
            index_chosen = self.all_questions.index(chosen_colour)

            # check score is not already in list
            if chosen_colour[1] not in color_scores:
                # add item to rounds list
                round_colour_list.append(chosen_colour)
                color_scores.append(chosen_colour[1])

                # remove item from master list
                self.all_questions.pop(index_chosen)
        return round_colour_list

    def close_play(self):
        # reshow root (i.e., choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

    def to_help(self):
        DisplayHelp(self)

    def next_round(self):
        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()
        if rounds_played < rounds_wanted:
            rounds_played += 1
            self.rounds_played.set(rounds_played)
            self.rounds_heading.config(text="Round {} of {}".format(rounds_played, rounds_wanted))
            self.button_question = self.get_round_colours()
            question = self.button_question[0][0]
            answer = self.button_question[0][1]
            self.rounds_instructions.config(text="{} is the fear of what?".format(question))
            count = 1
            for button in self.buttons:
                if button.cget("text") != answer:
                    button.config(text=self.button_question[count][1])
                    count += 1
                else:
                    button.config(text=answer, command=lambda: self.button_press(button.cget("text")))
        else:
            self.next_button.config(state=DISABLED)


class DisplayHelp:

    def __init__(self, partner):
        # setup dialogue box and background colour
        background = "#ffe6cc"

        self.help_box = Toplevel()

        # disable help button
        partner.help_button.config(state=DISABLED)

        # if users press cross at top, closes help and
        # releases help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300, height=200,
                                bg=background)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame, text="Help", bg=background,
                                        font=("Arial", "23", "bold"))
        self.help_heading_label.grid(row=0)

        help_text = "Fear or Fail is a super spectacular quiz. You will be given " \
                    "4 options to choose from for each question, simply click the " \
                    "answer you want to choose, and you will be told whether you are " \
                    "right or wrong, and which answer the correct one is." \
                    "\n\n" \
                    "In order to start, simply enter the number of rounds you want to play " \
                    "between 1 and 113 rounds in the field below, and press enter or start to begin the quiz." \
                    "\n\n" \
                    "*Please note that Fear or Fail is not responsible for any harm that comes to the " \
                    "participant in the event they do not get a perfect score"

        self.help_text_label = Label(self.help_frame, bg=background,
                                     text=help_text, wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help,
                                                     partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

    # closes help dialogue (used by button and x at top of dialogue)
    def close_help(self, partner):
        # Put help button back to normal...
        partner.help_button.config(state=NORMAL)
        self.help_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    antigravity = 1
    root.title("Fear or Fail")
    Rounds()
    root.mainloop()
