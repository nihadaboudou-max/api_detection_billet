from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware # pyright: ignore[reportMissingImports]
import pandas as pd
import joblib
import io
import os
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # autorise toutes les origines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model_rforest.sav")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.sav")

# Chargement des objets au démarrage
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

@app.get("/")
def bienvenu():
    return {"message": "Bienvenue sur l'API de prédiction de faux billets"}

@app.post("/predict")
async def fichier_csv(file: UploadFile = File(...), separateur: str = Form(...)):
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content), sep=separateur)  # lecture avec séparateur 

    if 'margin_low' in df.columns:
        df['margin_low'].fillna(df['margin_low'].median(), inplace=True)
    else:
        raise HTTPException(status_code=400, detail="Colonne 'margin_low' manquante dans le CSV")

    # Appliquer le scaler correctement
    X_scaled = df 
    scaler.transform(X_scaled)

    # Faire la prédiction avec le modèle chargé
    prediction = model.predict(X_scaled)
    proba = model.predict_proba(X_scaled)
    
    # Retourner le résultat
    result_pred=[]
    tab_proba=[]
    for i in range(len(prediction)):
        result_pred.append(int(prediction[i]))
        tab_proba.append(float(proba[i][1]))
    
    df_predict=df.copy()
    df["prediction"]= result_pred
    df["probabilite"]= tab_proba
    

    return {"resultat": df[["prediction","probabilite"]].to_dict(orient="records")}

