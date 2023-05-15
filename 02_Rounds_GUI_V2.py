from tkinter import *


class Rounds:

    def __init__(self):
        # common format for all buttons
        # Arial size 14 bold, with white text
        button_font = ("Arial", "12", "bold")
        button_fg = "#FFFFFF"

        # Set up GUI Frame
        self.rounds_frame = Frame(padx=10, pady=10)
        self.rounds_frame.grid()

        self.rounds_heading = Label(self.rounds_frame,
                                    text="Fear or Fail",
                                    font=("Arial", "30", "bold",)
                                    )
        self.rounds_heading.grid(row=0)

        instructions = "Fear or Fail is a super spectacular quiz. You will be given " \
                       "4 options to choose from for each question, simply click the " \
                       "answer you want to choose, and you will be told whether you are " \
                       "right or wrong, and which answer the correct one is." \
                       "\n\n" \
                       "In order to start, simply enter the number of rounds you want to play " \
                       "between 1 and 113 rounds in the field below, and press enter or start to begin the quiz." \
                       "\n\n" \
                       "*Please note that Fear or Fail is not responsible for any harm that comes to the " \
                       "participant in the event they do not get a perfect score" \
                       "" \
                       "\n\n\n" \
                       "** TLDR: ENTER ROUNDS BETWEEN 1 AND 113 AND PRESS START, THEN CLICK THE CORRECT ANSWER"

        self.rounds_instructions = Label(self.rounds_frame,
                                         text=instructions,
                                         wraplength=300, width=60,
                                         justify="left")
        self.rounds_instructions.grid(row=1, pady=20)

        self.rounds_error = Label(self.rounds_frame, text="",
                                  fg="#9C0000", font="bold")
        self.rounds_error.grid(row=3)

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        self.entry_rounds_frame = Entry(self.start_frame,
                                        width=9, font=("Arial", "19"))
        self.entry_rounds_frame.grid(row=4, column=0, pady=5)

        self.start_button = Button(self.start_frame, width=12, text="Start",
                                   font=("Arial", "12", "bold",), bg="#429E9D",
                                   command= self.rounds_check)
        self.start_button.grid(row=4, column=1, pady=5)

        # Conversion, help and statistics
        self.button_frame = Frame(self.rounds_frame)
        self.button_frame.grid(row=5)

        self.help_button = Button(self.start_frame, width=12, text="Help",
                                  bg="#FFCC99", font=("Arial", "12", "bold"))
        self.help_button.grid(row=5, column=0, padx=10, pady=10)

        self.statistics_button = Button(self.start_frame, width=12, text="Statistics",
                                        bg="#CCE5FF", font=("Arial", "12", "bold"))
        self.statistics_button.grid(row=5, column=1, padx=10, pady=10)

    def check_rounds(self, min_value, max_value):
        error = "Please enter the number of rounds rounds \n you want to play between 1 - 113"

        try:
            response = self.entry_rounds_frame.get()
            response = int(response)

            if response < min_value or response > max_value:
                self.rounds_error.config(text=error, fg="#9C0000")
            else:
                self.rounds_error.config(text="You chose to play {} rounds".format(response), fg="#32CD32")
                return response

        except ValueError:
            self.rounds_error.config(text=error, fg="#9C0000")

    def rounds_check(self):
        self.check_rounds(1, 113)


# main routine
if __name__ == "__main__":
    root = Tk()
    antigravity = 1
    root.title("Fear or Fail")
    Rounds()
    root.mainloop()
