# trainding_best_plan.py
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, classification_report

# === Path設定 ===
data_path = Path('csv/trainding_data.csv')

# === CSV読み込み ===
df = pd.read_csv(data_path)

# === labelを0,1に変換 ===
df["label_num"] = df["label"].map({
    "povo": 0,
    "LINEMO": 1
})

# === X, y ===
X = df[["data_gb", "calls_5min"]]
y = df["label_num"]

# === train_test_split ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# === model作成 ===
model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

# === 学習データ表示 ===
print("accuracy:", acc)
print("test_size:", len(y_test))
print("pred counts:", pd.Series(y_pred).value_counts().to_dict())
print("true counts:", pd.Series(y_test).value_counts().to_dict())
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=["povo", "LINEMO"]))
print("coef:", model.coef_)
print("intercept:", model.intercept_)
print("features:", X.columns.tolist())

result_df = X_test.copy()
result_df["true_label"] = y_test.values
result_df["pred_label"] = y_pred
print(result_df)

label_map = {0: "povo", 1: "LINEMO"}
result_df["true_label"] = result_df["true_label"].map(label_map)
result_df["pred_label"] = result_df["pred_label"].map(label_map)

misclassified = result_df[result_df["true_label"] != result_df["pred_label"]]

print(misclassified)