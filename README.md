# 🕸️ P2P Botnet Detection System  
A modern, modular system for detecting Peer-to-Peer botnets using machine learning on pre-extracted network flow features.

This upgraded version replaces the legacy PCAP-based workflow with a **clean CSV-based inference pipeline**, a **FastAPI backend**, and a **production-ready Streamlit UI**.

---

## 🚀 Features (New System)

### ✔ ML-Powered Botnet Detection  
Uses a pre-trained BaggingClassifier model (`trained_model.pickle`) to classify malicious network flows.

### ✔ CSV-Based Workflow  
Instead of parsing PCAP files (slow, heavy), the system works with flow-level feature CSVs (like `training.csv`).

### ✔ FastAPI Backend  
Provides clean REST APIs for:

- Uploading CSV  
- Running predictions  
- Downloading malicious-flow reports  

### ✔ Streamlit UI  
Interactive dashboard with:

- CSV uploader  
- Real-time detection  
- Summary statistics  
- Malicious flow explorer  
- Downloadable results  

### ✔ Modular & Extensible  
Core ML logic separated into `detector_core.py`, backend in `app_fastapi.py`, UI in `app_streamlit.py`.

---

## 📁 Project Structure

```text
P2P-BOTNET-DETECTOR/
│
├── app_fastapi.py            # FastAPI backend
├── app_streamlit.py          # Streamlit UI
├── detector_core.py          # Core ML detection pipeline
├── detect.py                 # CLI tool for detection
├── convert_model.py          # Optional: fixes old sklearn pickles
│
├── trained_model.pickle      # Pretrained classifier
├── training.csv              # Dataset used for training/testing
├── training_output.txt       # Sample output generated
│
├── requirements.txt
└── README.md (this file)
```

🗑️ *Legacy PCAP extraction (`botnetdetect.py`, pyshark, magic, tshark) is no longer required.*

---

## 🧠 Core Concept  
The system classifies each network flow using:

- Traffic size statistics  
- Payload entropy  
- Packet rates  
- Protocol behavior  
- Flow duration  
- Ratio of incoming/outgoing bytes  

These features are already pre-extracted in `training.csv`.

---

## 📦 Installation

### 1️⃣ Create environment  
```bash
conda create -n p2pbot python=3.9
conda activate p2pbot
```

### 2️⃣ Install requirements  
```bash
pip install -r requirements.txt
```

> No PCAP tools like tshark or libmagic are needed anymore.

---

## ⚡ Usage

### ▶ CLI Mode  
Run detection directly on any CSV:

```bash
python detect.py <csv_file>
```

Example:

```bash
python detect.py training.csv
```

Outputs:

```text
<csv_name>_output.txt
```

---

### 🖥️ Streamlit UI  

Start the UI:

```bash
streamlit run app_streamlit.py
```

Features:

- Upload CSV  
- View summary stats  
- See total malicious flows  
- Download results  
- Visualizations and tables  

---

### 🌐 FastAPI Backend  

Start API server:

```bash
uvicorn app_fastapi:app --reload
```

Endpoints (example design):

| Method | Endpoint        | Description                              |
|--------|-----------------|------------------------------------------|
| GET    | `/health`       | Health check                             |
| POST   | `/predict-csv`  | Upload CSV, receive classified flows     |

Interactive docs (Swagger UI) at:

```text
http://localhost:8000/docs
```

---

## 📊 Model

The model (`trained_model.pickle`) is a BaggingClassifier trained on:

- ~100k+ network flows  
- Benign + multiple P2P botnet families  
- Cleaned metadata and 20+ statistical features  

If your pickle was created on old sklearn (0.22.x), use:

```bash
python convert_model.py
```

to convert it to a newer format for modern sklearn.

---

## 🧪 Features Used

| Feature                    | Description                              | Meta? |
|---------------------------|------------------------------------------|-------|
| src_ip                    | Source IP of flow                        | ✔     |
| src_port                  | Port of source                           | ✔     |
| dst_ip                    | Destination IP of flow                   | ✔     |
| dst_port                  | Port of destination                      | ✔     |
| protocol                  | Protocol used                            | ✔     |
| total_data                | Total data exchanged (incl. headers)     | ✖     |
| sent_packets              | Total packets sent                       | ✖     |
| recv_packets              | Total packets received                   | ✖     |
| sent_data                 | Total data sent                          | ✖     |
| recv_data                 | Total data received                      | ✖     |
| total_sent_payload        | Total payload sent                       | ✖     |
| total_recv_payload        | Total payload received                   | ✖     |
| max_payload_size          | Maximum payload size                     | ✖     |
| max_payload_entropy       | Maximum payload entropy                  | ✖     |
| min_payload_size          | Minimum payload size                     | ✖     |
| min_payload_entropy       | Minimum payload entropy                  | ✖     |
| net_entropy               | Entropy of all payload combined          | ✖     |
| average_payload_size      | Average payload size                     | ✖     |
| average_packet_length     | Average packet size                      | ✖     |
| average_packet_per_sec    | Average packets per second               | ✖     |
| average_packet_size_per_sec | Average data transfer rate             | ✖     |
| num_protocols             | Number of protocols used                 | ✖     |
| total_time                | Flow duration                            | ✖     |
| incoming_outgoing_ratio   | Incoming vs outgoing data ratio          | ✖     |
| num_small_packets         | Number of small packets                  | ✖     |
| label                     | Ground-truth label (0 = benign, 1 = bot) | ✔     |

---

## 👨‍💻 Contributors

| Name                     | GitHub                                  |
|--------------------------|-----------------------------------------|
| **Chirag Singh**         | — https://github.com/Chiraggg99         |
| **Geetanjali Sikarwar**  | — https://github.com/geetanjalisikarwar |

---

## 🛠️ TODO

- [ ] Add optional PCAP → CSV extraction module
- [ ] Threat actor / botnet family classification
- [ ] Clustering + visualization for flow patterns
- [ ] Dockerized deployment (FastAPI + Streamlit)
- [ ] Integration with SIEM / SOC pipelines (ELK, Splunk)

---

## 📬 Notes

This repository is a **modernized fork** of the original PCAP-based implementation, redesigned to be:

- Easier to run on any OS (no tshark/wireshark required)  
- More suitable for demos, research, and teaching  
- Ready to wrap into services (APIs / dashboards).  

