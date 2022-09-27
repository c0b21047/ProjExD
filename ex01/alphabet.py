import random
import datetime

alphabet_lst = [chr(i) for i in range(65,91)]
loop_n = 3
chr_n = 10
del_n = 2

def shutudai():
    print("対象文字：")
    q =random.sample(alphabet_lst,chr_n)
    print(" ".join(q))
    return q

def del_alp(q,test=False):
    sub = []
    for i in range(del_n):
        a = random.choice(q)
        q.remove(a)
        sub.append(a)
    if test:
        print("欠損文字：")
        print(" ".join(sub))
    print("表示文字：")
    print(" ".join(q))
    return sub

def ans(a):
    user_ans1 = input("欠損文字はいくつあるでしょうか？：")
    if int(user_ans1) != del_n:
        return False
    else:
        print("正解です。それでは、具体的に欠損文字を１つずつ入力してください")
        user_ans2 = input("1つ目の文字を入力してください：")
        user_ans3 = input("2つ目の文字を入力してください：")
        if user_ans2 in a and user_ans3 in a and user_ans2 != user_ans3:
            return True
        else:
            return False

if __name__ == "__main__":
    st = datetime.datetime.now()
    print(loop_n,"回挑戦できます")
    for i in range(1,loop_n+1):
        print(i,"回目の挑戦です")
        q = shutudai()
        a = del_alp(q)
        if ans(a):
            print("正解です！！！")
            ed = datetime.datetime.now()
            print("かかった時間は",(ed-st).seconds,"秒です。")
            break
        else:
            print("不正解です。またチャレンジしてください")
            print("-"*40)
