
from tkinter import *
import pygame

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 1
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

timer = None
session_no = 0

#play beep sound
def play_beep_sound():
    pygame.mixer.init()
    my_sound = pygame.mixer.Sound('beep.wav')
    my_sound.play()


# append 0 before 1 digit number
def attach_zero(time_str):
    if len(time_str) == 1:
        time_str = "0" + time_str
    return time_str

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global session_no
    session_no = 0
    canvas.itemconfig(timer_text, text="00:00")
    window.after_cancel(timer)
    btn_start.config(state=NORMAL)

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    play_beep_sound()
    btn_start.config(state=DISABLED)
    global session_no
    session_no += 1

    if session_no % 8 == 0:
        count_down(LONG_BREAK_MIN * 60)
        title_label.config(text = "Break", fg=RED)
    elif session_no % 2 == 0:
        count_down(SHORT_BREAK_MIN * 60)
        title_label.config(text="Break", fg=PINK)
    else:
        count_down(WORK_MIN * 60)
        title_label.config(text="Work", fg=GREEN)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def count_down(count):
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count-1)
        min = attach_zero(str(count// 60))
        sec = attach_zero(str(count % 60))
        canvas.itemconfig(timer_text, text= f"{min}:{sec}")
    else:
        ticks = ""
        work_sessions = int((session_no+1) / 2)
        for _ in range(work_sessions):
            ticks += "✔"
        lbl_ticks.config(text=ticks)
        canvas.itemconfig(timer_text, text="00:00")
        start_timer()



# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro App")
window.config(padx=100, pady=50,bg=YELLOW)

title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)

canvas = Canvas(window,bg=YELLOW, height=224, width = 200,highlightthickness=0)
filename = PhotoImage(file="tomato.png")
img_tomato = canvas.create_image(100,112, image=filename)
timer_text = canvas.create_text(100, 130, text = "00:00",font=(FONT_NAME, 35, "bold"),fill="white")

btn_start = Button(window, text="Start", command=start_timer)
btn_start.grid(row=4, column=0)

btn_reset = Button(window, text="Reset", command=reset_timer)
btn_reset.grid(row=4, column=2)

lbl_ticks = Label(text = "", fg=GREEN, bg=YELLOW, justify="center", font=(FONT_NAME, 20, "bold"))
lbl_ticks.grid(row=4, column=1)

canvas.grid(row=1,column=1)
window.mainloop()