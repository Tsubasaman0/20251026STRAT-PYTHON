import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

df = pd.read_csv("../ads.csv")

X = df[["ad_cost"]]
y = df["sales"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# --- 残差の計算 ---
residuals = y_test - y_pred

print("=== Residuals ===")
print(list(residuals))

# --- 残差プロット ---
plt.scatter(y_pred, residuals, color="red")
plt.axhline(0, color="black", linestyle="--")
plt.xlabel("Predicted")
plt.ylabel("Residuals")
plt.title("Residual Plot")
plt.show()