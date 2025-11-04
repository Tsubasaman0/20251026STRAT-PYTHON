# 合計数値を出力するアプリ
n = int(input())
ans = 0
for i in range(n):
    num = int(input())
    ans += num
    print(f"あなたが入力した合計値は{ans}")