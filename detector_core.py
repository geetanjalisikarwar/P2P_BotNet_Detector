# detector_core.py

import os
import pandas as pd
import numpy as np
import pickle
from typing import Tuple, List, Dict


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Replace NaN/Inf and cast to float (model-friendly)."""
    df = df.replace([np.nan, np.inf, -np.inf], 0)
    return df.astype(float)


def load_model(model_path: str = "trained_model.pickle"):
    """Load the sklearn model from pickle."""
    model_path = os.path.abspath(model_path)
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at: {model_path}")
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model


def predict_flows(df: pd.DataFrame, model) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Given full dataframe with columns:
    [src_ip, src_port, dst_ip, dst_port, protocol, feature_1, ..., label]
    return:
      flows_df: first 5 cols (identifiers)
      preds: predicted labels (0/1)
    """
    if df.shape[1] < 7:
        raise ValueError("Dataframe must contain at least 7 columns (5 id + features + label).")

    flows = df.iloc[:, 0:5]      # src_ip, src_port, dst_ip, dst_port, protocol
    features = clean_dataset(df.iloc[:, 5:-1])  # all between id cols and label

    preds = model.predict(features)
    return flows, preds


def detect_from_csv(
    csv_path: str,
    model_path: str = "trained_model.pickle",
    output_in_same_dir: bool = True,
    save_malicious_csv: bool = True,
) -> Dict:
    """
    Run detection on a CSV file and optionally write outputs next to it.
    Returns a summary dict.
    """
    csv_path = os.path.abspath(csv_path)
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found at: {csv_path}")

    base_dir = os.path.dirname(csv_path)
    file_stem = os.path.splitext(os.path.basename(csv_path))[0]

    output_dir = base_dir if output_in_same_dir else os.getcwd()
    os.makedirs(output_dir, exist_ok=True)

    txt_output_path = os.path.join(output_dir, f"{file_stem}_output.txt")
    mal_csv_path = os.path.join(output_dir, f"{file_stem}_malicious_flows.csv")

    # Load data + model
    df = pd.read_csv(csv_path)
    model = load_model(model_path)

    flows, preds = predict_flows(df, model)

    malicious_mask = preds == 1
    malicious_flows = flows[malicious_mask]

    # Write human-readable txt
    with open(txt_output_path, "w") as out:
        total = len(df)
        mal_count = malicious_flows.shape[0]
        ratio = mal_count / total if total > 0 else 0

        if mal_count == 0:
            out.write("No Botnet Activity Detected\n")
        else:
            out.write("---------- BOTNET FLOWS DETECTED ----------\n\n")
            out.write(f"Total flows: {total}\n")
            out.write(f"Malicious flows: {mal_count}\n")
            out.write(f"Malicious ratio: {ratio:.4f}\n\n")

            for _, row in malicious_flows.iterrows():
                src, sport, dst, dport, proto = row
                out.write(f"{src}:{sport} -> {dst}:{dport} ({proto})\n")

    # Optional CSV of malicious flows
    if save_malicious_csv and not malicious_flows.empty:
        malicious_flows.to_csv(mal_csv_path, index=False)

    summary = {
        "total_flows": int(len(df)),
        "malicious_flows": int(malicious_flows.shape[0]),
        "malicious_ratio": float(
            malicious_flows.shape[0] / len(df) if len(df) > 0 else 0
        ),
        "txt_output_path": txt_output_path,
        "malicious_csv_path": mal_csv_path if save_malicious_csv else None,
        "sample_malicious_flows": malicious_flows.head(50).to_dict(orient="records"),
    }

    return summary
