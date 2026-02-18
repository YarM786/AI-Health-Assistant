import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("https://studentdetector-app-d6uattjwttxk3ghmmzwkej.streamlit.app/")

st.title("🩺 AI Powered Healthcare Assistant")

if API_KEY:
    st.success("API Key Loaded Securely ✅")
else:
    st.error("API Key Not Found ❌")

st.write("Your secure AI Healthcare Assistant is running.")
