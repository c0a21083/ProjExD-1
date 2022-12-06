import tkinter as tk
import tkinter.messagebox as tkm

#練習5
def key_down(event):
    global key
    key = event.keysym

#練習6
def key_up(event):
    global key
    key = ""

#練習1
if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん")
    root.geometry("1500x900")

    #練習2
    canvas = tk.Canvas(root, width=1500, height=900, bg = "black")
    canvas.pack()

    #練習3
    cx , cy = 300, 400
    tori = tk.PhotoImage(file="fig/6.png")
    canvas.create_image(cx, cy, image=tori, tag="tori")

    #練習4
    key = ""

root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)
root.mainloop()