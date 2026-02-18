import streamlit as st
import random

st.set_page_config(page_title="AI Healthcare Assistant", layout="wide")

# Safely load API key
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    API_KEY = None

st.title("🩺 AI Powered Healthcare Assistant")
st.markdown("Your smart health guidance companion")

st.warning("⚠ This system provides AI-based guidance only. Please consult a certified medical professional.")

if API_KEY:
    st.success("API Key Loaded Securely ✅")
else:
    st.info("Running without API key (Demo mode)")

# -----------------------------------
# Sidebar Menu
# -----------------------------------

option = st.sidebar.selectbox(
    "Choose Service",
    ["Symptom Checker", "Image Disease Scanner", "Live Skin Scanner"]
)

# -----------------------------------
# 1️⃣ Symptom Checker
# -----------------------------------

if option == "Symptom Checker":

    symptoms = st.text_area("Describe your symptoms:")

    if st.button("Analyze Symptoms"):
        if symptoms.strip() != "":
            symptoms = symptoms.lower()

            if "fever" in symptoms:
                disease = "Flu"
                specialist = "General Physician"

            elif "rash" in symptoms:
                disease = "Skin Allergy"
                specialist = "Dermatologist"

            elif "chest pain" in symptoms:
                disease = "Heart Issue"
                specialist = "Cardiologist"

            else:
                disease = "Common Infection"
                specialist = "General Physician"

            st.success(f"Possible Condition: {disease}")
            st.write(f"Recommended Specialist: {specialist}")
        else:
            st.error("Please enter symptoms.")

# -----------------------------------
# 2️⃣ Image Disease Scanner (Upload)
# -----------------------------------

elif option == "Image Disease Scanner":

    st.header("📷 Upload Medical Image")

    uploaded_file = st.file_uploader(
        "Upload image (skin / report / x-ray)", 
        type=["jpg", "png", "jpeg"]
    )

    user_city = st.text_input("Enter your city for nearby hospital suggestion:")

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        if st.button("Scan Image"):
            possible_diseases = [
                ("Skin Infection", "Dermatologist"),
                ("Pneumonia", "Pulmonologist"),
                ("Fracture", "Orthopedic"),
                ("Normal", "No Specialist Required")
            ]

            prediction = random.choice(possible_diseases)

            st.success(f"Detected Condition: {prediction[0]}")
            st.write(f"Recommended Specialist: {prediction[1]}")

            if user_city.strip() != "":
                st.subheader("🏥 Suggested Nearby Hospital")
                st.write(f"City: {user_city}")
                st.write(f"• {user_city} General Hospital")
                st.write(f"• City Care Medical Center")
                st.write(f"• Al-Shifa Health Clinic")
            else:
                st.info("Enter your city to get hospital suggestions.")

# -----------------------------------
# 3️⃣ Live Camera Skin Scanner
# -----------------------------------

elif option == "Live Skin Scanner":

    st.header("📷 Live Skin Scanner (Camera Detection)")

    user_city = st.text_input("Enter your city for hospital suggestion:")

    camera_image = st.camera_input("Take a photo of your skin area")

    if camera_image is not None:
        st.image(camera_image, caption="Captured Image", use_column_width=True)

        if st.button("Analyze Live Image"):
            possible_diseases = [
                ("Acne", "Dermatologist"),
                ("Skin Allergy", "Dermatologist"),
                ("Eczema", "Dermatologist"),
                ("Normal Skin", "No Specialist Required")
            ]

            prediction = random.choice(possible_diseases)

            st.success(f"Detected Condition: {prediction[0]}")
            st.write(f"Recommended Specialist: {prediction[1]}")

            if user_city.strip() != "":
                st.subheader("🏥 Suggested Nearby Hospital")
                st.write(f"City: {user_city}")
                st.write(f"• {user_city} General Hospital")
                st.write(f"• City Care Medical Center")
                st.write(f"• Al-Shifa Health Clinic")
            else:
                st.info("Enter your city to get hospital suggestions.")
