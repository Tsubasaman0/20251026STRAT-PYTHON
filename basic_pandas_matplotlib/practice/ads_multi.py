import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

df = pd.read_csv("ads_multi.csv")

# X (説明変数) は3つ
X = df[["search_ad", "sns_ad", "tv_ad"]]
y = df["sales"]

# train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# モデル
model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)




#vifチェック表
from statsmodels.stats.outliers_influence import variance_inflation_factor

X = df[["search_ad","sns_ad","tv_ad"]]

vif_data = pd.DataFrame()
vif_data["feature"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

print(vif_data)