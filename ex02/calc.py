import tkinter as tk
import tkinter.messagebox as tkm


#ボタン警告
def button_click(event):
    btn = event.widget
    num = btn["text"]
    tkm.showinfo("", f"{num}ボタンがクリックされました")

#数字をクリック
def number_click(event):
    btn = event.widget
    num = btn["text"]
    entry.insert(tk.END,num)
    
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

#ウィンドウ作成
root = tk.Tk()
root.geometry("300x500")

#Entryクラス(入力欄描画)
entry = tk.Entry(root, width=10, font=(", 40"),justify="right")
entry.grid(row=0, column=0, columnspan=3)

#数字ボタン作成
r, c = 1, 0
for i in range(9, -1, -1):
    button = tk.Button(root, text=f"{i}", width=4, height=2,font=("", "30"))
    button.grid(row= r , column = c)
    button.bind("<1>", number_click)
    c += 1

    if c % 3 == 0:
        r += 1
        c = 0

button = tk.Button(root, text="=", width=4, height=2, font=("", "30"))
button.grid(row= 4 , column = 2)
button.bind("<1>", equal_click)

button = tk.Button(root, text="+", width=4, height=2, font=("", "30"))
button.grid(row= 4 , column = 1)
button.bind("<1>", plus_click)



root.mainloop()