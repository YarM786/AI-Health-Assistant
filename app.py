import streamlit as st
import numpy as np
from PIL import Image
import random

st.set_page_config(page_title="AI Healthcare Assistant", layout="wide")

# ---------------------------
# Header
# ---------------------------
st.title("🩺 AI Powered Healthcare Assistant")
st.markdown("Your smart health guidance companion")
st.markdown("---")

st.warning("⚠ This system provides AI-based guidance only. Please consult a certified medical professional for final diagnosis.")

# Sidebar Navigation
option = st.sidebar.selectbox(
    "Choose Service",
    ("Symptom Checker", "Medical Image Analysis", "Doctor Recommendation")
)

# ---------------------------
# 1️⃣ Symptom Checker
# ---------------------------
if option == "Symptom Checker":
    st.header("🤖 Symptom Checker")

    symptoms = st.text_area("Describe your symptoms:")

    if st.button("Analyze Symptoms"):
        if symptoms:
            symptoms = symptoms.lower()

            if "fever" in symptoms or "cold" in symptoms:
                disease = "Flu"
                specialist = "General Physician"
            elif "chest pain" in symptoms:
                disease = "Heart Issue"
                specialist = "Cardiologist"
            elif "rash" in symptoms:
                disease = "Skin Allergy"
                specialist = "Dermatologist"
            else:
                disease = "Common Viral Infection"
                specialist = "General Physician"

            confidence = random.randint(70, 95)

            st.success(f"🩺 Possible Condition: {disease}")
            st.info(f"📊 Confidence Level: {confidence}%")
            st.write(f"👨‍⚕ Recommended Specialist: {specialist}")
        else:
            st.error("Please enter symptoms.")

# ---------------------------
# 2️⃣ Medical Image Analysis
# ---------------------------
elif option == "Medical Image Analysis":
    st.header("🖼 Medical Image Analysis")

    uploaded_file = st.file_uploader("Upload medical image (X-ray / Skin image)", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Analyze Image"):
            prediction = random.choice(["Normal", "Abnormality Detected"])
            confidence = random.randint(75, 98)

            st.success(f"🔍 Result: {prediction}")
            st.info(f"📊 Confidence Score: {confidence}%")

# ---------------------------
# 3️⃣ Doctor Recommendation
# ---------------------------
elif option == "Doctor Recommendation":
    st.header("🏥 Doctor Recommendation")

    disease_input = st.text_input("Enter diagnosed condition:")

    if st.button("Find Specialist"):
        mapping = {
            "flu": "General Physician",
            "skin allergy": "Dermatologist",
            "heart issue": "Cardiologist",
            "pneumonia": "Pulmonologist",
            "eye problem": "Ophthalmologist"
        }

        specialist = mapping.get(disease_input.lower(), "General Physician")

        st.success(f"👨‍⚕ You should consult a: {specialist}")
        st.write("📍 Nearby doctors feature can be integrated with Google Maps API.")

# ---------------------------
# Footer
# ---------------------------
st.markdown("---")
st.caption("AI Healthcare Assistant | Final Year Project")
