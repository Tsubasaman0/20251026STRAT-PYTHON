import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# ads.csv を読み込む
df_ads =pd.read_csv("ads.csv")

# x, y
X = df_ads[["ad_cost"]]
y = df_ads["sales"]

# モデル学習
model = LinearRegression()
model.fit(X, y)


# a, b を取得
a = model.coef_[0]
b = model.intercept_

print("a: (coef_):", a)
print("b: (intercept_):", b)

# 直線の点を作る
x_line = np.linspace(df_ads["ad_cost"].min(), df_ads["ad_cost"].max(), 100)
y_line = a * x_line + b

# グラフ
plt.scatter(df_ads["ad_cost"], df_ads["sales"], label="data")
plt.plot(x_line, y_line, label="y = ax + b")
plt.legend()
plt.title("Regression line and intercept")
plt.xlabel("ad_cost")
plt.ylabel("sales")
plt.savefig("intercept.png")
plt.show()