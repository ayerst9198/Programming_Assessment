import tkinter as tk
import time

root = tk.Tk()
root.title("Dancing Banana")
root.geometry("400x450")

canvas = tk.Canvas(root, width=400, height=450)
canvas.pack()

# add a red water-like background
bg = canvas.create_rectangle(0, 0, 400, 450, fill="red")

body = canvas.create_oval(150, 100, 250, 300, fill="yellow")
stem = canvas.create_rectangle(195, 75, 205, 100, fill="brown")
left_arm = canvas.create_rectangle(100, 170, 150, 180, fill="yellow")
right_arm = canvas.create_rectangle(250, 170, 300, 180, fill="yellow")
left_leg = canvas.create_rectangle(175, 290, 185, 340, fill="brown")
right_leg = canvas.create_rectangle(215, 290, 225, 340, fill="brown")
face = canvas.create_oval(175, 125, 225, 175, fill="white")
left_eye = canvas.create_oval(190, 145, 195, 150, fill="black")
right_eye = canvas.create_oval(210, 145, 215, 150, fill="black")
mouth = canvas.create_arc(180, 155, 220, 170, start=180, extent=180, fill="red")

message = canvas.create_text(200, 350, text="Flying Banana God", font=("Helvetica", 20))

while True:
    for i in range(10):
        canvas.move(body, 0, -5)
        canvas.move(stem, 0, -5)
        canvas.move(left_arm, 0, -5)
        canvas.move(right_arm, 0, -5)
        canvas.move(left_leg, 0, -5)
        canvas.move(right_leg, 0, -5)
        canvas.move(face, 0, -5)
        canvas.move(left_eye, 0, -5)
        canvas.move(right_eye, 0, -5)
        canvas.move(mouth, 0, -5)
        canvas.move(message, 0, -5)
        root.update()
        time.sleep(0.05)
    for i in range(10):
        canvas.move(body, 0, 5)
        canvas.move(stem, 0, 5)
        canvas.move(left_arm, 0, 5)
        canvas.move(right_arm, 0, 5)
        canvas.move(left_leg, 0, 5)
        canvas.move(right_leg, 0, 5)
        canvas.move(face, 0, 5)
        canvas.move(left_eye, 0, 5)
        canvas.move(right_eye, 0, 5)
        canvas.move(mouth, 0, 5)
        canvas.move(message, 0, 5)
        root.update()
        time.sleep(0.05)

root.mainloop()
