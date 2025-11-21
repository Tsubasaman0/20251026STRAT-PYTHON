import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

# データの読み込み
df = pd.read_csv("ads.csv")

# x, y  に分ける
X = df[["ad_cost"]]
y = df["sales"]

# モデル作成＆学習（全データで）
model = LinearRegression()
model.fit(X, y)

print("coef: (a):", model.coef_[0])
print("intercept (b):", model.intercept_)

for cost in [1,5,14,50,72]:
    x_new = pd.DataFrame({"ad_cost": [cost]})
    pred = model.predict(x_new)
    print(f"ad_cost={cost}, predicted_sales={pred[0]:.2}")
    
r2 = r2_score(y, model.predict(X))
print(f"r2_score: {r2:.2}")

a = model.coef_[0]
b = model.intercept_

x_line = np.linspace(0, 60, 100)
y_line = a * x_line + b

plt.scatter(df["ad_cost"], df["sales"], label="Actual Data", color="blue")
plt.plot(x_line, y_line, color="red", label="Regression Line")
plt.show()



# つまり y = ax * b は　「売上高(y)　＝　広告宣伝効果(a)　＊　広告宣伝費(x)　＋　ベース売上高(b)」　 