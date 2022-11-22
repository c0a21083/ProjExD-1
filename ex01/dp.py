import random
import datetime

def sagasu(a):
    for i in range(2):
        e = random.choice(c)
        d.append(e)
        c.remove(d[i])
    return c

a = ["A","B","C","D","E","F","G","H","I","J",
"K","L","M","N","O","P","Q","R",
    "S","T","U","V","W","X","Y","Z"]
b = [i for i in range(len(a))]
c = random.sample(a, random.choice(b))
d = []

print(f"対称文字 :{c}")
sagasu(a)
print(f"欠損文字{d}")
print(f"表示文字:{c}")

input_a = int(input("欠損文字はいくつあるでしょうか？"))

while(True):
    if input_a == len(d):
        print("正解です. それでは、具体的に欠損文字数を1つずつ入力してください")
        input_b = input("1つ目の文字を入力してください:")
        input_c = input("2つ目の文字を入力してください:")
        if input_b == d[0] and input_c == d[1]:
            print("正解です！")
            break
        else:
            print("不正解です. またチャレンジしてください")

    












