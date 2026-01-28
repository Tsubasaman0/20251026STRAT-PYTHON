import csv
import random
from choose_best_plan_v2 import choose_best_plan_v2

OUTPUT_FILE = "trainding_data.csv"

rows = []

for _ in range(200):
    data_gb = round(random.uniform(0, 30), 1) # 0~30GB
    calls_5min = random.randint(0, 50) # 0~50回

    result = choose_best_plan_v2(data_gb, calls_5min)

    # unsuported は除外
    if result.get("status") == "unsupported":
        continue

    label = result["recommended"]

    rows.append([data_gb, calls_5min, label])

# CSV作成
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["data_gb", "calls_5min", "label"])
    writer.writerows(rows)

print(f"{len(rows)} rows saved to {OUTPUT_FILE}")    