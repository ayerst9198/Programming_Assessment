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

        instructions = "Instructions go here..."

        self.rounds_instructions = Label(self.rounds_frame,
                                         text=instructions,
                                         wraplength=400, width=60,
                                         justify="center")
        self.rounds_instructions.grid(row=1, pady=20)

        rounds_error = "Please enter the number of rounds rou want to play between 1-113"

        self.rounds_error = Label(self.rounds_frame, text="ERROR GOES HERE",
                                  fg="#9C0000", font=("bold"))
        self.rounds_error.grid(row=3)

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        self.entry_rounds_frame = Entry(self.start_frame,
                                        width=12, font=("Arial", "16"))
        self.entry_rounds_frame.grid(row=4, column=0, pady=5)

        self.start_button = Button(self.start_frame, width=6, text="Start",
                                   font=("Arial", "12", "bold",), bg="#429E9D")
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


# main routine
if __name__ == "__main__":
    root = Tk()
    antigravity = 1
    root.title("Fear or Fail")
    Rounds()
    root.mainloop()
