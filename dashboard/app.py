import streamlit as st
from auth import login

st.set_page_config(page_title="Raasta AI Dashboard", layout="wide")

if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    login()
    st.stop()

st.sidebar.title("🚦 Raasta AI")
st.sidebar.success("✅ Logged in")

st.title("📊 Raasta AI Control Panel")

st.markdown("""
<style>
div.stButton > button {
    height: 3em;
    width: 100%;
    font-size: 20px;
    margin: 5px 0;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("🪖 Helmet Detection"):
        st.switch_page("pages/Helmet Detection.py")
    if st.button("🚨 Signal Jump Detection"):
        st.switch_page("pages/Signal Jump Detection.py")

with col2:
    if st.button("👨‍👩‍👧 Triple Riding"):
        st.switch_page("pages/Triple Riding.py")
    if st.button("🚦 Red Light Jump"):
        st.switch_page("pages/Red Light Jump.py")