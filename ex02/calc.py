import tkinter as tk
import tkinter.messagebox as tkm

x = 0
y = 3
num = [i for i in range(9,0,-1)]
ope = ["c","bs","√","+","-","*","/","="]
ckdel = False

def ope_fnc(event):
    global ckdel
    btn = event.widget
    txt = btn["text"]
    if txt == "=":
        formula = entry2.get() + entry.get()
        ans = eval(formula)
        entry2.insert(tk.END,entry.get()+"=")
        entry.delete(0,tk.END)
        entry.insert(tk.END,ans)
        
        ckdel = True

    elif txt == "c":
        entry.delete(0,tk.END)
        entry.insert(tk.END,0)

    elif txt == "+/-":
        try:
            sub = int(entry.get())
        except ValueError:
            sub = float(entry.get())
        if sub != 0:
            sub *= -1
            entry.delete(0,tk.END)
            entry.insert(tk.END,sub)

    elif txt == "bs":
        entry.delete(0,1)
        if entry.get() == "":
            entry.insert(tk.END,0)
        
    elif txt == "√":
        sub = float(entry.get()) ** (1/2)
        if list(str(sub))[-1] == "0":
            sub = int(sub)
        entry.delete(0,tk.END)
        entry.insert(tk.END,sub)

    elif txt == "+" or txt == "-" or txt == "*" or txt == "/":
        entry.insert(tk.END,txt)
        entry2.insert(tk.END,entry.get())
        entry.delete(0,tk.END) 
        entry.insert(tk.END,0)

    else:
        if txt != "." or "." not in list(entry.get()):
            entry.insert(tk.END,txt)


def button_click(event):
    global ckdel
    if ckdel:
        entry2.delete(0,tk.END)
        ckdel = False
    btn = event.widget
    txt = btn["text"]
    if txt in ope+["+/-","."]:
        ope_fnc(event)
    else:
        if entry.get() == "0":
            entry.delete(0)
        entry.insert(tk.END,txt)

root = tk.Tk()
root.geometry("300x500")

entry = tk.Entry(root,width=10,justify="right",font=("Times New Roman",40))
entry.insert(0,"0")
entry.grid(row=1,column=0,columnspan=4)

entry2 = tk.Entry(root,width=19,justify="right",font=("Times New Roman",20))
entry2.grid(row=0,column=0,columnspan=4)

 
x = 2
for i in (num+[".",0,"+/-"]): #数字ボタンの配置
    button = tk.Button(root,text=i,width=3,height=1,font=("",30))
    button.bind("<1>",button_click)
    button.grid(row=y, column=x)
    if x <= 0:
        x = 2
        y += 1
    else:
        x -= 1

y = 2
x = 0

for i in ope:
    button = tk.Button(root,text=i,width=3,height=1,font=("",30))
    button.bind("<1>",button_click)
    button.grid(row=y, column=x)
    if x >= 3:
        y += 1
    else:
        x += 1


root.mainloop()