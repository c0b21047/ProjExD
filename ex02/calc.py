import tkinter as tk
import tkinter.messagebox as tkm

root = tk.Tk()
root.geometry("300x500")

x = 0
y = 0
for i in range(9,-1,-1):
    button = tk.Button(root,text=i,width=4,height=2,font=("",30))
    button.grid(row=y, column=x)
    if x >= 2:
        x = 0
        y += 1
    else:
        x += 1

root.mainloop()