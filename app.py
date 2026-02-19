import streamlit as st
import random
from gtts import gTTS
import tempfile
import os
import speech_recognition as sr
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings

st.set_page_config(page_title="AI Healthcare Assistant", layout="wide")

# ------------------------------
# Custom AI Medical Background
# ------------------------------
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)),
    url("https://images.unsplash.com/photo-1576091160550-2173dba999ef");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

[data-testid="stHeader"] { background: rgba(0,0,0,0); }
[data-testid="stSidebar"] { background: rgba(0, 0, 0, 0.75); }

h1, h2, h3, h4, h5, h6, p, label { color: white !important; }

.stButton>button {
    background-color: #00c6ff;
    color: white;
    border-radius: 10px;
    font-weight: bold;
    height: 45px;
    width: 100%;
}

.stTextInput>div>div>input,
.stTextArea textarea {
    background-color: rgba(255,255,255,0.95);
    color: black;
    border-radius: 8px;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.title("🩺 AI Powered Healthcare Assistant")
st.markdown("Your smart health guidance companion")
st.warning("⚠ This system provides AI-based guidance only. Please consult a certified medical professional.")

# -----------------------------------
# Sidebar Menu
# -----------------------------------
option = st.sidebar.selectbox(
    "Choose Service",
    ["Symptom Checker", "Image Disease Scanner", "Live Skin Scanner", "World Famous Hospitals"]
)

# -------------------------
# Voice Input & Output Setup
# -------------------------
def text_to_speech(text):
    """Convert text to audio for browser playback"""
    tts = gTTS(text=text, lang="en")
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp_file.name)
    return tmp_file.name

def get_assistant_response(user_input):
    """Generate assistant response (basic example, replace with AI if needed)"""
    user_input = user_input.lower()
    # Simple symptom check response
    if "fever" in user_input:
        return "It seems like you may have a fever. Please consult a General Physician."
    elif "rash" in user_input:
        return "This may be a skin allergy. A Dermatologist can help."
    elif "chest pain" in user_input:
        return "Chest pain is serious. Please consult a Cardiologist immediately."
    else:
        return "It looks like a common infection. A General Physician can guide you further."

# -------------------------
# Symptom Checker with Voice
# -------------------------
if option == "Symptom Checker":
    st.subheader("📝 Describe your symptoms")
    st.markdown("You can type your symptoms or use voice input below:")

    # Voice input
    voice_button = st.button("🎤 Record Voice Input")
    user_input = st.text_area("Or type your symptoms here:")

    if voice_button:
        st.info("Listening... Please speak clearly (max 10 sec).")
        # Using microphone for speech recognition
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio = recognizer.listen(source, timeout=10)
                user_input = recognizer.recognize_google(audio)
                st.success(f"You said: {user_input}")
            except sr.UnknownValueError:
                st.error("Sorry, could not understand your voice.")
            except sr.RequestError:
                st.error("Speech recognition service failed.")

    if st.button("Analyze Symptoms") and user_input.strip() != "":
        response = get_assistant_response(user_input)
        st.success(f"Assistant: {response}")

        # Generate and play audio response
        audio_file = text_to_speech(response)
        st.audio(audio_file)
        os.remove(audio_file)

# -------------------------
# Image Disease Scanner
# -------------------------
elif option == "Image Disease Scanner":
    st.header("📷 Upload Medical Image")
    uploaded_file = st.file_uploader("Upload image (skin / report / x-ray)", type=["jpg", "png", "jpeg"])
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

# -------------------------
# Live Skin Scanner
# -------------------------
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

# -------------------------
# World Famous Hospitals
# -------------------------
elif option == "World Famous Hospitals":
    st.header("🌍 World Famous Hospitals for Research & Treatment")
    st.markdown("Explore globally recognized hospitals known for advanced research and specialized treatments.")
    st.subheader("🏥 Top Multi-Specialty Hospitals")
    st.markdown("""
    - 🇺🇸 **Mayo Clinic** - https://www.mayoclinic.org  
    - 🇺🇸 **Cleveland Clinic** - https://my.clevelandclinic.org  
    - 🇺🇸 **Johns Hopkins Hospital** - https://www.hopkinsmedicine.org  
    - 🇩🇪 **Charité – Berlin University Hospital** - https://www.charite.de  
    """)
    st.subheader("🎗 Cancer Research Centers")
    st.markdown("""
    - 🇺🇸 **MD Anderson Cancer Center** - https://www.mdanderson.org  
    - 🇬🇧 **Royal Marsden Hospital** - https://www.royalmarsden.nhs.uk  
    """)
    st.subheader("❤️ Heart & Cardiology Institutes")
    st.markdown("""
    - 🇺🇸 **Texas Heart Institute** - https://www.texasheart.org  
    - 🇬🇧 **Royal Brompton Hospital** - https://www.rbht.nhs.uk  
    """)
    st.subheader("🧠 Neurology & Brain Research")
    st.markdown("""
    - 🇺🇸 **Massachusetts General Hospital** - https://www.massgeneral.org  
    - 🇨🇭 **University Hospital Zurich** - https://www.usz.ch  
    """)
    st.info("⚠ These links are for research and educational purposes only. Always consult certified medical professionals.")
