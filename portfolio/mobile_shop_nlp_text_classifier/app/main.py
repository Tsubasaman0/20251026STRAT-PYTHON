# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from src.config import MODEL_FAQ_PATH

app = FastAPI()
model = None # なぜここでNoneのmodelを作る

class PredictRequest(BaseModel): # ここでクラ作る意味は?
    text: str # テキストをstrで読みこむ?どういうこと

@app.on_event("startup")
def load_model():
    global model # なぜglobalにする? 
    model = joblib.load(MODEL_FAQ_PATH)

@app.get("/")
def root():
    return {"message" : "ok"}

@app.get("/health")
def health():
    return { "status" : "ok"}

@app.post("/predict")
def predict(req: PredictRequest): # 全体的になにしているかわからない
    label = model.predict([req.text])[0]

    confidence = None
    # 確信度（predict_probaがあるモデルの場合）
    proba = None
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba([req.text])[0]
        confidence = float(proba.max())

    return {"label" : label, "confidence" : confidence}