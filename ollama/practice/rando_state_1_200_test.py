from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import numpy as np

X = np.array([[i] for i in range(1, 21)])
y = np.array([i * 2 + 3 for i in range(1, 20)] + [90])  # 外れ値1個

for seed in [1, 10, 20, 42, 99]:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)
    model = LinearRegression().fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(seed, "-> R2:", r2_score(y_test, y_pred))

scores = []
for seed in range(1, 200):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)
    model = LinearRegression().fit(X_train, y_train)
    y_pred = model.predict(X_test)
    scores.append(r2_score(y_test, y_pred))

print("min_score: ", min(scores))
print("max_score:", max(scores))
print("np.mean:", np.mean(scores))
print("np.std: ", np.std(scores))