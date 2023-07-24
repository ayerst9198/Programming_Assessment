from tkinter import *
from tkinter.constants import DISABLED
from functools import partial  # To prevent unwanted windows
import csv
import random
import statistics


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
                                        bg="#CCE5FF", font=("Arial", "12", "bold"),
                                        command=self.to_statistics)
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

    def to_statistics(self):
        DisplayStats(self)


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

        # Initially set rounds played, won, and incorrect answers to 0
        self.rounds_played = IntVar()
        self.rounds_played.set(0)
        self.rounds_won = 0
        self.incorrect_answers = 0
        self.correct_answers = 0
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
        for item in range(len(button_names)):
            if right != (item + 1):
                self.button_phobia = self.get_round_colours()
                text = self.button_phobia[item][1]
                button = Button(self.question_frame, width=15, height=2, text=text,
                                font=("Arial", "12", "bold",), bg="#484770", fg="#FFFFFF", wraplength=150)
                button.config(command=lambda b=button: self.check_answer(b, text))  # Modified command
                button.grid(row=item // 2 + 2, column=item % 2, pady=5, padx=10)
                self.buttons.append(button)
            else:
                self.button_phobia = self.get_round_colours()
                text = answer
                button = Button(self.question_frame, width=15, height=2, text=text,
                                font=("Arial", "12", "bold",), bg="#484770", fg="#FFFFFF", wraplength=150)
                button.config(command=lambda b=button: self.check_answer(b, text))  # Modified command
                button.grid(row=item // 2 + 2, column=item % 2, pady=5, padx=10)
                self.buttons.append(button)

        self.score_frame = Frame(self.play_box, padx=10, pady=10)
        self.score_frame.grid(row=3)

        self.correct_label = Label(self.score_frame, text="Correct: 0", font=("Arial", "12", "bold"))
        self.correct_label.grid(row=0, column=0, padx=5)

        self.incorrect_label = Label(self.score_frame, text="Incorrect: 0", font=("Arial", "12", "bold"))
        self.incorrect_label.grid(row=0, column=1, padx=5)

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
                                        bg="#CCE5FF", font=("Arial", "12", "bold"),
                                        command=self.to_statistics)
        self.statistics_button.grid(row=4, column=1, padx=10, pady=10)

        self.next_button = Button(self.button_frame, width=16, text="Next Round",
                                  bg="#D5E8D4", font=("Arial", "12", "bold"),
                                  command=self.next_round)
        self.next_button.grid(row=4, column=2, padx=10, pady=10)
        self.next_button.config(state=DISABLED)

        # Statistics
        self.user_answers = []
        self.correct_answers_list = []
        self.round_scores = []

    def close_play(self):
        # reshow root (i.e., choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

    def to_help(self):
        DisplayHelp(self)

    def to_statistics(self):
        DisplayStats(self, self.user_answers, self.correct_answers_list)

    def check_answer(self, button, button_name):
        # enable next round button
        self.next_button.config(state=NORMAL)
        # Disable all buttons
        for btn in self.buttons:
            btn.config(state=DISABLED)

        # Find the correct answer button and change its color to green
        correct_answer = self.button_question[0][1]
        correct_button = None
        for btn in self.buttons:
            if btn.cget("text") == correct_answer:
                correct_button = btn
                break

        # Change the color of the selected button to red if incorrect
        if button.cget("text") != correct_answer:
            button.config(bg="#FF0000")  # Red color
            self.incorrect_answers += 1
            self.incorrect_label.config(text="Incorrect: {}".format(self.incorrect_answers))
        else:
            button.config(bg="#008000")  # Green color
            # Update the score counters
            self.correct_answers += 1
            self.correct_label.config(text="Correct: {}".format(self.correct_answers))
        if correct_button is not None:
            correct_button.config(bg="#008000")  # Green color

        # Append user's answer and correct answer to the respective lists
        self.user_answers.append(button_name)
        self.correct_answers_list.append(correct_answer)

        # Enable the next button
        self.next_button.config(state=NORMAL)

    def next_round(self):
        self.next_button.config(state=DISABLED)
        self.rounds_played.set(self.rounds_played.get() + 1)
        if self.rounds_played.get() >= self.rounds_wanted.get():
            self.play_box.destroy()
            root.deiconify()
        else:
            self.rounds_heading.config(text="Round {} of {}".format(self.rounds_played.get() + 1, self.rounds_wanted.get()))
            self.generate_new_question()

    def generate_new_question(self):
        count = 0
        self.button_question = self.get_round_colours()
        question = self.button_question[count][0]
        answer = self.button_question[count][1]
        count += 1

        instructions = "{} is the fear of what?".format(question)
        self.rounds_instructions.config(text=instructions)

        # Enable all buttons
        for btn in self.buttons:
            btn.config(state=NORMAL)

        # Reset button colors
        for btn in self.buttons:
            btn.config(bg="#484770")

        # Assign new answers to buttons
        right = random.randint(1, 4)
        button_names = ["1", "2", "3", "4"]
        for i, btn in enumerate(self.buttons):
            if right != (i + 1):
                self.button_phobia = self.get_round_colours()
                text = self.button_phobia[i][1]
                btn.config(text=text)
            else:
                self.button_phobia = self.get_round_colours()
                text = answer
                btn.config(text=text)

    def get_list(self):
        file = open("fear_list_csv.csv", "r")
        var_all_questions = list(csv.reader(file, delimiter=","))
        # removes first entry in list
        var_all_questions.pop(0)
        return var_all_questions

    def get_round_colours(self):
        round_colour_list = []
        color_scores = []

        # Get four unique colours
        while len(round_colour_list) < 4:
            # Read from the CSV file if all questions have been used
            if not self.all_questions:
                self.all_questions = self.get_list()

            chosen_colour = random.choice(self.all_questions)
            index_chosen = self.all_questions.index(chosen_colour)

            if chosen_colour[1] not in color_scores:
                round_colour_list.append(chosen_colour)
                color_scores.append(chosen_colour[1])

                self.all_questions.pop(index_chosen)

        return round_colour_list


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


class DisplayStats:

    def __init__(self, partner, user_answers, correct_answers):
        # set up dialogue box and background colour
        background = "#DAE8FC"
        self.stats_box = Toplevel()

        # disable stats button
        partner.statistics_button.config(state=DISABLED)

        # if users press cross at top, closes stats and
        # 'releases' stats button
        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=300, height=200,
                                 bg=background)
        self.stats_frame.grid()

        self.stats_heading = Label(self.stats_frame,
                                   text="Statistics", bg=background,
                                   font=("Arial", "14", "bold"))
        self.stats_heading.grid(row=0)

        stats_text = "Here are your game statistics"

        self.stats_text_label = Label(self.stats_frame, bg=background,
                                      text=stats_text, justify="left")
        self.stats_text_label.grid(row=1, padx=10)

        # create scrollable frame
        self.scroll_canvas = Canvas(self.stats_frame, bg=background)
        self.scroll_canvas.grid(row=2, padx=10, pady=10, sticky=NSEW)

        self.scroll_frame = Frame(self.scroll_canvas, bg=background)
        self.scroll_frame.pack(fill=BOTH, expand=True)

        self.scroll_canvas.create_window((0, 0), window=self.scroll_frame, anchor=NW)

        self.scroll_frame.bind("<Configure>", self.adjust_scroll_region)
        self.scroll_canvas.bind_all("<MouseWheel>", self.mouse_scroll)

        # background formatting for heading, odd and even rows
        head_back = "#FFFFFF"
        odd_rows = "#C9D6E8"
        even_rows = background

        row_names = ["Question", "Your Answer", "Correct Answer"]

        # create labels for column headings
        for col, name in enumerate(row_names):
            self.data_label = Label(self.scroll_frame, text=name,
                                    bg=head_back,
                                    width="15", height="3", padx=5, pady=5, wraplength=100)
            self.data_label.grid(row=0, column=col, sticky=W)

        # create labels for question numbers and answers
        for i, (user_answer, correct_answer) in enumerate(zip(user_answers, correct_answers), start=1):
            label_text = "Round {}".format(i)
            self.data_label = Label(self.scroll_frame, text=label_text,
                                    bg=odd_rows if i % 2 != 0 else even_rows,
                                    width="15", height="3", padx=5, pady=5, wraplength=100)
            self.data_label.grid(row=i, column=0, sticky=W)

            self.data_label = Label(self.scroll_frame, text=user_answer,
                                    bg=odd_rows if i % 2 != 0 else even_rows,
                                    width="15", height="3", padx=5, pady=5, wraplength=100)
            self.data_label.grid(row=i, column=1, sticky=W)

            self.data_label = Label(self.scroll_frame, text=correct_answer,
                                    bg=odd_rows if i % 2 != 0 else even_rows,
                                    width="15", height="3", padx=5, pady=5, wraplength=100)
            self.data_label.grid(row=i, column=2, sticky=W)

        # create vertical scrollbar
        scrollbar = ttk.Scrollbar(self.stats_frame, orient=VERTICAL, command=self.scroll_canvas.yview)
        scrollbar.grid(row=2, column=3, sticky=N+S)

        # configure the canvas to use the scrollbar
        self.scroll_canvas.configure(yscrollcommand=scrollbar.set)

        self.scroll_frame.update_idletasks()
        self.scroll_canvas.config(scrollregion=self.scroll_canvas.bbox("all"))

        # dismiss button
        self.dismiss_button = Button(self.stats_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_stats,
                                                     partner))
        self.dismiss_button.grid(row=3, padx=10, pady=10)

    # closes stats dialogue (used by button and x at top of dialogue)
    def close_stats(self, partner):
        # Put stats button back to normal...
        partner.statistics_button.config(state=NORMAL)
        self.stats_box.destroy()

    def adjust_scroll_region(self, event):
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))

    def mouse_scroll(self, event):
        self.scroll_canvas.yview_scroll(int(-event.delta / 120), "units")


# main routine
if __name__ == "__main__":
    root = Tk()
    antigravity = 1
    root.title("Fear or Fail")
    Rounds()
    root.mainloop()
