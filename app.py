import streamlit as st

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
    st.info("Running without API key (local/test mode)")

# ---------------------------
# Symptom Checker
# ---------------------------

symptoms = st.text_area("Describe your symptoms:")

if st.button("Analyze"):
    if symptoms.strip() != "":
        symptoms = symptoms.lower()

        if "fever" in symptoms:
            st.success("Possible Condition: Flu")
            st.write("Recommended Specialist: General Physician")

        elif "rash" in symptoms:
            st.success("Possible Condition: Skin Allergy")
            st.write("Recommended Specialist: Dermatologist")

        elif "chest pain" in symptoms:
            st.success("Possible Condition: Heart Issue")
            st.write("Recommended Specialist: Cardiologist")

        else:
            st.success("Possible Condition: Common Infection")
            st.write("Recommended Specialist: General Physician")
    else:
        st.error("Please enter symptoms.")
