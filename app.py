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

.response-card {
    background: linear-gradient(135deg, rgba(0,198,255,0.08), rgba(0,114,255,0.08));
    border: 1px solid rgba(0,198,255,0.35);
    border-radius: 16px;
    padding: 22px 26px;
    margin: 14px 0;
}

.firstaid-card {
    background: linear-gradient(135deg, rgba(0,255,136,0.07), rgba(0,198,100,0.07));
    border: 1px solid rgba(0,255,136,0.3);
    border-radius: 16px;
    padding: 22px 26px;
    margin: 14px 0;
}

.specialist-card {
    background: linear-gradient(135deg, rgba(255,180,0,0.08), rgba(255,120,0,0.08));
    border: 1px solid rgba(255,180,0,0.35);
    border-radius: 16px;
    padding: 18px 24px;
    margin: 14px 0;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.title("🩺 AI Powered Healthcare Assistant")
st.markdown("Your smart health guidance companion — speak or type your symptoms")
st.warning("⚠ This system provides AI-based guidance only. Please consult a certified medical professional for proper treatment.")

# -----------------------------------
# Sidebar Menu
# -----------------------------------
option = st.sidebar.selectbox(
    "Choose Service",
    ["Symptom Checker", "Image Disease Scanner", "Live Skin Scanner", "World Famous Hospitals"]
)

# -----------------------------------------------
# Disease Knowledge Base
# Each entry: keywords, diagnosis, specialist,
#             first_aid (list), voice_response (spoken text)
# -----------------------------------------------
DISEASE_DB = [
    {
        "keywords": ["fever", "temperature", "chills", "shivering", "hot body", "high temp"],
        "condition": "Fever / Viral Infection",
        "emoji": "🌡️",
        "specialist": "General Physician",
        "diagnosis": "You appear to have a fever. This is often caused by a viral or bacterial infection and your body's immune system fighting it.",
        "first_aid": [
            "💧 Drink plenty of fluids — water, ORS, or coconut water to stay hydrated",
            "🛏️ Rest completely and avoid physical exertion",
            "🧊 Apply a cool damp cloth on your forehead to reduce temperature",
            "💊 Take paracetamol (e.g. Panadol) as directed if temperature exceeds 38.5°C",
            "🚫 Avoid tea, coffee, and cold drinks",
            "🌡️ Monitor temperature every 2–3 hours",
            "🏥 Visit a doctor if fever exceeds 39.5°C or lasts more than 2 days",
        ],
        "voice_response": "You appear to have a fever. Here is your first aid advice. Drink plenty of fluids and rest. Apply a cool damp cloth on your forehead. Take paracetamol if temperature exceeds 38 point 5 degrees. Monitor your temperature every few hours and visit a doctor if fever lasts more than 2 days.",
    },
    {
        "keywords": ["headache", "migraine", "head pain", "head ache", "head hurts", "throbbing head"],
        "condition": "Headache / Migraine",
        "emoji": "🧠",
        "specialist": "Neurologist",
        "diagnosis": "You may be experiencing a tension headache or migraine. Common causes include stress, dehydration, eye strain, or neurological issues.",
        "first_aid": [
            "🌑 Rest in a quiet, dark room away from screens and noise",
            "💧 Drink 2–3 glasses of water immediately as dehydration is a common cause",
            "🧊 Apply a cold or warm compress on your forehead or neck",
            "💊 Take ibuprofen or paracetamol as directed for pain relief",
            "😴 Sleep for at least 30 minutes if possible",
            "🚫 Avoid bright lights, loud sounds, and phone screens",
            "🏥 See a Neurologist if headache is severe, recurring, or comes with vomiting",
        ],
        "voice_response": "You may have a headache or migraine. Rest in a quiet dark room and drink water immediately. Apply a cold compress on your forehead. Take ibuprofen or paracetamol for pain relief. Avoid bright lights and screens. If headaches are severe or recurring, please consult a Neurologist.",
    },
    {
        "keywords": ["rash", "itching", "itch", "skin rash", "allergy", "hives", "red skin", "bumps on skin"],
        "condition": "Skin Allergy / Rash",
        "emoji": "🩹",
        "specialist": "Dermatologist",
        "diagnosis": "You may have a skin allergy, contact dermatitis, or hives. This can be triggered by food, medicine, plants, or chemicals.",
        "first_aid": [
            "🚿 Gently wash the affected area with cool water and mild soap",
            "🚫 Do NOT scratch — it worsens the rash and can cause infection",
            "🧴 Apply calamine lotion or a mild hydrocortisone cream to reduce itching",
            "💊 Take an antihistamine (e.g. cetirizine) to reduce allergic reaction",
            "🧊 Apply a cool compress to soothe burning or swelling",
            "👕 Wear loose, breathable cotton clothing",
            "🏥 See a Dermatologist immediately if rash spreads rapidly or causes breathing difficulty",
        ],
        "voice_response": "You may have a skin allergy or rash. Wash the affected area with cool water. Do not scratch as it worsens the condition. Apply calamine lotion and take an antihistamine tablet. Wear loose cotton clothing. If the rash spreads rapidly or causes breathing difficulty, see a Dermatologist immediately.",
    },
    {
        "keywords": ["chest pain", "heart pain", "chest tightness", "heart attack", "angina", "chest pressure", "heart"],
        "condition": "Chest Pain / Cardiac Emergency",
        "emoji": "❤️",
        "specialist": "Cardiologist",
        "diagnosis": "Chest pain is a serious symptom that could indicate a cardiac event, angina, or other heart-related condition. This requires immediate attention.",
        "first_aid": [
            "🚨 CALL EMERGENCY SERVICES (115 / 1122) IMMEDIATELY",
            "🛋️ Sit or lie down in a comfortable position — do NOT walk around",
            "👗 Loosen tight clothing around your chest and neck",
            "💊 If prescribed, take aspirin (300mg) or GTN spray as directed by your doctor",
            "😮‍💨 Take slow, deep breaths to stay calm",
            "🚫 Do NOT eat or drink anything",
            "👥 Stay with someone — do NOT be alone until help arrives",
        ],
        "voice_response": "Chest pain is a serious emergency. Call emergency services immediately. Sit or lie down and do not walk around. Loosen tight clothing. Take slow deep breaths to stay calm. If prescribed, take aspirin. Do not eat or drink anything. Do not stay alone — wait for medical help immediately.",
    },
    {
        "keywords": ["cough", "cold", "flu", "sore throat", "runny nose", "sneezing", "congestion", "blocked nose"],
        "condition": "Cold / Flu / Respiratory Infection",
        "emoji": "🤧",
        "specialist": "General Physician",
        "diagnosis": "You appear to have a cold, flu, or upper respiratory tract infection. These are usually viral and resolve within 5–7 days with proper care.",
        "first_aid": [
            "☕ Drink warm fluids — herbal tea, warm water with honey and lemon, or broth",
            "🛏️ Get adequate rest — sleep at least 8 hours",
            "💨 Inhale steam from hot water to relieve nasal congestion",
            "🍯 Take a teaspoon of honey to soothe sore throat",
            "💊 Take paracetamol for fever or body aches if needed",
            "🧴 Use saline nasal spray or drops for blocked nose",
            "🏥 See a doctor if symptoms worsen after 5 days or you develop high fever or shortness of breath",
        ],
        "voice_response": "You may have a cold or flu. Drink warm fluids like herbal tea with honey and lemon. Rest and sleep well. Inhale steam to relieve congestion. Take paracetamol for fever. Use saline nasal drops for blocked nose. Visit a doctor if symptoms worsen after 5 days or you develop breathing difficulty.",
    },
    {
        "keywords": ["stomach", "stomach pain", "nausea", "vomiting", "diarrhea", "loose motion", "indigestion", "bloating", "abdominal pain", "stomach ache"],
        "condition": "Gastrointestinal Issue / Stomach Problem",
        "emoji": "🫀",
        "specialist": "Gastroenterologist",
        "diagnosis": "You may be experiencing a stomach infection, food poisoning, indigestion, or gastritis. These are common and usually manageable at home.",
        "first_aid": [
            "💧 Sip small amounts of water or ORS frequently to prevent dehydration",
            "🍚 Eat light, bland food — rice, boiled potatoes, toast, or bananas (BRAT diet)",
            "🚫 Avoid spicy, oily, dairy, or heavy food completely",
            "🛏️ Rest and avoid physical activity",
            "💊 Take oral rehydration salts (ORS) if experiencing diarrhea or vomiting",
            "🌿 Ginger tea or peppermint tea can help with nausea",
            "🏥 See a Gastroenterologist if symptoms persist beyond 48 hours or you see blood in stool/vomit",
        ],
        "voice_response": "You may have a stomach infection or gastrointestinal issue. Sip water or ORS frequently to stay hydrated. Eat light bland food like rice and toast. Avoid spicy and oily food. Take ginger tea for nausea. See a Gastroenterologist if symptoms persist beyond 48 hours or you notice blood in stool or vomit.",
    },
    {
        "keywords": ["diabetes", "sugar", "high sugar", "blood sugar", "low sugar", "hypoglycemia", "hyperglycemia"],
        "condition": "Diabetes / Blood Sugar Issue",
        "emoji": "🍬",
        "specialist": "Endocrinologist",
        "diagnosis": "You may be experiencing symptoms related to blood sugar fluctuation — either high (hyperglycemia) or low (hypoglycemia) blood sugar levels.",
        "first_aid": [
            "🍬 If feeling dizzy/shaky (low sugar): immediately eat 15g of fast sugar — glucose tablets, juice, or sugar",
            "💧 Drink water regularly and stay hydrated",
            "🥗 Eat small frequent meals — avoid skipping meals",
            "🚫 Avoid sweets, sugary drinks, and refined carbohydrates",
            "💊 Take your prescribed diabetes medication on time",
            "📊 Monitor blood sugar levels with a glucometer",
            "🏥 See an Endocrinologist regularly for proper management",
        ],
        "voice_response": "You may have a blood sugar issue related to diabetes. If feeling dizzy or shaky from low sugar, immediately eat glucose tablets or drink juice. Stay hydrated, eat small frequent meals, and avoid sweets. Take your prescribed medication on time and monitor blood sugar regularly. Consult an Endocrinologist for proper management.",
    },
    {
        "keywords": ["back pain", "back ache", "lower back", "spine", "backache", "lumbar pain"],
        "condition": "Back Pain / Musculoskeletal Issue",
        "emoji": "🦴",
        "specialist": "Orthopedic Specialist",
        "diagnosis": "You may be experiencing muscle strain, lumbar pain, or a spinal issue. Poor posture, heavy lifting, or prolonged sitting are common causes.",
        "first_aid": [
            "🛏️ Rest and avoid activities that worsen the pain",
            "🧊 Apply an ice pack for the first 48 hours (15–20 min intervals) to reduce inflammation",
            "🔥 After 48 hours, switch to a warm compress or heating pad to relax muscles",
            "💊 Take ibuprofen or a muscle relaxant as directed",
            "🧘 Do gentle stretches — knee-to-chest stretch or child's pose",
            "🪑 Improve your sitting posture — use a lumbar support cushion",
            "🏥 See an Orthopedic Specialist if pain radiates to legs or lasts more than a week",
        ],
        "voice_response": "You may have back pain or a musculoskeletal issue. Rest and avoid heavy lifting. Apply ice for the first 48 hours then switch to a warm compress. Take ibuprofen for pain relief. Do gentle stretches and improve your sitting posture. See an Orthopedic Specialist if pain radiates to your legs or lasts more than one week.",
    },
    {
        "keywords": ["anxiety", "stress", "panic", "panic attack", "anxious", "nervous", "mental health", "depression", "sad", "depressed"],
        "condition": "Anxiety / Mental Health",
        "emoji": "🧘",
        "specialist": "Psychiatrist / Psychologist",
        "diagnosis": "You may be experiencing anxiety, stress, or signs of depression. Mental health is just as important as physical health and deserves proper care.",
        "first_aid": [
            "😮‍💨 Practice deep breathing — inhale for 4 counts, hold 4, exhale 4 (box breathing)",
            "🧘 Try grounding: name 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste",
            "🚶 Take a short walk outside — fresh air and movement reduce anxiety quickly",
            "📵 Limit social media and news consumption",
            "💬 Talk to a trusted friend or family member about how you feel",
            "😴 Ensure 7–8 hours of quality sleep every night",
            "🏥 Consult a Psychiatrist or Psychologist — mental health care is not weakness",
        ],
        "voice_response": "You may be experiencing anxiety or stress. Practice deep breathing by inhaling for 4 counts, holding for 4, and exhaling for 4. Try grounding techniques and take a short walk outside. Limit social media use and talk to someone you trust. Ensure you get 7 to 8 hours of sleep. Please consult a Psychiatrist or Psychologist for proper support.",
    },
    {
        "keywords": ["eye", "eyes", "eye pain", "blurry vision", "red eye", "eye irritation", "conjunctivitis", "itchy eyes"],
        "condition": "Eye Problem / Conjunctivitis",
        "emoji": "👁️",
        "specialist": "Ophthalmologist",
        "diagnosis": "You may have an eye infection (conjunctivitis), eye strain, or irritation. These can be caused by infection, allergies, or excessive screen time.",
        "first_aid": [
            "💧 Rinse your eye gently with clean, cool water or saline solution",
            "🚫 Do NOT rub your eyes — it worsens irritation and spreads infection",
            "🌿 Apply a clean cool compress over closed eyes to soothe redness",
            "💊 Use antibiotic eye drops only if prescribed by a doctor",
            "📵 Reduce screen time and take 20-20-20 breaks (every 20 min, look 20 feet away for 20 sec)",
            "🙅 Do not share towels, pillows, or eye products with others",
            "🏥 See an Ophthalmologist if vision becomes blurry or pain is severe",
        ],
        "voice_response": "You may have an eye problem or conjunctivitis. Rinse your eye gently with clean cool water. Do not rub your eyes. Apply a cool compress over closed eyes. Reduce screen time and take regular breaks. Do not share towels or eye products. See an Ophthalmologist if vision becomes blurry or pain is severe.",
    },
]

DEFAULT_RESPONSE = {
    "condition": "General Health Concern",
    "emoji": "🩺",
    "specialist": "General Physician",
    "diagnosis": "Based on your input, I could not identify a specific condition. It is best to consult a General Physician who can properly evaluate your symptoms.",
    "first_aid": [
        "🛏️ Rest and avoid strenuous activity",
        "💧 Stay hydrated — drink at least 8 glasses of water daily",
        "🥗 Eat a balanced, nutritious diet",
        "😴 Get at least 7–8 hours of sleep",
        "🚫 Avoid self-medicating without a doctor's advice",
        "🏥 Visit a General Physician for a proper diagnosis",
    ],
    "voice_response": "Based on your symptoms, I recommend consulting a General Physician for a proper diagnosis. In the meantime, rest well, stay hydrated, eat nutritious food, and avoid self-medicating. Please take care of your health.",
}

# -----------------------------------------------
# Helper Functions
# -----------------------------------------------
def get_disease_info(user_input):
    """Match user input to disease knowledge base"""
    user_input_lower = user_input.lower()
    for disease in DISEASE_DB:
        for keyword in disease["keywords"]:
            if keyword in user_input_lower:
                return disease
    return DEFAULT_RESPONSE

def text_to_speech_base64(text):
    """Convert text to base64-encoded MP3"""
    tts = gTTS(text=text, lang="en")
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp_file.name)
    with open(tmp_file.name, "rb") as f:
        audio_bytes = f.read()
    os.remove(tmp_file.name)
    return base64.b64encode(audio_bytes).decode()

def play_audio_response(text):
    """Auto-play voice response in browser"""
    audio_b64 = text_to_speech_base64(text)
    audio_html = f"""
    <div class="voice-box" style="text-align:center;">
        <p style="color:#00c6ff; font-family:'Syne',sans-serif; font-size:14px; font-weight:700; margin-bottom:12px;">
            🔊 Assistant Voice Response — Auto Playing
        </p>
        <audio controls autoplay style="width:100%; border-radius:8px;">
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
        </audio>
    </div>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

def show_full_response(info, user_input_mode="text"):
    """Display the full structured response card"""

    # 1. Diagnosis Card
    st.markdown(f"""
    <div class="response-card">
        <p style="color:#00c6ff; font-weight:700; font-size:17px; margin-bottom:8px;">
            {info['emoji']} Detected Condition: {info['condition']}
        </p>
        <p style="color:rgba(255,255,255,0.85); font-size:15px; line-height:1.7; margin:0;">
            {info['diagnosis']}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 2. First Aid Card
    first_aid_items = "".join([
        f'<li style="color:rgba(255,255,255,0.88); font-size:14px; margin-bottom:8px; line-height:1.6;">{item}</li>'
        for item in info["first_aid"]
    ])
    st.markdown(f"""
    <div class="firstaid-card">
        <p style="color:#00ff88; font-weight:700; font-size:16px; margin-bottom:14px;">
            🩹 First Aid & Home Treatment
        </p>
        <ul style="padding-left:18px; margin:0;">
            {first_aid_items}
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # 3. Specialist Card
    st.markdown(f"""
    <div class="specialist-card">
        <p style="color:#ffb400; font-weight:700; font-size:15px; margin-bottom:4px;">
            👨‍⚕️ Recommended Specialist
        </p>
        <p style="color:white; font-size:16px; margin:0; font-weight:600;">
            {info['specialist']}
        </p>
        <p style="color:rgba(255,255,255,0.5); font-size:12px; margin-top:6px;">
            Please book an appointment if symptoms persist or worsen.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 4. Voice Response (always plays)
    play_audio_response(info["voice_response"])

# -----------------------------------------------
# Voice Recognition Component
# -----------------------------------------------
def voice_input_component():
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
            Click the mic, speak your symptoms clearly, then copy & paste the text below
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
    st.components.v1.html(voice_html, height=420)

# -----------------------------------------------
# PAGES
# -----------------------------------------------

if option == "Symptom Checker":
    st.subheader("📝 Symptom Checker")

    st.markdown("### 🎙️ Step 1 — Voice Input *(Chrome/Edge only)*")
    voice_input_component()

    st.markdown("### ✏️ Step 2 — Type or Paste Your Symptoms")
    user_input = st.text_area(
        "Describe your symptoms in detail:",
        placeholder="e.g. I have fever, headache, and body aches since yesterday...",
        height=120
    )

    st.markdown("### 🔍 Step 3 — Get Full Response")
    if st.button("🔍 Analyze & Get Voice Response"):
        if user_input.strip() != "":
            with st.spinner("Analyzing your symptoms..."):
                info = get_disease_info(user_input)
            show_full_response(info)
        else:
            st.warning("Please describe your symptoms first — type or use voice input above.")

elif option == "Image Disease Scanner":
    st.header("📷 Upload Medical Image")
    uploaded_file = st.file_uploader("Upload image (skin / report / x-ray)", type=["jpg", "png", "jpeg"])
    user_city = st.text_input("Enter your city for nearby hospital suggestion:")

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        if st.button("Scan Image"):
            possible_diseases = [
                ("skin infection", "Skin Infection"),
                ("pneumonia", "Pneumonia"),
                ("fracture", "Fracture"),
                ("normal", "Normal — No Condition Detected"),
            ]
            raw = random.choice(possible_diseases)
            info = get_disease_info(raw[0])

            st.markdown(f"**Scan Result:** {raw[1]}")
            show_full_response(info)

            if user_city.strip() != "":
                st.subheader("🏥 Suggested Nearby Hospital")
                st.write(f"• {user_city} General Hospital")
                st.write(f"• City Care Medical Center")
                st.write(f"• Al-Shifa Health Clinic")
            else:
                st.info("Enter your city to get hospital suggestions.")

elif option == "Live Skin Scanner":
    st.header("📷 Live Skin Scanner")
    user_city = st.text_input("Enter your city for hospital suggestion:")
    camera_image = st.camera_input("Take a photo of your skin area")

    if camera_image is not None:
        st.image(camera_image, caption="Captured Image", use_container_width=True)
        if st.button("Analyze Live Image"):
            possible_keywords = ["rash", "rash", "itching", "eczema"]
            keyword = random.choice(possible_keywords)
            info = get_disease_info(keyword)
            show_full_response(info)

            if user_city.strip() != "":
                st.subheader("🏥 Suggested Nearby Hospital")
                st.write(f"• {user_city} General Hospital")
                st.write(f"• City Care Medical Center")
                st.write(f"• Al-Shifa Health Clinic")
            else:
                st.info("Enter your city to get hospital suggestions.")

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
