# app.py
from flask import Flask, render_template, request
from mobile_calc import choose_best_plan

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        try:
            data_gb = float(request.form.get("data_gb", "0"))
            calls_5min = int(request.form.get("calls_5min", "0"))

            # ここでバリデーション
            if data_gb < 0 or calls_5min < 0:
                raise ValueError("マイナスは不可")

            result = choose_best_plan(data_gb, calls_5min)

        except ValueError:
            error = "数値を正しく入力してください。(マイナスは不可)"
        except Exception:
            error = "予期せぬエラーが発生しました。入力値を見直してください。"

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True)