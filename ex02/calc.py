import tkinter as tk
import tkinter.messagebox as tkm


#ボタン警告
def button_click(event):
    btn = event.widget
    num = btn["text"]
    tkm.showinfo("", f"{num}ボタンがクリックされました")

#deleteする
def AC_click(event):
    entry.delete(0, tk.END)

#数字をクリック
def number_click(event):
    btn = event.widget
    num = btn["text"]
    entry.insert(tk.END,num)
    
#足し算
def plus_click(event):
    btn = event.widget
    num = btn["text"]
    entry.insert(tk.END, "+")
#＝をクリックした場合
def equal_click(event):
    eqn = entry.get()
    re = eval(eqn)
    entry.delete(0,tk.END)
    entry.insert(tk.END, re)

#引き算
def maina_click(event):
    btn = event.widget
    num = btn["text"]
    entry.insert(tk.END, "-")

#割り算
def warizan_click(event):
    btn = event.widget
    num = btn["text"]
    entry.insert(tk.END, "/")

#掛け算
def kakezan_click(event):
    btn = event.widget
    num = btn["text"]
    entry.insert(tk.END, "*")

#ウィンドウ作成
root = tk.Tk()
root.geometry("400x500")

#Entryクラス(入力欄描画)
entry = tk.Entry(root, width=15, font=(", 40"),justify="right")
entry.grid(row=0, column=0, columnspan=4)

#数字ボタン作成
r, c = 1, 0
num_list = [7, 8, 9, 4, 5, 6, 1, 2, 3, 0]
for i in num_list:
    button = tk.Button(root, text=f"{i}", width=4, height=2,font=("", "30"))
    button.grid(row= r , column = c)
    button.bind("<1>", number_click)
    c += 1

    if c % 3 == 0:
        r += 1
        c = 0

button = tk.Button(root, text="=", width=4, height=2, font=("", "30"))
button.grid(row= 4 , column = 3)
button.bind("<1>", equal_click)

button = tk.Button(root, text="+", width=4, height=2, font=("", "30"))
button.grid(row= 4 , column = 1)
button.bind("<1>", plus_click)

button = tk.Button(root, text="-", width=4, height=2, font=("", "30"))
button.grid(row= 4 , column = 2)
button.bind("<1>", maina_click)

button = tk.Button(root, text="/", width=4, height=2, font=("", "30"))
button.grid(row= 1 , column = 3)
button.bind("<1>", warizan_click)

button = tk.Button(root, text="*", width=4, height=2, font=("", "30"))
button.grid(row= 2 , column = 3)
button.bind("<1>", kakezan_click)

button = tk.Button(root, text="AC", width=4, height=2, font=("", "30"))
button.grid(row= 3 , column = 3)
button.bind("<1>", AC_click)


root.mainloop()