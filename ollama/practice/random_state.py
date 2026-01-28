import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

X = np.array([1,2,3,4,5,6,7,8,9,10,
              11,12,13,14,15,16,17,18,19,20]).reshape(-1,1)
y = np.array([5,7,9,11,13,15,17,19,21,23,
              25,27,29,31,33,35,37,39,41,80])

def eval_once(random_state, use_outlier=True):
    if use_outlier:
        X_use, y_use = X, y
    else:
        X_use, y_use = X[:-1], y[:-1]  # (20,80)削除

    X_train, X_test, y_train, y_test = train_test_split(
        X_use, y_use, test_size=0.2, random_state=random_state
    )
    model = LinearRegression().fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return r2_score(y_test, y_pred)

for rs in [1, 42, 99, 123]:
    print("rs =", rs,
          " with outlier:", eval_once(rs, True),
          " without outlier:", eval_once(rs, False))