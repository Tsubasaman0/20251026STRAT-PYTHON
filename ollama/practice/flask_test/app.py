# app.py
from flask import Flask, render_template, request
from choose_best_plan_v2 import choose_best_plan_v2

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    
    if request.method == "POST":
        try:
            data_gb = float(request.form.get("data_gb", "0"))
            calls_5min = int(request.form.get("calls_5min", "0"))

            if data_gb < 0:
                raise ValueError("マイナスは不可")

            result = choose_best_plan_v2(data_gb, calls_5min)
            print("ここは処理できてる")
        
        except ValueError:
            error = "数値を正しく入力してください"
        except Exception:
            error = "予期せぬエラーが発生しました。入力値を見直してください"

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)