import streamlit as st

def login():
    st.sidebar.title("🔐 Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type='password')
    
    if st.sidebar.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state['authenticated'] = True
        else:
            st.error("❌ Invalid credentials")

def check_login():
    return st.session_state.get("authenticated", False)