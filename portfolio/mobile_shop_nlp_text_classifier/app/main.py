# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
import joblib
from src.config import MODEL_FAQ_PATH


app = FastAPI(title="Mobile Shop FAQ Classifier", version="1.0.0")
model = None 

class PredictRequest(BaseModel):
    text: str = Field(..., min_length=2, description="問い合わせしたい文")

class Candidate(BaseModel):
    label: str
    proba: float

class PredictResponse(BaseModel):
    label: str
    confidence: Optional[float]
    needs_review: bool
    candidates: Optional[list[Candidate]] = None

@app.on_event("startup")
def load_model():
    global model # なぜglobalにする? 
    model = joblib.load(MODEL_FAQ_PATH)

@app.get("/health")
def health():
    return { "status" : "ok", "model_loaded": model is not None}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded")
    
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is empty")
    
    label = model.predict([req.text])[0]

    confidence = None
    needs_review = True
    candidates = None

    if hasattr(model, "predict_proba"):
        proba = model.predict_proba([req.text])[0]
        confidence = float(proba.max())
        needs_review = confidence < 0.65

        # 上位候補 top3 を返す
        labels = list(model.classes_)
        pairs = sorted(zip(labels, proba), key=lambda x: x[1], reverse=True)[:3]
        candidates = [{"label": l, "proba": float(p)} for l, p in pairs]

    return PredictResponse(
        label=label,
        confidence=confidence,
        needs_review=needs_review,
        candidates=candidates)