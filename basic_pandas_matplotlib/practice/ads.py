import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
plt.rcParams['font.family'] = 'Hiragino Sans'

df = pd.read_csv("../ads.csv")

# 散布図
plt.scatter(df["ad_cost"], df["sales"])
plt.xlabel("Ad Cost")
plt.ylabel("Sales")
plt.title("Ad Cost vs Sales")
plt.show()

# X, y
X = df[["ad_cost"]]
y = df["sales"]

# train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# model
model = LinearRegression()
model.fit(X_train, y_train)

# prediction
y_pred = model.predict(X_test)

print("coef (a):", model.coef_)
print("intercept (b):", model.intercept_)
print("R2:", r2_score(y_test, y_pred))
print("Actual:", list(y_test))
print("Predicted:", list(y_pred))

# 回帰直線
plt.scatter(df["ad_cost"], df["sales"], color="blue")
plt.plot(df["ad_cost"], model.predict(X), color="red")
plt.xlabel("Ad Cost")
plt.ylabel("売上")
plt.title("Regression Line")
plt.show()