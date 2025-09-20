from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np
import joblib

app = FastAPI()


class AdmissionData(BaseModel):
    gre: int
    toefl: int
    uni_rating: int
    sop: float
    log: float
    cgpa: float
    research: int


try:
    with open('/app/models/model.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    print("Модель не найдена! Убедитесь, что файл model.pkl существует")
    model = None


@app.post("/predict")
async def predict_admission(data: AdmissionData):
    if model is None:
        return {"error": "Модель не загружена"}

    features = np.array([[data.gre, data.toefl, data.uni_rating,
                          data.sop, data.log, data.cgpa, data.research]])

    scaler = joblib.load("/app/code_models/scaler.save")
    features = scaler.transform(features)

    prediction = model.predict(features)

    return {"prediction": float(prediction[0])}


@app.get("/")
async def root():
    return {"message": "Admission Prediction API"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)