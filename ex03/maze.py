import tkinter as tk
import tkinter.messagebox as tkm

#練習8
import maze_maker as mz_m

#練習5
def key_down(event):
    global key
    key = event.keysym

#練習6
def key_up(event):
    global key
    key = ""

#練習7
def main_proc(event):
    global cx, cy, key
    key = event.keysym
    if key == "Up":
        cy -= 20
    elif key == "Left":
        cx -= 20
    elif key == "Right":
        cx += 20
    elif key == "Down":
        cy += 20
    canvas.coords("tori", cx, cy)

if __name__ == "__main__":
    #練習1
    root = tk.Tk()
    root.title("迷えるこうかとん")
    root.geometry("1500x900")
    
    #練習9
    mz_m.make_maze(15, 9)

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
root.bind("<KeyPress>", main_proc)
root.mainloop()