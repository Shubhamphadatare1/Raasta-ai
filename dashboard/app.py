import streamlit as st

# Page config
st.set_page_config(page_title="Raasta AI Dashboard", layout="wide", page_icon="🚦")

# Custom CSS for better UI
st.markdown("""
    <style>
        .main {
            background-color: #f5f7fa;
        }
        .title {
            font-size: 3em;
            color: #0f4c75;
            text-align: center;
            margin-bottom: 30px;
        }
        .stButton > button {
            background-color: #0f4c75;
            color: white;
            font-size: 18px;
            padding: 10px 24px;
            border: none;
            border-radius: 8px;
        }
        .stButton > button:hover {
            background-color: #3282b8;
            color: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">🚦 Raasta AI – Smart Traffic Violation Detection Dashboard</div>', unsafe_allow_html=True)

# Sidebar for feature selection
st.sidebar.header("🎛️ Select Detection Module")
module = st.sidebar.radio("", [
    "Helmet Detection",
    "Signal Jump Detection",
    "Triple Riding Detection",
    "Red Light Violation",
    "Seatbelt Detection",
    "Wrong Way Driving",
    "Fake Number Plate Detection",
    "Zebra Crossing Violation",
    "Traffic Heatmap",
    "Live Traffic Insights"
])

st.markdown(f"## 🔍 Currently Selected: **{module}**")

# Start Detection Button
if st.button("🚀 Start Detection"):
    if module == "Helmet Detection":
        st.success("Helmet detection started (dummy run)...")
    else:
        st.warning(f"{module} module is not yet integrated. Coming soon!")

# Footer Info
st.markdown("---")
st.info("📢 More modules will be added soon. Stay tuned for real-time traffic analytics, violation alerts, and city-wise dashboards!")