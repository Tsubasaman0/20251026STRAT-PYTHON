import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# csv読み込み
df = pd.read_csv("ads_multi.csv")

# X,y
X = df[["search_ad", "tv_ad"]]
y = df["sales"]

# train/test 分割
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# モデル作成
model = LinearRegression()
model.fit(X_train, y_train)

# 予測
y_pred = model.predict(X_test)

# 結果
print("coef_:", model.coef_)
print("intercept:", model.intercept_)
print("R2:", r2_score(y_test, y_pred))
print("y_test:", y_test)
print("y_pred:", y_pred)