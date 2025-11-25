# app_fastapi.py

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from io import StringIO
from typing import Optional
from detector_core import load_model, clean_dataset, predict_flows
from fastapi.responses import FileResponse
import os

app = FastAPI(
    title="P2P Botnet Detector API",
    description="FastAPI backend for CSV-based botnet flow detection.",
    version="1.0.0",
)

# CORS (optional – for Streamlit or web frontends)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock down in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model stored on API server
MODEL_PATH = "trained_model.pickle"
model = None

def load_model_if_exists():
    global model
    if os.path.exists(MODEL_PATH):
        try:
            model = load_model(MODEL_PATH)
            return True
        except Exception:
            model = None
            return False
    model = None
    return False

# Attempt to load at startup if file present
_load_ok = load_model_if_exists()


@app.get("/health")
def health():
    return {"status": "ok", "model_path": MODEL_PATH, "model_loaded": model is not None}


@app.post("/upload-model")
async def upload_model(file: UploadFile = File(...)):
    """
    Upload a model pickle (.pkl/.pickle) to the server and load it.
    """
    if not (file.filename.endswith(".pkl") or file.filename.endswith(".pickle")):
        raise HTTPException(status_code=400, detail="Only .pkl or .pickle files are supported.")

    content = await file.read()
    try:
        with open(MODEL_PATH, "wb") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save model file: {e}")

    ok = load_model_if_exists()
    if not ok:
        try:
            os.remove(MODEL_PATH)
        except Exception:
            pass
        raise HTTPException(status_code=500, detail="Model saved but failed to load on server.")

    return {"detail": "Model uploaded and loaded successfully.", "model_path": MODEL_PATH}


@app.get("/download-model")
def download_model():
    if not os.path.exists(MODEL_PATH):
        raise HTTPException(status_code=404, detail="Model file not found on server.")
    return FileResponse(MODEL_PATH, media_type="application/octet-stream", filename=os.path.basename(MODEL_PATH))


@app.post("/predict-csv")
async def predict_csv(
    file: UploadFile = File(...),
    limit: Optional[int] = Query(100, description="Max malicious flows to return in response"),
):
    """
    Upload a CSV (same schema as training.csv) and get detection results.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded on server. Upload a model via /upload-model.")

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    content = await file.read()
    try:
        df = pd.read_csv(StringIO(content.decode("utf-8")))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {e}")

    if df.empty:
        raise HTTPException(status_code=400, detail="Empty CSV.")

    flows, preds = predict_flows(df, model)
    malicious_mask = preds == 1
    malicious_flows = flows[malicious_mask]

    total = int(len(df))
    mal_count = int(malicious_flows.shape[0])
    ratio = float(mal_count / total) if total > 0 else 0.0

    result_rows = malicious_flows.head(limit).to_dict(orient="records")

    top_sources = (
        malicious_flows["src_ip"].value_counts().head(10).to_dict()
        if mal_count > 0 else {}
    )
    top_dests = (
        malicious_flows["dst_ip"].value_counts().head(10).to_dict()
        if mal_count > 0 else {}
    )

    return {
        "total_flows": total,
        "malicious_flows": mal_count,
        "malicious_ratio": ratio,
        "returned_flows": len(result_rows),
        "malicious_sample": result_rows,
        "top_source_ips": top_sources,
        "top_destination_ips": top_dests,
    }
