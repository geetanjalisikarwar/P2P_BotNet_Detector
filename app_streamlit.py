# app_streamlit.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO
from datetime import datetime

# Mock detector_core functions (replace with your actual imports)
# from detector_core import load_model, clean_dataset, predict_flows

MODEL_PATH = "trained_model.pickle"

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


# Mock functions (replace with your actual implementation)
def load_model(model_path):
    """Load your trained model"""
    # return pickle.load(open(model_path, 'rb'))
    return "MockModel"


def predict_flows(df, model):
    """Predict malicious flows"""
    # Your actual prediction logic here
    # For demo, randomly mark some as malicious
    import numpy as np
    predictions = np.random.choice([0, 1], size=len(df), p=[0.85, 0.15])
    return df, predictions


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
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        model_path = st.text_input(
            "Model Path",
            MODEL_PATH,
            help="Path to your trained model file"
        )
        
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
    
    # Main content
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
    
    # Load model and predict
    try:
        with st.spinner("🔄 Loading model..."):
            model = load_model(model_path)
    except Exception as e:
        st.error(f"❌ Failed to load model: {e}")
        return
    
    with st.spinner("🔍 Analyzing flows... This may take a moment..."):
        flows, predictions = predict_flows(df, model)
        malicious_mask = predictions == 1
        malicious_flows = flows[malicious_mask].copy()
    
    # Calculate metrics
    total = len(df)
    mal_count = len(malicious_flows)
    ratio = mal_count / total if total > 0 else 0
    benign_count = total - mal_count
    
    # Success message
    st.markdown("""
    <div class="success-box">
        <h3>✅ Detection Complete</h3>
        <p>Analysis finished successfully. Review the results below.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics
    st.markdown("### 📊 Detection Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Flows",
            value=f"{total:,}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Malicious Flows",
            value=f"{mal_count:,}",
            delta=f"{ratio*100:.2f}%",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="Benign Flows",
            value=f"{benign_count:,}",
            delta=f"{(1-ratio)*100:.2f}%"
        )
    
    with col4:
        st.metric(
            label="Threat Level",
            value="HIGH" if ratio > 0.1 else "MEDIUM" if ratio > 0.05 else "LOW",
            delta=None
        )
    
    if mal_count == 0:
        st.success("🎉 No malicious flows detected. Your network appears clean!")
        return
    
    # Warning if high threat
    if ratio > 0.1:
        st.markdown("""
        <div class="warning-box">
            <h3>⚠️ High Threat Level Detected</h3>
            <p>More than 10% of flows are malicious. Immediate action recommended.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Visualization
    st.markdown("### 📈 Threat Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Benign', 'Malicious'],
            values=[benign_count, mal_count],
            hole=0.4,
            marker=dict(colors=['#22c55e', '#ef4444']),
            textinfo='label+percent',
            textfont=dict(size=14, color='white')
        )])
        fig_pie.update_layout(
            title="Flow Classification",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=True
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Bar chart
        fig_bar = go.Figure(data=[
            go.Bar(
                x=['Benign', 'Malicious'],
                y=[benign_count, mal_count],
                marker=dict(color=['#22c55e', '#ef4444']),
                text=[f"{benign_count:,}", f"{mal_count:,}"],
                textposition='auto',
            )
        ])
        fig_bar.update_layout(
            title="Flow Count Comparison",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            yaxis=dict(gridcolor='rgba(148, 163, 184, 0.1)'),
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Malicious flows table
    st.markdown("### 🚨 Malicious Flows Detected")
    st.dataframe(
        malicious_flows.head(limit_display),
        use_container_width=True,
        height=400
    )
    
    # Top talkers
    st.markdown("### 🔝 Top Threat Sources")
    col1, col2 = st.columns(2)
    
    # Check if IP columns exist
    if 'src_ip' in malicious_flows.columns:
        with col1:
            st.markdown("#### 📤 Top Source IPs")
            top_src = malicious_flows['src_ip'].value_counts().head(10)
            st.dataframe(
                top_src.to_frame('Count'),
                use_container_width=True
            )
    
    if 'dst_ip' in malicious_flows.columns:
        with col2:
            st.markdown("#### 📥 Top Destination IPs")
            top_dst = malicious_flows['dst_ip'].value_counts().head(10)
            st.dataframe(
                top_dst.to_frame('Count'),
                use_container_width=True
            )
    
    # Download button
    st.markdown("### 💾 Export Results")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        csv = malicious_flows.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Malicious Flows as CSV",
            data=csv,
            file_name=f"malicious_flows_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )
    
    with col2:
        if st.button("🔄 Analyze Another File"):
            st.rerun()


if __name__ == "__main__":
    main()