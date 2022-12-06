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

#練習7 and 練習11
def main_proc(event):
    global mx, my, cx, cy, key
    key = event.keysym
    if key == "Up":
        my -= 1
        if canv_lst[mx][my] == 0:
            cy = my*100 + 50
        else:
            my += 1
    elif key == "Left":
        mx -= 1
        if canv_lst[mx][my] == 0:
            cx = mx*100 + 50
        else:
            mx += 1
    elif key == "Right":
        mx += 1
        if canv_lst[mx][my] == 0:
            cx = mx*100 + 50
        else:
            mx -= 1
    elif key == "Down":
        my += 1
        if canv_lst[mx][my] == 0:
            cy = my*100 + 50
        else:
            my -= 1

    canvas.coords("tori", cx, cy)

if __name__ == "__main__":
    #練習1
    root = tk.Tk()
    root.title("迷えるこうかとん")
    root.geometry("1500x900")
    
    #練習9
    canv_lst = mz_m.make_maze(15, 9)

    #練習2
    canvas = tk.Canvas(root, width=1500, height=900, bg = "black")
    canvas.pack()

    #練習10
    mz_m.show_maze(canvas, canv_lst)

    #練習3
    cx , cy = 150, 150
    mx, my = 1, 1
    tori = tk.PhotoImage(file="fig/6.png")
    canvas.create_image(cx, cy, image=tori, tag="tori")

    #練習4
    key = ""

root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)
root.bind("<KeyPress>", main_proc)

root.mainloop()