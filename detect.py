# detect.py

import sys
from detector_core import detect_from_csv

USAGE = "Usage: python detect.py <path_to_csv> [model_path]"

if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print(USAGE)
        sys.exit(1)

    csv_path = sys.argv[1]
    model_path = sys.argv[2] if len(sys.argv) == 3 else "trained_model.pickle"

    summary = detect_from_csv(csv_path, model_path=model_path)

    print(f"[+] Total flows:      {summary['total_flows']}")
    print(f"[+] Malicious flows:  {summary['malicious_flows']}")
    print(f"[+] Malicious ratio:  {summary['malicious_ratio']:.4f}")
    print(f"[+] Text output:      {summary['txt_output_path']}")
    if summary["malicious_csv_path"]:
        print(f"[+] Malicious CSV:    {summary['malicious_csv_path']}")
