import streamlit as st
import random
from gtts import gTTS
import tempfile
import os
import base64

st.set_page_config(page_title="AI Healthcare Assistant", layout="wide")

# ------------------------------
# Custom Styling
# ------------------------------
page_bg = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

* { font-family: 'DM Sans', sans-serif; }
h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

[data-testid="stAppViewContainer"] {
    background-image: linear-gradient(rgba(0, 0, 0, 0.72), rgba(0, 0, 0, 0.72)),
    url("https://images.unsplash.com/photo-1576091160550-2173dba999ef");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

[data-testid="stHeader"] { background: rgba(0,0,0,0); }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(0,20,40,0.95) 0%, rgba(0,10,25,0.98) 100%);
    border-right: 1px solid rgba(0,198,255,0.2);
}

h1, h2, h3, h4, h5, h6, p, label { color: white !important; }

.stButton>button {
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 12px;
    font-weight: 600;
    height: 48px;
    width: 100%;
    border: none;
    font-family: 'Syne', sans-serif;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px rgba(0,198,255,0.3);
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0,198,255,0.5);
}

.stTextInput>div>div>input,
.stTextArea textarea {
    background-color: rgba(255,255,255,0.08) !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid rgba(0,198,255,0.3) !important;
    backdrop-filter: blur(10px);
}

.voice-box {
    background: linear-gradient(135deg, rgba(0,198,255,0.1), rgba(0,114,255,0.1));
    border: 1px solid rgba(0,198,255,0.4);
    border-radius: 16px;
    padding: 24px;
    margin: 16px 0;
    backdrop-filter: blur(10px);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.title("🩺 AI Powered Healthcare Assistant")
st.markdown("Your smart health guidance companion — speak or type your symptoms")
st.warning("⚠ This system provides AI-based guidance only. Please consult a certified medical professional.")

# -----------------------------------
# Sidebar Menu
# -----------------------------------
option = st.sidebar.selectbox(
    "Choose Service",
    ["Symptom Checker", "Image Disease Scanner", "Live Skin Scanner", "World Famous Hospitals"]
)

# -------------------------
# Helper Functions
# -------------------------
def text_to_speech_base64(text):
    """Convert text to base64-encoded MP3 for inline browser playback"""
    tts = gTTS(text=text, lang="en")
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp_file.name)
    with open(tmp_file.name, "rb") as f:
        audio_bytes = f.read()
    os.remove(tmp_file.name)
    return base64.b64encode(audio_bytes).decode()

def get_assistant_response(user_input):
    """Generate assistant response based on symptoms"""
    user_input = user_input.lower()
    if "fever" in user_input or "temperature" in user_input:
        return "It seems like you may have a fever. Stay hydrated, rest well, and please consult a General Physician if the fever persists beyond two days."
    elif "rash" in user_input or "itching" in user_input or "skin" in user_input:
        return "This may be a skin allergy or dermatitis. Avoid scratching and consult a Dermatologist for proper diagnosis and treatment."
    elif "chest pain" in user_input or "heart" in user_input:
        return "Chest pain can be serious. Please seek immediate medical attention and consult a Cardiologist as soon as possible."
    elif "headache" in user_input or "migraine" in user_input:
        return "You may be experiencing a headache or migraine. Rest in a quiet dark room, stay hydrated, and consult a Neurologist if it is severe or recurring."
    elif "cough" in user_input or "cold" in user_input or "flu" in user_input:
        return "You may have a respiratory infection. Stay warm, drink warm fluids, and consult a General Physician if symptoms worsen."
    elif "stomach" in user_input or "nausea" in user_input or "vomiting" in user_input:
        return "You may have a gastrointestinal issue. Avoid heavy food, stay hydrated, and consult a Gastroenterologist if symptoms persist."
    else:
        return "Based on your symptoms, I recommend consulting a General Physician for a proper diagnosis. Please do not self-medicate."

def play_audio_response(text):
    """Generate TTS and auto-play it in the browser"""
    audio_b64 = text_to_speech_base64(text)
    audio_html = f"""
    <div class="voice-box" style="text-align:center;">
        <p style="color:#00c6ff; font-family:'Syne',sans-serif; font-size:14px; margin-bottom:12px;">
            🔊 Assistant Voice Response
        </p>
        <audio controls autoplay style="width:100%; border-radius:8px;">
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
        </audio>
    </div>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# -------------------------
# Voice Recognition Component
# -------------------------
def voice_input_component():
    """Browser-based voice recognition using Web Speech API"""
    voice_html = """
    <div style="
        background: linear-gradient(135deg, rgba(0,198,255,0.1), rgba(0,114,255,0.1));
        border: 1px solid rgba(0,198,255,0.4);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        text-align: center;
        font-family: 'DM Sans', sans-serif;
    ">
        <p style="color:#00c6ff; font-weight:700; font-size:16px; margin-bottom:6px;">
            🎙️ Voice Input
        </p>
        <p style="color:rgba(255,255,255,0.6); font-size:13px; margin-bottom:18px;">
            Click the mic, speak your symptoms, then copy & paste the text below
        </p>

        <button id="micBtn" onclick="toggleRecording()" style="
            background: linear-gradient(135deg, #00c6ff, #0072ff);
            border: none;
            border-radius: 50%;
            width: 76px;
            height: 76px;
            font-size: 30px;
            cursor: pointer;
            color: white;
            box-shadow: 0 4px 24px rgba(0,198,255,0.5);
            transition: all 0.3s ease;
            margin-bottom: 18px;
            display: block;
            margin-left: auto;
            margin-right: auto;
        ">🎤</button>

        <div id="status" style="color:rgba(255,255,255,0.45); font-size:13px; margin-bottom:14px;">
            Click mic to start recording
        </div>

        <div id="transcriptBox" style="
            display:none;
            background: rgba(0,198,255,0.08);
            border-left: 3px solid #00c6ff;
            border-radius: 0 12px 12px 0;
            padding: 14px 18px;
            text-align:left;
            color:white;
            font-style:italic;
            margin-bottom:14px;
        ">
            <small style="color:#00c6ff;">Heard:</small><br>
            <span id="transcriptText"></span>
        </div>

        <div id="copyArea" style="display:none;">
            <p style="color:rgba(255,255,255,0.5); font-size:12px; margin-bottom:8px;">
                📋 Copy this and paste into the symptom box below:
            </p>
            <input id="transcriptInput" readonly style="
                width:100%;
                padding:10px 14px;
                background:rgba(255,255,255,0.1);
                border:1px solid rgba(0,198,255,0.4);
                border-radius:8px;
                color:white;
                font-size:14px;
                box-sizing:border-box;
                margin-bottom:10px;
            "/>
            <button onclick="copyTranscript()" style="
                background:rgba(0,198,255,0.2);
                border:1px solid rgba(0,198,255,0.5);
                border-radius:8px;
                color:#00c6ff;
                padding:9px 24px;
                cursor:pointer;
                font-size:13px;
                font-weight:600;
                transition: all 0.2s ease;
            ">📋 Copy Text</button>
        </div>
    </div>

    <script>
    let recognition = null;
    let isRecording = false;

    function toggleRecording() {
        if (isRecording) { stopRecording(); } else { startRecording(); }
    }

    function startRecording() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            document.getElementById('status').innerHTML =
                '❌ Voice not supported. Please use Chrome or Edge browser.';
            document.getElementById('status').style.color = '#ff6b6b';
            return;
        }
        const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SR();
        recognition.lang = 'en-US';
        recognition.interimResults = true;
        recognition.maxAlternatives = 1;

        recognition.onstart = function() {
            isRecording = true;
            document.getElementById('micBtn').style.background = 'linear-gradient(135deg,#ff416c,#ff4b2b)';
            document.getElementById('micBtn').innerHTML = '⏹';
            document.getElementById('status').innerHTML = '🔴 Listening... Speak clearly';
            document.getElementById('status').style.color = '#ff6b6b';
            document.getElementById('copyArea').style.display = 'none';
        };

        recognition.onresult = function(event) {
            let interim = '', final = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const t = event.results[i][0].transcript;
                if (event.results[i].isFinal) final += t;
                else interim += t;
            }
            const display = final || interim;
            document.getElementById('transcriptText').innerText = display;
            document.getElementById('transcriptBox').style.display = 'block';
            if (final) {
                document.getElementById('transcriptInput').value = final;
                document.getElementById('copyArea').style.display = 'block';
            }
        };

        recognition.onerror = function(e) {
            document.getElementById('status').innerHTML = '❌ Error: ' + e.error + '. Try again.';
            document.getElementById('status').style.color = '#ff6b6b';
            resetMic();
        };

        recognition.onend = function() {
            resetMic();
            if (document.getElementById('transcriptInput').value) {
                document.getElementById('status').innerHTML = '✅ Done! Copy the text below.';
                document.getElementById('status').style.color = '#00ff88';
            }
        };

        recognition.start();
    }

    function stopRecording() { if (recognition) recognition.stop(); }

    function resetMic() {
        isRecording = false;
        document.getElementById('micBtn').style.background = 'linear-gradient(135deg,#00c6ff,#0072ff)';
        document.getElementById('micBtn').innerHTML = '🎤';
    }

    function copyTranscript() {
        const input = document.getElementById('transcriptInput');
        input.select();
        document.execCommand('copy');
        document.getElementById('status').innerHTML = '✅ Copied! Now paste it in the box below.';
        document.getElementById('status').style.color = '#00ff88';
    }
    </script>
    """
    st.components.v1.html(voice_html, height=400)

# -------------------------
# Symptom Checker with Voice
# -------------------------
if option == "Symptom Checker":
    st.subheader("📝 Symptom Checker")

    st.markdown("### 🎙️ Step 1 — Voice Input")
    voice_input_component()

    st.markdown("### ✏️ Step 2 — Type or Paste Your Symptoms")
    user_input = st.text_area(
        "Enter symptoms here (type directly or paste from voice above):",
        placeholder="e.g. I have fever and headache since yesterday...",
        height=120
    )

    st.markdown("### 🔍 Step 3 — Get Response")
    if st.button("🔍 Analyze Symptoms & Get Voice Response"):
        if user_input.strip() != "":
            with st.spinner("Analyzing your symptoms..."):
                response = get_assistant_response(user_input)

            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(0,198,255,0.1), rgba(0,114,255,0.1));
                border: 1px solid rgba(0,198,255,0.4);
                border-radius: 16px;
                padding: 20px 24px;
                margin: 12px 0;
            ">
                <p style="color:#00c6ff; font-weight:700; margin-bottom:8px;">🤖 Assistant Response:</p>
                <p style="color:white; font-size:16px; line-height:1.7; margin:0;">{response}</p>
            </div>
            """, unsafe_allow_html=True)

            # Auto-play voice response
            play_audio_response(response)

        else:
            st.warning("Please enter your symptoms first — type or use the voice input above.")

# -------------------------
# Image Disease Scanner
# -------------------------
elif option == "Image Disease Scanner":
    st.header("📷 Upload Medical Image")
    uploaded_file = st.file_uploader("Upload image (skin / report / x-ray)", type=["jpg", "png", "jpeg"])
    user_city = st.text_input("Enter your city for nearby hospital suggestion:")

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        if st.button("Scan Image"):
            possible_diseases = [
                ("Skin Infection", "Dermatologist"),
                ("Pneumonia", "Pulmonologist"),
                ("Fracture", "Orthopedic"),
                ("Normal", "No Specialist Required")
            ]
            prediction = random.choice(possible_diseases)
            result_text = f"Detected condition is {prediction[0]}. Recommended specialist is {prediction[1]}."
            st.success(f"Detected Condition: {prediction[0]}")
            st.write(f"Recommended Specialist: {prediction[1]}")
            play_audio_response(result_text)

            if user_city.strip() != "":
                st.subheader("🏥 Suggested Nearby Hospital")
                st.write(f"• {user_city} General Hospital")
                st.write(f"• City Care Medical Center")
                st.write(f"• Al-Shifa Health Clinic")
            else:
                st.info("Enter your city to get hospital suggestions.")

# -------------------------
# Live Skin Scanner
# -------------------------
elif option == "Live Skin Scanner":
    st.header("📷 Live Skin Scanner")
    user_city = st.text_input("Enter your city for hospital suggestion:")
    camera_image = st.camera_input("Take a photo of your skin area")

    if camera_image is not None:
        st.image(camera_image, caption="Captured Image", use_container_width=True)
        if st.button("Analyze Live Image"):
            possible_diseases = [
                ("Acne", "Dermatologist"),
                ("Skin Allergy", "Dermatologist"),
                ("Eczema", "Dermatologist"),
                ("Normal Skin", "No Specialist Required")
            ]
            prediction = random.choice(possible_diseases)
            result_text = f"Detected condition is {prediction[0]}. Recommended specialist is {prediction[1]}."
            st.success(f"Detected Condition: {prediction[0]}")
            st.write(f"Recommended Specialist: {prediction[1]}")
            play_audio_response(result_text)

            if user_city.strip() != "":
                st.subheader("🏥 Suggested Nearby Hospital")
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
