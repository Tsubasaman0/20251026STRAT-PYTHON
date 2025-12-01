import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from statsmodels.stats.outliers_influence import variance_inflation_factor
import numpy as np

# ====== CSV 読み込み ======
df = pd.read_csv("practice/ads_multi.csv")

# ====== 広告費のトータル算出 =====
df["sum_ad"] = df["search_ad"] + df["sns_ad"] + df["tv_ad"]

# X, y
X = df[["sum_ad"]]
y = df["sales"]

# ====== train/test 分割 ======
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ====== モデル作成 ======
model = LinearRegression()
model.fit(X_train, y_train)

# ====== 予測 ======
y_pred = model.predict(X_test)

# ====== R2 ======
print("coef:", model.coef_)
print("intercept:", model.intercept_)
print("R2:", r2_score(y_test, y_pred))
print("Actual:", list(y_test.values))
print("Predicted:", list(y_pred))

# ====== 残差 ======
residuals = y_test - y_pred
print("\n=== Residuals ===")
print(list(residuals))

# ====== 残差プロット ======
plt.figure(figsize=(6,4))
plt.scatter(y_pred, residuals)
plt.axhline(0, color="red", linewidth=1)
plt.title("Residual Plot")
plt.xlabel("Predicted")
plt.ylabel("Residuals")
plt.tight_layout()
plt.show()

# ====== VIF 計算 ======
# vif_df = pd.DataFrame()
# vif_df["feature"] = X.columns
# vif_df["VIF"] = [
#     variance_inflation_factor(X.values, i) for i in range(X.shape[1])
# ]

# print("\n=== VIF ===")
# print(vif_df)

# import matplotlib.pyplot as plt

# coef = model.coef_
# features = X.columns

# plt.figure(figsize=(6,4))
# plt.bar(features, coef)
# plt.axhline(0, color="black", linewidth=1)
# plt.title("Feature Importance (Coefficients)")
# plt.ylabel("Coefficient Value")
# plt.tight_layout()
# plt.show()

# print("\n=== Corraelation Matrix ===")
# print(df.corr(numeric_only=True))

# ===== 回帰直線の可視化 =====
plt.figure(figsize=(6,4))
plt.scatter(X, y, label="data")
x_line = pd.DataFrame({"sum_ad": range(int(X.min()), int(X.max())+1)})
y_line = model.predict(x_line)
plt.plot(x_line, y_line, color="red", label="regression line")
plt.xlabel("sum_ad")
plt.ylabel("sales")
plt.title("sum_ad vs sales")
plt.legend()
plt.tight_layout()
plt.show()