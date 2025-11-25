# app_streamlit.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO
from datetime import datetime
import requests
import os

# Custom CSS for stunning dark theme
def load_custom_css():
    st.markdown("""
    <style>
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, rgba(6, 182, 212, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
        padding: 2rem;
        border-radius: 1rem;
        border: 1px solid rgba(6, 182, 212, 0.3);
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #06b6d4 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    /* Metric cards */
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* File uploader */
    .uploadedFile {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 0.5rem;
    }
    
    /* Tables */
    .dataframe {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 0.5rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #06b6d4 0%, #3b82f6 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border-radius: 0.5rem;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(6, 182, 212, 0.3);
    }
    
    /* Info boxes */
    .info-box {
        background: rgba(6, 182, 212, 0.1);
        border-left: 4px solid #06b6d4;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .success-box {
        background: rgba(34, 197, 94, 0.1);
        border-left: 4px solid #22c55e;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Animation for loading */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    st.set_page_config(
        page_title="P2P Botnet Detector",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    load_custom_css()

    # Header
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🛡️ P2P Botnet Detector</h1>
        <p style="color: #94a3b8; font-size: 1.1rem;">Advanced ML-powered threat detection system</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar - API first (Streamlit uses API-hosted model)
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")

        api_url = st.text_input("Detector API URL", "http://localhost:8000").rstrip("/")

        st.markdown("---")
        st.markdown("### 🔧 Model Management")
        model_file = st.file_uploader("Upload model (.pkl/.pickle) to API", type=["pkl", "pickle"])
        if model_file is not None:
            if st.button("📤 Upload model to API"):
                try:
                    files = {"file": (model_file.name, model_file.read(), "application/octet-stream")}
                    resp = requests.post(f"{api_url}/upload-model", files=files, timeout=60)
                    resp.raise_for_status()
                    st.success("Model uploaded and loaded on API server.")
                except requests.RequestException as e:
                    st.error(f"❌ Failed to upload model: {e}")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {e}")

        if st.button("📥 Download model from API"):
            try:
                resp = requests.get(f"{api_url}/download-model", timeout=60)
                resp.raise_for_status()
                content = resp.content
                # derive filename from header or fallback
                filename = "downloaded_model.pickle"
                cd = resp.headers.get("content-disposition", "")
                if "filename=" in cd:
                    filename = cd.split("filename=")[-1].strip('" ')
                st.download_button("Save model locally", data=content, file_name=filename, mime="application/octet-stream")
            except requests.RequestException as e:
                st.error(f"❌ Failed to download model: {e}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")

        st.markdown("---")
        st.markdown("### 📊 Display Options")
        show_raw = st.checkbox("Show raw data", value=False)
        limit_display = st.slider(
            "Max malicious flows to display",
            min_value=10,
            max_value=1000,
            value=100,
            step=10
        )

        st.markdown("---")
        st.markdown("### 📈 Features")
        st.markdown("""
        - ✅ ML Detection
        - ✅ Real-time Analysis  
        - ✅ Flow-based Patterns
        - ✅ Advanced Visualization
        """)
        st.markdown("---")
        st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Main content - CSV upload for prediction
    uploaded_file = st.file_uploader(
        "📂 Upload Network Flow Data (CSV)",
        type=["csv"],
        help="Upload a CSV file with the same schema as training.csv"
    )

    if uploaded_file is None:
        # Welcome section when no file is uploaded
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="info-box">
                <h3>🔍 ML Detection</h3>
                <p>Advanced algorithms powered by machine learning to detect sophisticated threats</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-box">
                <h3>⚡ Real-time</h3>
                <p>Instant analysis of network flows with sub-second response times</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="info-box">
                <h3>🌐 Flow-based</h3>
                <p>Analyze network patterns and behaviors at the flow level</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.info("👆 Upload a CSV file to begin threat detection analysis")
        return

    # Process uploaded file
    try:
        csv_bytes = uploaded_file.read()
        df = pd.read_csv(StringIO(csv_bytes.decode("utf-8")))
    except Exception as e:
        st.error(f"❌ Failed to read CSV: {e}")
        return

    if df.empty:
        st.warning("⚠️ Uploaded CSV is empty")
        return

    # Show raw data if requested
    if show_raw:
        with st.expander("📄 Raw Data Preview"):
            st.dataframe(df.head(50), use_container_width=True)

    # Send CSV to FastAPI for prediction (API holds the model)
    try:
        with st.spinner("🔍 Sending data to detection API..."):
            files = {"file": (uploaded_file.name, csv_bytes, "text/csv")}
            params = {"limit": limit_display}
            resp = requests.post(f"{api_url}/predict-csv", files=files, params=params, timeout=60)
            resp.raise_for_status()
            result = resp.json()
    except requests.RequestException as e:
        st.error(f"❌ API request failed: {e}")
        return
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
        return

    # Parse API response
    total = result.get("total_flows", 0)
    mal_count = result.get("malicious_flows", 0)
    ratio = result.get("malicious_ratio", 0.0)
    returned = result.get("returned_flows", 0)
    malicious_sample = result.get("malicious_sample", [])
    top_sources = result.get("top_source_ips", {})
    top_dests = result.get("top_destination_ips", {})

    # Convert sample to DataFrame for display and download
    malicious_flows_df = pd.DataFrame(malicious_sample)

    # Minimal display of results
    st.metric("Total Flows", total)
    st.metric("Malicious Flows", mal_count)
    st.metric("Malicious Ratio", f"{ratio:.2%}")

    if not malicious_flows_df.empty:
        with st.expander(f"🚨 Malicious sample ({returned} rows)"):
            st.dataframe(malicious_flows_df, use_container_width=True)
        csv_down = malicious_flows_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download malicious sample CSV", data=csv_down, file_name="malicious_sample.csv", mime="text/csv")

    # simple charts for top IPs
    if top_sources:
        src_df = pd.DataFrame(list(top_sources.items()), columns=["src_ip", "count"])
        fig = px.bar(src_df, x="src_ip", y="count", title="Top Malicious Source IPs")
        st.plotly_chart(fig, use_container_width=True)

    if top_dests:
        dst_df = pd.DataFrame(list(top_dests.items()), columns=["dst_ip", "count"])
        fig = px.bar(dst_df, x="dst_ip", y="count", title="Top Malicious Destination IPs")
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()