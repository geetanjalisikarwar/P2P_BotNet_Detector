# convert_model.py

import pickle
import os

OLD_MODEL = "trained_model.pickle"
NEW_MODEL = "trained_model_converted.pkl"


def convert_model(old_path=OLD_MODEL, new_path=NEW_MODEL):
    old_path = os.path.abspath(old_path)
    new_path = os.path.abspath(new_path)

    if not os.path.exists(old_path):
        raise FileNotFoundError(f"Old model not found at: {old_path}")

    print(f"[+] Loading old model from: {old_path}")
    with open(old_path, "rb") as f:
        model = pickle.load(f)

    print(f"[+] Saving converted model to: {new_path}")
    with open(new_path, "wb") as f:
        pickle.dump(model, f)

    print("[✓] Conversion complete.")


if __name__ == "__main__":
    convert_model()
