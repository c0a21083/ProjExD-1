import tkinter as tk
import tkinter.messagebox as tkm

#練習8
import maze_maker as mz_m

#練習6
def key_up(event):
    global key
    key = ""

#ゴールにかかった時間を計測する関数
def count_up():
    global tmr, jid
    label["text"] = tmr
    tmr += 1
    jid = root.after(1000, count_up)

#練習7 and 練習11
def main_proc(event):
    global mx, my
    global cx, cy
    global key
    global tmr, jid
    global count
    key = event.keysym

    if mx == 13 and my == 7:
        root.after_cancel(jid)
        tkm.showinfo("GOAL", f"所要時間：{tmr}秒かかりました。")

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
    root.geometry("1500x1000")
    
    #練習9
    canv_lst = mz_m.make_maze(15, 9)

    #練習2
    canvas = tk.Canvas(root, width=1500, height=900, bg = "black")
    canvas.pack()

    #練習10
    mz_m.show_maze(canvas, canv_lst)

    #スタートの文字をはじめに表示させる
    start_image = tk.PhotoImage(file="fig/start.png")
    s_x, s_y = 1, 0
    s_xx, s_yy = s_x*100 + 50, s_y*100 + 70
    canvas.create_image(s_xx, s_yy, image=start_image, tag="start")

    #練習3
    cx , cy = 150, 150
    mx, my = 1, 1
    tori = tk.PhotoImage(file="fig/6.png")
    canvas.create_image(cx, cy, image=tori, tag="tori")

    #ゴールの文字を最後に表示させる
    goal_image = tk.PhotoImage(file="fig/goal.png")
    g_x, g_y = 13, 7
    g_xx, g_yy = g_x*100 + 50, g_y*100 + 50
    canvas.create_image(g_xx, g_yy, image=goal_image, tag="goal")
    
    #ゴールにかかった時間を計測
    label = tk.Label(root, text = "-", font=("", 80))
    label.pack()

    tmr = 0
    jid = None
    count_up()

    #練習4
    key = ""

    root.bind("<KeyPress>", main_proc)
    root.mainloop()