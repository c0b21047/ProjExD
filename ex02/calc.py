import tkinter as tk
import tkinter.messagebox as tkm

def button_click(event):
    btn = event.widget
    txt = btn["text"]
    try:
        if txt == "=":
            formula = entry.get()
            ans = eval(formula)
            entry.delete(0,tk.END)
            entry.insert(tk.END,ans)
        else:
            entry.insert(tk.END,txt)
    except:
        None

root = tk.Tk()
root.geometry("300x500")

entry = tk.Entry(root,width=10,justify="right",font=("Times New Roman",40))
entry.grid(row=0,column=0,columnspan=3)

num = [i for i in range(9,-1,-1)]
ope = ["+","="]
x = 0
y = 1
max_x = 2
for i in (num+ope):
    button = tk.Button(root,text=i,width=4,height=2,font=("",30))
    button.bind("<1>",button_click)
    button.grid(row=y, column=x)
    if x>= max_x:
        x = 0
        y += 1
    else:
        x += 1

root.mainloop()