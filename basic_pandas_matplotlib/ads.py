import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# csvの読み込み
df = pd.read_csv("ads.csv")

# X, yに分ける
X = df[["ad_cost"]]
y = df["sales"]

# train/test 分割
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 理解するためのプリント
print("---df---")
print(df)

print("---X---")
print(X)

print("---y---")
print(y)

print("---X_train---")
print(X_train)

print("---X_test---")
print(X_test)

model = LinearRegression()
model.fit(X_train, y_train)

# 予測
y_pred = model.predict(X_test)

#print("予測：", y_pred)
#print("実測：", y_test.values)

# グラフの作成
plt.figure(figsize=(8,5))
plt.scatter(X_test, y_test, color="blue", label="Actual")
plt.scatter(X_test, y_pred, color="red", label="Predicted")

plt.title("Actual vs Predicted Sales")
plt.xlabel("Ad Cost")
plt.ylabel("Sales")
plt.legend()
plt.tight_layout()
plt.savefig("ads.png")
