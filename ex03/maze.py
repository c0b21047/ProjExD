import tkinter as tk
import tkinter.messagebox as tkm
import maze_maker as mm
import random
import datetime

def key_down(event):
    global key
    key = event.keysym #練習5


def key_up(event):
    global key,st
    key = "" #練習6
    if st == 0:
        st = datetime.datetime.now()

def main_proc():
    global cx,cy,mx,my,game
    if key == "Up" and maze_lst[my-1][mx] != 1:
        my -= 1
    elif key == "Down" and maze_lst[my+1][mx] != 1:
        my += 1
    elif key == "Left" and maze_lst[my][mx-1] != 1:
        mx -= 1
    elif key == "Right"and maze_lst[my][mx+1] != 1: #課題12
        mx += 1

    cx = mx * 100 + 50
    cy = my * 100 + 50 #課題11

    if maze_lst[my][mx] == 2:
        canv.coords("tori",cx-25,cy)
        canv.coords("goal",cx+25,cy)
        ed = datetime.datetime.now()
        time(ed)
    else:
        canv.coords("tori",cx,cy)
    nowtime = datetime.datetime.now()
    label["text"] = f"{(nowtime-st).seconds}秒"
    game = root.after(100,main_proc) #練習7


def set_goal():
    global maze_lst,gx,gy
    while True:
        gx = random.randint(1,14)
        gy = random.randint(1,8)
        print(gx,gy)
        if maze_lst[gy][gx] == 0:
            a = gx * 100 + 50
            b = gy * 100 + 50
            canv.coords("goal",a,b)
            maze_lst[gy][gx] = 2
            return True

def time(ed):
    global maze_lst
    score = ed - st
    root.after_cancel(a)
    root.after_cancel(game)
    maze_lst[my][mx] = 3
    tkm.showinfo("結果",f"記録：{score.seconds}秒")


def escp_proc():
    global gx,gy,a,maze_lst,speed
    sub = random.randint(0,5)
    if sub == 1 and maze_lst[gy-1][gx] != 1:
        maze_lst[gy][gx] = 0
        gy -= 1
        maze_lst[gy][gx] = 2 
    elif sub == 2 and maze_lst[gy+1][gx] != 1:
        maze_lst[gy][gx] = 0
        gy += 1
        maze_lst[gy][gx] = 2
    elif sub == 3 and maze_lst[gy][gx-1] != 1:
        maze_lst[gy][gx] = 0
        gx -= 1
        maze_lst[gy][gx] = 2
    elif sub == 4 and maze_lst[gy][gx+1] != 1: 
        maze_lst[gy][gx] = 0
        gx += 1
        maze_lst[gy][gx] = 2
            
    tx = gx * 100 + 50
    ty = gy * 100 + 50 
    
    canv.coords("goal",tx,ty)

    a = root.after(speed,escp_proc)


if __name__ == "__main__":
    st = datetime.datetime.now()
    game,a= None, None
    root = tk.Tk()
    root.title("迷えるこうかとん") #練習1

    label = tk.Label(root,text="",font=("",20))
    label.pack()

    canv = tk.Canvas(root,width=1500,height=900,bg="black")
    canv.pack() #練習2

    maze_lst = mm.make_maze(15,9) #練習9
    mm.show_maze(canv,maze_lst) #練習10
    print(maze_lst)

    mx, my = 1,1
    cx = mx * 100 + 50
    cy = my * 100 + 50

    gx,gy = 0,0

    speed = 500

    tori = tk.PhotoImage(file="fig/0.png")
    canv.create_image(cx, cy, image=tori, tag="tori") #練習3

    goal = tk.PhotoImage(file="fig/8.png")
    canv.create_image(0,0,image=goal, tag="goal")

    set_goal()
    
    key = "" #練習4
    root.bind("<KeyPress>",key_down)

    root.bind("<KeyRelease>",key_up)

    main_proc()
    escp_proc()

    root.mainloop()
    