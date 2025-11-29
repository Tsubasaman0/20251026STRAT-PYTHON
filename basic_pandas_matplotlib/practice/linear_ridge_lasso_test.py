import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt 

# === データ読み込み ===
df = pd.read_csv("ads_multi.csv")
df["sum_ad"] = df["search_ad"] + df["sns_ad"]

X = df[["sum_ad", "tv_ad"]]
y = df["sales"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ====== 1. 通常線形回帰 ======
lr = LinearRegression()
lr.fit(X_train, y_train)
lr_pred = lr.predict(X_test)

print("\n=== LinearRegression ===")
print("coef:", lr.coef_)
print("intercept:", lr.intercept_)
print("R2:", r2_score(y_test, lr_pred))


# ====== 2. Ridge ======
ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)
ridge_pred = ridge.predict(X_test)

print("\n=== Ridge Regression ===")
print("coef:", ridge.coef_)
print("intercept:", ridge.intercept_)
print("R2:", r2_score(y_test, ridge_pred))


# ====== 3. Lasso ======
lasso = Lasso(alpha=1.0)
lasso.fit(X_train, y_train)
lasso_pred = lasso.predict(X_test)

print("\n=== Lasso Regression ===")
print("coef:", lasso.coef_)
print("intercept:", lasso.intercept_)
print("R2:", r2_score(y_test, lasso_pred))
print(df[["sum_ad", "tv_ad"]].corr())

plt.scatter(lr.predict(X), y -lr.predict(X))
plt.axhline(0, color="red")
plt.title("Residuals Plot")
plt.xlabel("Predict")
plt.ylabel("Residuals")
plt.show()