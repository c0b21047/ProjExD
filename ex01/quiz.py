import random

def shutudai():
    q ={"サザエの旦那の名前は？":["マスオ","ますお"], \
        "カツオの妹の名前は？":["ワカメ","わかめ"], \
        "タラオはカツオから見てどんな関係？":["甥","おい","甥っ子","おいっこ"]}
    Q = random.choice(list(q.keys()))
    print(Q)
    return q[Q]

def kaito(ans):
    user_ans = input("答えるんだ：")
    if user_ans in ans:
        print("正解！！！")
    else:
        print("出直してこい")

print("問題：")
kaito(shutudai())