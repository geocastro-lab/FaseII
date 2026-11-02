from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI(
    title="API de Detección de Fraude Financiero",
    description="Microservicio para la evaluación de transacciones en tiempo real usando XGBoost.",
    version="1.0.0"
)

# Ruta del modelo guardado en la carpeta app
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

try:
    model = joblib.load(MODEL_PATH)
    print("¡Modelo cargado exitosamente en memoria!")
except Exception as e:
    raise RuntimeError(f"No se pudo cargar el archivo model.pkl: {e}")

# Umbral de decisión optimizado obtenido en la validación del modelo
UMBRAL_OPTIMIZADO = 0.7084

class TransactionInput(BaseModel):
    features: list[float]

@app.get("/", tags=["Estado"])
def read_root():
    return {
        "status": "online",
        "service": "Fraud Detection ML API",
        "version": "1.0.0"
    }

@app.post("/predict", tags=["Predicción"])
def predict_fraud(transaction: TransactionInput):
    try:
        if len(transaction.features) != 20:
            raise HTTPException(
                status_code=400, 
                detail=f"Se esperaban 20 características, pero se recibieron {len(transaction.features)}."
            )

        data = np.array(transaction.features).reshape(1, -1)
        probabilities = model.predict_proba(data)
        fraud_probability = float(probabilities[0][1])
        is_fraud = fraud_probability >= UMBRAL_OPTIMIZADO
        
        return {
            "fraud_probability": round(fraud_probability, 4),
            "threshold_applied": UMBRAL_OPTIMIZADO,
            "is_fraud": bool(is_fraud),
            "action_recommended": "BLOQUEAR_TRANSACCION" if is_fraud else "APROBAR_TRANSACCION"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))