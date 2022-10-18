import tkinter as tk
import tkinter.messagebox as tkm
import maze_maker as mm


def key_down(event):
    global key
    key = event.keysym #練習5


def key_up(event):
    global key
    key = "" #練習6


def main_proc():
    global cx,cy,mx,my
    if key == "Up" and maze_lst[my-1][mx] == 0:
        my -= 1
    elif key == "Down" and maze_lst[my+1][mx] == 0:
        my += 1
    elif key == "Left" and maze_lst[my][mx-1] == 0:
        mx -= 1
    elif key == "Right"and maze_lst[my][mx+1] == 0: #課題12
        mx += 1

    cx = mx * 100 + 50
    cy = my * 100 + 50 #課題11

    canv.coords("tori",cx,cy)
    root.after(100,main_proc) #練習7


if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん") #練習1
    
    canv = tk.Canvas(root,width=1500,height=900,bg="black")
    canv.pack() #練習2

    maze_lst = mm.make_maze(15,9) #練習9
    mm.show_maze(canv,maze_lst) #練習10
    print(maze_lst)

    mx, my = 1,1
    cx = mx * 100 + 50
    cy = my * 100 + 50

    tori = tk.PhotoImage(file="fig/0.png")
    canv.create_image(cx, cy, image=tori, tag="tori") #練習3

   
    key = "" #練習4
    root.bind("<KeyPress>",key_down)

    root.bind("<KeyRelease>",key_up)

    main_proc()
 #   appel = tk.PhotoImage(file="fig/fruit_ringo.png")
 #   canv.create_image(100,100,image=appel, tag="apple")

    root.mainloop()
    