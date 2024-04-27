import tkinter

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

cycle = 1
runThread = ""
totalLoops = 0

# ---------------------------- TIMER RESET ------------------------------- #


def resetTimer():
    global cycle, totalLoops
    startBtn["state"] = tkinter.NORMAL
    resetBtn["state"] = tkinter.DISABLED
    window.after_cancel(runThread)  # cancel continuous function call thread
    timerLabel.config(text="Timer", fg=GREEN)
    canvas.itemconfig(timerTxt, text="00:00")
    checkmarkFrame["text"] = ""
    multiplierLabel["text"] = ""
    cycle = 1
    totalLoops = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #


def startTimer():
    startBtn["state"] = tkinter.DISABLED
    resetBtn["state"] = tkinter.NORMAL
    timerLabel.config(text="Work", fg=GREEN)
    multiplierLabel["text"] = "Total completed \nloops: 0"
    countdown(WORK_MIN, 0)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def countdown(mins, secs):
    global cycle, runThread, totalLoops

    if mins == 0 and secs == 0:
        cycle += 1
        mins = SHORT_BREAK_MIN if cycle % 2 == 0 else WORK_MIN
        mins = LONG_BREAK_MIN if cycle % 8 == 0 else mins
        checkmarkFrame["text"] += "✔" if cycle % 2 == 0 else ""
        checkmarkFrame["text"] = "" if (cycle + totalLoops) % 9 == 0 else checkmarkFrame["text"]

        totalLoops += 1 if (cycle + totalLoops) % 9 == 0 else 0
        multiplierLabel["text"] = f"Total completed \nloops: {totalLoops}" if (cycle + (totalLoops - 1)) % 9 == 0 else multiplierLabel["text"]

        timerLabel.config(text="Work", fg=GREEN) if mins == WORK_MIN else timerLabel
        timerLabel.config(text="Break", fg=PINK) if mins == SHORT_BREAK_MIN else timerLabel
        timerLabel.config(text="Break", fg=RED) if mins == LONG_BREAK_MIN else timerLabel

        window.attributes('-topmost', 1)  # put the window temporarily on top of the others
        window.attributes('-topmost', 0)

    mins = mins - 1 if secs == 0 else mins
    secs = secs - 1 if secs > 0 else 59
    minsStr = "0" + str(mins) if mins < 10 else mins
    secsStr = "0" + str(secs) if secs < 10 else secs

    canvas.itemconfig(timerTxt, text=f"{minsStr}:{secsStr}")

    runThread = window.after(1000, countdown, mins, secs)  # calls function after specified time, without interrupting program regular flow, with recursivity

# ---------------------------- UI SETUP ------------------------------- #


window = tkinter.Tk()
window.title("Pomodoro")
window.config(padx=50, pady=50, bg=YELLOW)

canvas = tkinter.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)  # create canvas to store image, with yellow bg and no borders
tomatoPic = tkinter.PhotoImage(file="tomato.png")  # get image
canvas.create_image(100, 112, image=tomatoPic)  # X and Y position of the image in the canvas
timerTxt = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

timerLabel = tkinter.Label(text="Timer", font=(FONT_NAME, 35, "bold"), fg=GREEN, bg=YELLOW)
timerLabel.grid(row=0, column=1)

startBtn = tkinter.Button(text="Start", bg="#FFFFFF", bd=1, command=startTimer, font=(FONT_NAME, 14, "bold"))
startBtn.grid(row=2, column=0)

resetBtn = tkinter.Button(text="Reset", bg="#FFFFFF", bd=1, command=resetTimer, state=tkinter.DISABLED, font=(FONT_NAME, 14, "bold"))
resetBtn.grid(row=2, column=2)

checkmarkFrame = tkinter.Label(text="", font=(FONT_NAME, 20, "bold"), fg=GREEN, bg=YELLOW)
checkmarkFrame.grid(row=3, column=1)

multiplierLabel = tkinter.Label(text="", font=(FONT_NAME, 12, "bold"), fg=RED, bg=YELLOW)
multiplierLabel.grid(row=4, column=1)

window.mainloop()
