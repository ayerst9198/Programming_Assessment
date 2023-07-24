from tkinter import *
from functools import partial
from tkinter import ttk


class Colour:

    def __init__(self):
        # invoke play class with three rounds for testing purposes.
        self.to_play(3)

        # hide Menu
        root.withdraw()

    def to_play(self, num_rounds):
        Play(num_rounds)


class Play:

    def __init__(self, how_many):
        self.play_box = Toplevel()

        # lists of user and computer scores
        # used to work out stats
        self.users_scores = [20, 14, 14, 13, 14, 11, 20, 10, 20, 11]
        self.computer_scores = [12, 4, 6, 20, 20, 14, 10, 14, 16, 22]

        # if users press cross at tip, closes help and
        # 'refuses' help button
        self.play_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_play))

        self.quest_frame = Frame(self.play_box, padx=10, pady=10)
        self.quest_frame.grid()

        self.control_frame = Frame(self.quest_frame)
        self.control_frame.grid(row=6)

        control_buttons = [
            ["#CC6600", "Help", "get help"],
            ["#004C99", "Statistics", "get stats"],
            ["#808080", "Start Over", "start over"]
        ]

        # list to hold  references for control buttons
        # so that the text of the 'start over' button
        # con easily be configured when the game
        self.control_button_ref = []

        for item in range(0, 3):
            self.make_control_button = Button(self.control_frame,
                                              fg="#FFFFFF",
                                              bg=control_buttons[item][0],
                                              text=control_buttons[item][1],
                                              width=11, font=("Arial", 12, "bold"),
                                              command=lambda i=item: self.to_do(control_buttons[i][2]))
            self.make_control_button.grid(row=0, column=item, padx=5, pady=5)

            # add buttons to control list
            self.control_button_ref.append(self.make_control_button)

        # disable help button
        self.to_help_btn = self.control_button_ref[0]
        self.to_stats_btn = self.control_button_ref[1]

    def to_do(self, action):
        if action == "get help":
            DisplayHelp(self)
        elif action == "get stats":
            DisplayStats(self, self.users_scores, self.computer_scores)
        else:
            self.close_play()

    def close_play(self):
        # reshow menu
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


class DisplayHelp:

    def __init__(self, partner):
        # set up dialogue box and background colour
        background = "#ffe6cc"
        self.help_box = Toplevel()

        # disable help button
        partner.to_help_btn.config(state=DISABLED)

        # if users press cross at top, closes help and
        # 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300, height=200,
                                bg=background)
        self.help_frame.grid()

        self.help_heading = Label(self.help_frame,
                                  text="Help / Info", bg=background,
                                  font=("Arial", "23", "bold"))
        self.help_heading.grid(row=0)

        help_text = "Your goal in this game is to beat the computer and you " \
                    "have an advantage - you get to choose your colour first. " \
                    "The points associated with the colour are based on the colours " \
                    "hex code." \
                    "\n\n" \
                    "The higher the value of the colour, the greater your score. To " \
                    "see your statistics, press the 'Statistics' button. \n\n" \
                    "Win the game by scoring more than the computer overall. " \
                    "Don't be discouraged if you don't win every round; it's " \
                    "your overall score that counts.\n\n" \
                    "Good luck! Choose carefully."

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
        partner.to_help_btn.config(state=NORMAL)
        self.help_box.destroy()


class DisplayStats:

    def __init__(self, partner, user_scores, computer_scores):
        # set up dialogue box and background colour
        background = "#DAE8FC"
        self.stats_box = Toplevel()

        # disable stats button
        partner.to_stats_btn.config(state=DISABLED)

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

        self.user_stats = self.get_stats(user_scores, "User")
        self.comp_stats = self.get_stats(computer_scores, "Computer")

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

        # create labels for question numbers
        for i, (user_answer, correct_answer) in enumerate(zip(self.user_stats[1:], self.comp_stats[1:]), start=1):
            label_text = str(i)
            self.data_label = Label(self.scroll_frame, text=label_text,
                                    bg=odd_rows if i % 2 != 0 else even_rows,
                                    width="15", height="3", padx=5, pady=5, wraplength=100)
            self.data_label.grid(row=i, column=0, sticky=W)

            self.data_label = Label(self.scroll_frame, text="User's Answer",
                                    bg=odd_rows if i % 2 != 0 else even_rows,
                                    width="15", height="3", padx=5, pady=5, wraplength=100)
            self.data_label.grid(row=i, column=1, sticky=W)

            self.data_label = Label(self.scroll_frame, text="Correct Answer",
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
        partner.to_stats_btn.config(state=NORMAL)
        self.stats_box.destroy()

    # calculate stats and column
    # heading at first item
    @staticmethod
    def get_stats(score_list, entity):
        total_score = sum(score_list)
        best_score = max(score_list)
        worst_score = min(score_list)
        average = total_score / len(score_list)

        return [entity, total_score, best_score, worst_score, average]

    def adjust_scroll_region(self, event):
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))

    def mouse_scroll(self, event):
        self.scroll_canvas.yview_scroll(int(-event.delta / 120), "units")


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    Colour()
    root.mainloop()
