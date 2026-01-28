import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

np.random.seed(42)

# 身長 150〜180 の範囲で 100 個
height = np.linspace(150, 180, 100)

# 完全線形 + ノイズ
# 体重 = 0.75 * 身長 - 50 + ノイズ
noise = np.random.normal(0, 1.5, size=100)  # ±1.5kg 程度
weight = 0.75 * height - 50 + noise

df = pd.DataFrame({
    "height_cm": height,
    "weight_kg": weight
})




X = df[["height_cm"]]
y = df["weight_kg"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression().fit(X_train, y_train)
y_pred = model.predict(X_test)
