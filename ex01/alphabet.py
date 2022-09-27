import random
import datetime

alphabet_lst = [chr(i) for i in range(65,91)] #アルファベットのリスト
loop_n = 3 #挑戦回数
chr_n = 10 #対象文字数
del_n = 2 #欠損文字数

def shutudai(): #対象文字の表示
    print("対象文字：")
    q =random.sample(alphabet_lst,chr_n)
    print(" ".join(q))
    return q

def del_alp(q,test=False): #対象文字から欠損文字を削除 test=Trueで欠損文字表示
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

def ans(a): #回答確認 返り値がTrueで正解、Falseで不正解
    user_ans1 = input("欠損文字はいくつあるでしょうか？：")
    if int(user_ans1) != del_n: #欠損文字数は正しいか
        return False
    else:
        print("正解です。それでは、具体的に欠損文字を１つずつ入力してください")
        user_ans2 = input("1つ目の文字を入力してください：")
        user_ans3 = input("2つ目の文字を入力してください：")
        if user_ans2 in a and user_ans3 in a and user_ans2 != user_ans3: #欠損文字は正しいか
            return True
        else:
            return False


if __name__ == "__main__": #main関数
    st = datetime.datetime.now() #計測開始
    print(loop_n,"回挑戦できます")
    for i in range(1,loop_n+1): #挑戦可能回数分だけ繰り返す
        print(i,"回目の挑戦です")
        q = shutudai()
        a = del_alp(q)
        if ans(a): #回答が正しかったか
            print("正解です！！！")
            ed = datetime.datetime.now() #計測終了
            print("かかった時間は",(ed-st).seconds,"秒です。") #かかった時間を表示 
            break
        else:
            print("不正解です。またチャレンジしてください")
            print("-"*40) #回の切れ目