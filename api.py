import os
import uuid
import pickle
import pandas as pd
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

# -------------------------------
# Load Model at Startup
# -------------------------------
MODEL_PATH = "trained_model.pkl"

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print("[✓] Model loaded successfully")
except Exception as e:
    print("[X] Failed to load model:", e)
    model = None

# -------------------------------
# FastAPI App
# -------------------------------
app = FastAPI(
    title="P2P Botnet Detection API",
    description="Upload CSV → Get botnet detection results",
    version="2.0"
)

# -------------------------------
# Cleaning Function
# -------------------------------
def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.replace([np.inf, -np.inf, np.nan], 0)
    return df.astype(float)

# -------------------------------
# Detection Logic
# -------------------------------
def run_detection(csv_path: str):

    df = pd.read_csv(csv_path)

    # Extract features (all columns except first 5 metadata + last label)
    feature_cols = df.columns[5:-1]
    flow_cols = df.columns[0:5]

    features = clean_dataset(df[feature_cols])
    flows = df[flow_cols]

    predictions = model.predict(features)

    malicious = []
    for idx, label in enumerate(predictions):
        if label == 1:
            malicious.append(list(flows.iloc[idx]))

    return malicious


# -------------------------------
# API Endpoint: /detect
# -------------------------------
@app.post("/detect")
async def detect_botnet(file: UploadFile = File(...)):
    """
    Upload training-style CSV → returns malicious flows + downloads output file.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Upload a valid CSV file")

    # Save uploaded file to disk
    unique_id = uuid.uuid4().hex
    temp_csv_path = f"uploaded_{unique_id}.csv"
    output_path = f"botnet_output_{unique_id}.txt"

    with open(temp_csv_path, "wb") as f:
        f.write(await file.read())

    # Run detection
    malicious_flows = run_detection(temp_csv_path)

    # Write results
    with open(output_path, "w") as out:
        if len(malicious_flows) == 0:
            out.write("No Botnets Detected\n")
        else:
            out.write("----- Malicious Botnet Flows -----\n")
            for f in malicious_flows:
                out.write(f"{f[0]}:{f[1]} -> {f[2]}:{f[3]} ; {f[4]}\n")

    # Return output file
    return FileResponse(
        path=output_path,
        filename="botnet_output.txt",
        media_type="text/plain"
    )


# -------------------------------
# Health Check
# -------------------------------
@app.get("/")
def root():
    return {"status": "ok", "message": "Botnet Detection API is running"}
