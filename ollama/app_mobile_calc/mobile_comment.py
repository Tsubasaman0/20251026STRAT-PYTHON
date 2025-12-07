# mobile_comment.py
from mobile_calc import choose_best_plan

for data_gb, calls in [
    (30, 0),
    (30, 30)
]:

    result = choose_best_plan(data_gb, calls)
    povo = result["povo_cost"]
    linemo = result["linemo_cost"]
    rec = result["recommended"]

    print("povo:", povo)
    print("LINEMO:", linemo)
    print("recommended:", rec)