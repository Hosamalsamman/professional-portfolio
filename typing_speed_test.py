from faker import Faker
from tkinter import *
import difflib

counter = 0
timer = None
current_text = ""


def random_fake_text(max_chars=50):
    fake = Faker()
    text = fake.text(max_nb_chars=max_chars)
    return text


def count_up():
    global counter
    global timer
    counter += 1
    canvas.itemconfig(title_text, text=f"{counter}")
    timer = window.after(1000, count_up)  # reschedule itself


def start_on_typing(event):
    if counter == 0 and timer is None:  # only start once
        start_counter()


def check_done(event=None):
    user_text = entry.get()
    if len(user_text) >= len(current_text):
        get_result()


def start_counter():
    global timer
    global current_text
    # entry.config(state="normal")
    entry.delete(0, END)
    current_text = random_fake_text()
    canvas.itemconfig(test_text, text=current_text)
    timer = window.after(1000, count_up)


def get_result():
    global counter, timer
    window.after_cancel(timer)
    user_text = entry.get()

    # Words per minute
    minutes = counter / 60
    wpm = len(user_text.split()) / minutes if minutes > 0 else 0

    # Accuracy
    similarity = difflib.SequenceMatcher(None, current_text, user_text).ratio() * 100

    canvas.itemconfig(
        test_text,
        text=f"WPM: {wpm:.2f}\nAccuracy: {similarity:.2f}%"
    )

    # Reset
    counter = 0
    entry.delete(0, END)
    timer = None
    # entry.config(state="disabled")


window = Tk()
window.title("Typing speed test")
window.config(padx=50, pady=50, bg="#f0f8ff")

canvas = Canvas(width=800, height=526, highlightthickness=0)
title_text = canvas.create_text(400, 150, text="Start typing to begin", font=("Arial", 40, "italic"))
test_text = canvas.create_text(400, 263, text="_", font=("Arial", 15, "bold"), width=700)
canvas.grid(row=0, column=0)

# start_btn = Button(text="START", command=start_counter)
# start_btn.grid(row=1, column=0)

entry = Entry(window, width=60, fg="black", bg="white", font=("Arial", 16), justify="center")
entry.grid(row=2, column=0)

entry.bind("<Key>", start_on_typing)

entry.bind("<KeyRelease>", check_done)

# stop_btn = Button(text="STOP", command=get_result)
# stop_btn.grid(row=3, column=0)

window.mainloop()



