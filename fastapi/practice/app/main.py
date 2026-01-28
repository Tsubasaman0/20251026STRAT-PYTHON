from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from src.config import MODEL_FAQ_PATH

app = FastAPI()
model = None

class PredictRequest(BaseModel):
    text: str

@app.on_event("startup")
def load_model():
    global model
    model.joblib.load(MODEL_FAQ_PATH)

@app.get("/")
def root():
    return {"message" : "ok"}

@app.get("/health")
def health():
    return { "status" : "ok"}