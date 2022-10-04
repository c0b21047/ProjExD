import tkinter as tk
import tkinter.messagebox as tkm

x = 0 
y = 3 #数字のボタンの左上の値
num = [i for i in range(9,0,-1)] #数字のリスト
ope = ["c","bs","√","+","-","*","/","="] #記号のリスト
ckdel = False #entry2の削除を行うかの判定用

def ope_fnc(event): #記号の処理
    global ckdel
    btn = event.widget
    txt = btn["text"]
    if txt == "=": # =の場合 entry2とentryで計算
        formula = entry2.get() + entry.get()
        ans = eval(formula)
        entry2.insert(tk.END,entry.get()+"=")
        entry.delete(0,tk.END)
        entry.insert(tk.END,ans)
        
        ckdel = True #次の処理時にentry2を消すように

    elif txt == "c": # cの場合全部消す
        entry.delete(0,tk.END)
        entry.insert(tk.END,0) 

    elif txt == "+/-": # +/-の場合
        try: #entry内の値がintならint floatならfloatで処理
            sub = int(entry.get())
        except ValueError:
            sub = float(entry.get())
        if sub != 0: #0ははじく
            sub *= -1
            entry.delete(0,tk.END)
            entry.insert(tk.END,sub)

    elif txt == "bs": # bsの場合 一文字消す
        entry.delete(0,1)
        if entry.get() == "":
            entry.insert(tk.END,0)
        
    elif txt == "√": # √の場合 1/2乗して一番最後の数字が0ならそれを消すはずだったがなんか違う
        sub = float(entry.get()) ** (1/2)
        if list(str(sub))[-1] == "0":
            sub = int(sub)
        entry.delete(0,tk.END)
        entry.insert(tk.END,sub)

    elif txt == "+" or txt == "-" or txt == "*" or txt == "/": #四則演算用
        entry.insert(tk.END,txt)
        entry2.insert(tk.END,entry.get())
        entry.delete(0,tk.END) 
        entry.insert(tk.END,0)

    else:
        if txt != "." or "." not in list(entry.get()): # .が二つ以上にならないようにする
            entry.insert(tk.END,txt)


def button_click(event): #数字のボタンの処理
    global ckdel
    if ckdel:
        entry2.delete(0,tk.END) #entry2の削除
        ckdel = False
    btn = event.widget
    txt = btn["text"]
    if txt in ope+["+/-","."]: #記号の場合
        ope_fnc(event)
    else:
        if entry.get() == "0": #entry内が0のみの場合0を消す
            entry.delete(0)
        entry.insert(tk.END,txt)

root = tk.Tk()
root.geometry("300x500") #サイズ

entry = tk.Entry(root,width=10,justify="right",font=("Times New Roman",40))
entry.insert(0,"0")
entry.grid(row=1,column=0,columnspan=4) #数字が入るところ

entry2 = tk.Entry(root,width=19,justify="right",font=("Times New Roman",20))
entry2.grid(row=0,column=0,columnspan=4) #entry2の設定

 
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

for i in ope: #記号ボタンの配置
    button = tk.Button(root,text=i,width=3,height=1,font=("",30))
    button.bind("<1>",button_click)
    button.grid(row=y, column=x)
    if x >= 3:
        y += 1
    else:
        x += 1


root.mainloop()