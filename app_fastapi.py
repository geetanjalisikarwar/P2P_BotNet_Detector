# app_fastapi.py

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from io import StringIO
from typing import Optional
from detector_core import load_model, clean_dataset, predict_flows

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

# Load model once at startup
MODEL_PATH = "trained_model.pickle"  # or trained_model_converted.pkl
model = load_model(MODEL_PATH)


@app.get("/health")
def health():
    return {"status": "ok", "model_path": MODEL_PATH}


@app.post("/predict-csv")
async def predict_csv(
    file: UploadFile = File(...),
    limit: Optional[int] = Query(100, description="Max malicious flows to return in response"),
):
    """
    Upload a CSV (same schema as training.csv) and get detection results.
    """
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

    # quick stats: top src/dst IPs
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
