import pandas as pd

df = pd.DataFrame({
    "category": ["A", "A", "A", "B", "B", "B"],
    "sub":      ["x", "x", "y", "x", "y", "y"],
    "value":    [10, 20, 30, 15, 25, 35]
})

result = df.groupby(["category", "sub"])["value"].mean()

print(result)