import tkinter as tk
import tkinter.messagebox as tkm


def key_down(event):
    global key
    key = event.keysym #練習5


def key_up(event):
    global key
    key = "" #練習6


def main_proc():
    global cx,cy
    if key == "Up":
        cy -= 20
    elif key == "Down":
        cy += 20
    elif key == "Left":
        cx -= 20
    elif key == "Right":
        cx += 20
    canv.coords("tori",cx,cy)
    root.after(100,main_proc) #練習7


if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん") #練習1
    
    canv = tk.Canvas(root,width=1500,height=900,bg="black")
    canv.pack() #練習2

    tori = tk.PhotoImage(file="fig/0.png")
    cx, cy = 300, 400
    canv.create_image(cx, cy, image=tori, tag="tori") #練習3

    key = "" #練習4
    root.bind("<KeyPress>",key_down)

    root.bind("<KeyRelease>",key_up)
    
    main_proc()
    root.mainloop()
    