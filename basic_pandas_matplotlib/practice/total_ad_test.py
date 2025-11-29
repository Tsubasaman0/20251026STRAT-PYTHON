import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

df = pd.read_csv("ads_multi.csv")

# 総広告費を作る
df["total_ad"] = df["search_ad"] + df["sns_ad"] + df["tv_ad"]

X = df[["total_ad"]]   # 説明変数は総広告費のみ
y = df["sales"]        # 目的変数は売上

# train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
residuals = y_test - y_pred


print("coef (a):", model.coef_)
print("intercept (b):", model.intercept_)
print("R2:", r2_score(y_test, y_pred))
print("Actual:", list(y_test))
print("Predicted:", list(y_pred))

y_pred = model.predict(X_test)
residuals = y_test - y_pred

plt.scatter(y_pred, residuals)
plt.axhline(0, color="red")
plt.title("Residual Plot")
plt.xlabel("Predicted")
plt.ylabel("Residuals")
plt.show()