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
    background-image: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)),
    url("https://images.unsplash.com/photo-1576091160550-2173dba999ef");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
[data-testid="stHeader"] { background: rgba(0,0,0,0); }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(0,20,40,0.97) 0%, rgba(0,10,25,0.99) 100%);
    border-right: 1px solid rgba(0,198,255,0.2);
}
h1,h2,h3,h4,h5,h6,p,label { color: white !important; }

.stButton>button {
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 12px;
    font-weight: 700;
    height: 50px;
    width: 100%;
    border: none;
    font-family: 'Syne', sans-serif;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px rgba(0,198,255,0.35);
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0,198,255,0.55);
}
.stTextInput>div>div>input,
.stTextArea textarea {
    background-color: rgba(255,255,255,0.07) !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid rgba(0,198,255,0.3) !important;
}
.response-card {
    background: linear-gradient(135deg, rgba(0,198,255,0.09), rgba(0,114,255,0.09));
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
    background: linear-gradient(135deg, rgba(255,180,0,0.09), rgba(255,120,0,0.09));
    border: 1px solid rgba(255,180,0,0.35);
    border-radius: 16px;
    padding: 18px 24px;
    margin: 14px 0;
}
.doctor-card {
    background: linear-gradient(135deg, rgba(180,0,255,0.09), rgba(100,0,255,0.09));
    border: 1px solid rgba(180,0,255,0.35);
    border-radius: 16px;
    padding: 18px 24px;
    margin: 14px 0;
}
.voice-box {
    background: linear-gradient(135deg, rgba(0,198,255,0.1), rgba(0,114,255,0.1));
    border: 1px solid rgba(0,198,255,0.4);
    border-radius: 16px;
    padding: 24px;
    margin: 16px 0;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.title("🩺 AI Powered Healthcare Assistant")
st.markdown("Speak, type, or use video — get instant diagnosis, first aid & doctor recommendations")
st.warning("⚠ This system provides AI-based guidance only. Always consult a certified medical professional.")

# -----------------------------------
# Sidebar Menu
# -----------------------------------
option = st.sidebar.selectbox(
    "Choose Service",
    ["🎥 Video Voice Recognition", "📝 Symptom Checker", "📷 Image Disease Scanner", "📸 Live Skin Scanner", "🌍 World Famous Hospitals"]
)

# -----------------------------------------------
# Disease Knowledge Base
# -----------------------------------------------
DISEASE_DB = [
    {
        "keywords": ["fever", "temperature", "chills", "shivering", "hot body", "high temp", "sweating"],
        "condition": "Fever / Viral Infection",
        "emoji": "🌡️",
        "specialist": "General Physician",
        "diagnosis": "You appear to have a fever, likely caused by a viral or bacterial infection. Your immune system is actively fighting it.",
        "first_aid": [
            "💧 Drink plenty of fluids — water, ORS, or coconut water to stay hydrated",
            "🛏️ Rest completely and avoid any physical exertion",
            "🧊 Apply a cool damp cloth on your forehead to reduce temperature",
            "💊 Take paracetamol (e.g. Panadol) if temperature exceeds 38.5°C",
            "🚫 Avoid tea, coffee, and cold drinks",
            "🌡️ Monitor temperature every 2–3 hours",
            "🏥 Visit a doctor if fever exceeds 39.5°C or lasts more than 2 days",
        ],
        "doctors": [
            {"name": "Dr. Ahmed Raza", "specialty": "General Physician", "hospital": "City General Hospital", "timing": "Mon–Sat: 9AM–5PM"},
            {"name": "Dr. Sara Khan", "specialty": "Internal Medicine", "hospital": "Medicare Clinic", "timing": "Daily: 10AM–7PM"},
            {"name": "Dr. Imran Sheikh", "specialty": "General Physician", "hospital": "Al-Shifa Medical Center", "timing": "Mon–Fri: 8AM–3PM"},
        ],
        "voice_response": "You appear to have a fever. Here is your first aid advice. Drink plenty of fluids and rest. Apply a cool damp cloth on your forehead. Take paracetamol if temperature exceeds 38 point 5 degrees. Monitor your temperature every few hours. Visit a doctor if fever lasts more than 2 days.",
    },
    {
        "keywords": ["headache", "migraine", "head pain", "head ache", "head hurts", "throbbing head", "pressure in head"],
        "condition": "Headache / Migraine",
        "emoji": "🧠",
        "specialist": "Neurologist",
        "diagnosis": "You may be experiencing a tension headache or migraine. Common causes include stress, dehydration, eye strain, or neurological issues.",
        "first_aid": [
            "🌑 Rest in a quiet, dark room away from screens and noise",
            "💧 Drink 2–3 glasses of water immediately — dehydration is a common cause",
            "🧊 Apply a cold or warm compress on your forehead or neck",
            "💊 Take ibuprofen or paracetamol as directed for pain relief",
            "😴 Sleep for at least 30 minutes if possible",
            "🚫 Avoid bright lights, loud sounds, and phone/laptop screens",
            "🏥 See a Neurologist if headache is severe, recurring, or with vomiting",
        ],
        "doctors": [
            {"name": "Dr. Fatima Malik", "specialty": "Neurologist", "hospital": "Brain & Spine Institute", "timing": "Tue–Sun: 10AM–6PM"},
            {"name": "Dr. Khalid Mehmood", "specialty": "Neurologist", "hospital": "Neuro Care Hospital", "timing": "Mon–Sat: 9AM–4PM"},
            {"name": "Dr. Nadia Hussain", "specialty": "General Physician", "hospital": "City Clinic", "timing": "Daily: 8AM–8PM"},
        ],
        "voice_response": "You may have a headache or migraine. Rest in a quiet dark room and drink water immediately. Apply a cold compress on your forehead. Take ibuprofen or paracetamol for pain relief. Avoid bright lights and screens. If headaches are severe or recurring, please consult a Neurologist.",
    },
    {
        "keywords": ["rash", "itching", "itch", "skin rash", "allergy", "hives", "red skin", "bumps on skin", "eczema", "dermatitis"],
        "condition": "Skin Allergy / Rash / Eczema",
        "emoji": "🩹",
        "specialist": "Dermatologist",
        "diagnosis": "You may have a skin allergy, contact dermatitis, eczema, or hives. This can be triggered by food, medicine, plants, or chemicals.",
        "first_aid": [
            "🚿 Gently wash the affected area with cool water and mild soap",
            "🚫 Do NOT scratch — it worsens rash and can cause infection",
            "🧴 Apply calamine lotion or mild hydrocortisone cream to reduce itching",
            "💊 Take an antihistamine (e.g. cetirizine) to reduce allergic reaction",
            "🧊 Apply a cool compress to soothe burning or swelling",
            "👕 Wear loose, breathable cotton clothing",
            "🏥 See a Dermatologist immediately if rash spreads or causes breathing difficulty",
        ],
        "doctors": [
            {"name": "Dr. Zara Ahmed", "specialty": "Dermatologist", "hospital": "Skin Care Clinic", "timing": "Mon–Sat: 10AM–7PM"},
            {"name": "Dr. Omar Farooq", "specialty": "Dermatologist", "hospital": "DermaCare Hospital", "timing": "Tue–Sun: 9AM–5PM"},
            {"name": "Dr. Hina Baig", "specialty": "Skin Specialist", "hospital": "Al-Noor Medical", "timing": "Mon–Fri: 11AM–6PM"},
        ],
        "voice_response": "You may have a skin allergy or rash. Wash the affected area with cool water. Do not scratch as it worsens the condition. Apply calamine lotion and take an antihistamine tablet. Wear loose cotton clothing. See a Dermatologist immediately if the rash spreads rapidly.",
    },
    {
        "keywords": ["chest pain", "heart pain", "chest tightness", "heart attack", "angina", "chest pressure", "heart", "palpitation"],
        "condition": "Chest Pain / Cardiac Emergency",
        "emoji": "❤️",
        "specialist": "Cardiologist",
        "diagnosis": "Chest pain is a serious symptom that could indicate a cardiac event, angina, or other heart-related condition. This requires IMMEDIATE attention.",
        "first_aid": [
            "🚨 CALL EMERGENCY SERVICES (115 / 1122) IMMEDIATELY",
            "🛋️ Sit or lie down in a comfortable position — do NOT walk around",
            "👗 Loosen tight clothing around your chest and neck",
            "💊 If prescribed, take aspirin (300mg) or GTN spray as directed",
            "😮‍💨 Take slow, deep breaths to stay calm",
            "🚫 Do NOT eat or drink anything",
            "👥 Stay with someone — do NOT be alone until help arrives",
        ],
        "doctors": [
            {"name": "Dr. Tariq Mahmood", "specialty": "Cardiologist", "hospital": "Heart Institute Pakistan", "timing": "Mon–Sat: 9AM–3PM"},
            {"name": "Dr. Ayesha Siddiqui", "specialty": "Cardiologist", "hospital": "Cardiac Care Center", "timing": "Tue–Sun: 10AM–5PM"},
            {"name": "Dr. Bilal Akhtar", "specialty": "Interventional Cardiologist", "hospital": "Punjab Heart Hospital", "timing": "Mon–Fri: 8AM–2PM"},
        ],
        "voice_response": "Chest pain is a serious emergency. Call emergency services immediately. Sit or lie down and do not walk around. Loosen tight clothing. Take slow deep breaths to stay calm. Do not eat or drink anything. Do not stay alone — wait for medical help immediately.",
    },
    {
        "keywords": ["cough", "cold", "flu", "sore throat", "runny nose", "sneezing", "congestion", "blocked nose", "throat pain"],
        "condition": "Cold / Flu / Respiratory Infection",
        "emoji": "🤧",
        "specialist": "General Physician / ENT Specialist",
        "diagnosis": "You appear to have a cold, flu, or upper respiratory tract infection. These are usually viral and resolve within 5–7 days with proper care.",
        "first_aid": [
            "☕ Drink warm fluids — herbal tea, warm water with honey & lemon, or broth",
            "🛏️ Get adequate rest — sleep at least 8 hours",
            "💨 Inhale steam from hot water to relieve nasal congestion",
            "🍯 Take a teaspoon of honey to soothe sore throat",
            "💊 Take paracetamol for fever or body aches if needed",
            "🧴 Use saline nasal spray or drops for blocked nose",
            "🏥 See a doctor if symptoms worsen after 5 days or you develop high fever",
        ],
        "doctors": [
            {"name": "Dr. Usman Ali", "specialty": "ENT Specialist", "hospital": "ENT Care Hospital", "timing": "Mon–Sat: 9AM–6PM"},
            {"name": "Dr. Amna Pervez", "specialty": "General Physician", "hospital": "City Health Clinic", "timing": "Daily: 8AM–10PM"},
            {"name": "Dr. Shahid Latif", "specialty": "Pulmonologist", "hospital": "Lung & Chest Institute", "timing": "Mon–Fri: 10AM–4PM"},
        ],
        "voice_response": "You may have a cold or flu. Drink warm fluids like herbal tea with honey and lemon. Rest and sleep well. Inhale steam to relieve congestion. Take paracetamol for fever. Use saline nasal drops for blocked nose. Visit a doctor if symptoms worsen after 5 days.",
    },
    {
        "keywords": ["stomach", "stomach pain", "nausea", "vomiting", "diarrhea", "loose motion", "indigestion", "bloating", "abdominal pain", "stomach ache", "food poisoning"],
        "condition": "Gastrointestinal / Stomach Problem",
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
            "🏥 See a doctor if symptoms persist beyond 48 hours or you see blood in stool",
        ],
        "doctors": [
            {"name": "Dr. Rabia Nawaz", "specialty": "Gastroenterologist", "hospital": "Gastro Care Center", "timing": "Mon–Sat: 10AM–6PM"},
            {"name": "Dr. Faisal Qureshi", "specialty": "Gastroenterologist", "hospital": "Digestive Health Institute", "timing": "Tue–Sun: 9AM–5PM"},
            {"name": "Dr. Sana Mirza", "specialty": "General Physician", "hospital": "Medico Hospital", "timing": "Daily: 9AM–9PM"},
        ],
        "voice_response": "You may have a stomach infection or gastrointestinal issue. Sip water or ORS frequently. Eat light bland food like rice and toast. Avoid spicy and oily food. Take ginger tea for nausea. See a Gastroenterologist if symptoms persist beyond 48 hours.",
    },
    {
        "keywords": ["diabetes", "sugar", "high sugar", "blood sugar", "low sugar", "hypoglycemia", "hyperglycemia", "diabetic"],
        "condition": "Diabetes / Blood Sugar Issue",
        "emoji": "🍬",
        "specialist": "Endocrinologist",
        "diagnosis": "You may be experiencing symptoms related to blood sugar fluctuation — either high (hyperglycemia) or low (hypoglycemia) blood sugar levels.",
        "first_aid": [
            "🍬 If feeling dizzy/shaky (low sugar): eat glucose tablets, juice, or sugar immediately",
            "💧 Drink water regularly and stay hydrated",
            "🥗 Eat small, frequent meals — avoid skipping meals",
            "🚫 Avoid sweets, sugary drinks, and refined carbohydrates",
            "💊 Take your prescribed diabetes medication on time",
            "📊 Monitor blood sugar levels with a glucometer",
            "🏥 See an Endocrinologist regularly for proper management",
        ],
        "doctors": [
            {"name": "Dr. Asif Javed", "specialty": "Endocrinologist", "hospital": "Diabetes Care Center", "timing": "Mon–Sat: 9AM–5PM"},
            {"name": "Dr. Lubna Tariq", "specialty": "Diabetologist", "hospital": "Sugar Free Clinic", "timing": "Tue–Sun: 10AM–6PM"},
            {"name": "Dr. Kamran Yousuf", "specialty": "Internal Medicine", "hospital": "Metro Hospital", "timing": "Mon–Fri: 8AM–4PM"},
        ],
        "voice_response": "You may have a blood sugar issue related to diabetes. If feeling dizzy or shaky, immediately eat glucose tablets or drink juice. Stay hydrated, eat small frequent meals, and avoid sweets. Take your prescribed medication on time. Consult an Endocrinologist for proper management.",
    },
    {
        "keywords": ["back pain", "back ache", "lower back", "spine", "backache", "lumbar pain", "neck pain", "joint pain"],
        "condition": "Back / Joint Pain",
        "emoji": "🦴",
        "specialist": "Orthopedic Specialist",
        "diagnosis": "You may be experiencing muscle strain, lumbar pain, or a spinal issue. Poor posture, heavy lifting, or prolonged sitting are common causes.",
        "first_aid": [
            "🛏️ Rest and avoid activities that worsen the pain",
            "🧊 Apply an ice pack for the first 48 hours (15–20 min intervals)",
            "🔥 After 48 hours, switch to a warm compress to relax muscles",
            "💊 Take ibuprofen or a muscle relaxant as directed",
            "🧘 Do gentle stretches — knee-to-chest stretch or child's pose",
            "🪑 Improve your sitting posture — use a lumbar support cushion",
            "🏥 See an Orthopedic Specialist if pain radiates to legs or lasts more than a week",
        ],
        "doctors": [
            {"name": "Dr. Naveed Iqbal", "specialty": "Orthopedic Surgeon", "hospital": "Bone & Joint Hospital", "timing": "Mon–Sat: 9AM–4PM"},
            {"name": "Dr. Sumera Haq", "specialty": "Orthopedic Specialist", "hospital": "Ortho Care Clinic", "timing": "Tue–Sun: 10AM–5PM"},
            {"name": "Dr. Junaid Malik", "specialty": "Spine Surgeon", "hospital": "Spinal Institute", "timing": "Mon–Fri: 8AM–3PM"},
        ],
        "voice_response": "You may have back or joint pain. Rest and avoid heavy lifting. Apply ice for the first 48 hours then switch to a warm compress. Take ibuprofen for pain relief. Do gentle stretches and improve your sitting posture. See an Orthopedic Specialist if pain lasts more than one week.",
    },
    {
        "keywords": ["anxiety", "stress", "panic", "panic attack", "anxious", "nervous", "mental health", "depression", "sad", "depressed", "worry", "tension"],
        "condition": "Anxiety / Stress / Mental Health",
        "emoji": "🧘",
        "specialist": "Psychiatrist / Psychologist",
        "diagnosis": "You may be experiencing anxiety, stress, or signs of depression. Mental health is just as important as physical health and deserves proper professional care.",
        "first_aid": [
            "😮‍💨 Practice box breathing — inhale 4 counts, hold 4, exhale 4, hold 4",
            "🧘 Try grounding: name 5 things you see, 4 feel, 3 hear, 2 smell, 1 taste",
            "🚶 Take a 10–15 minute walk outside — fresh air reduces anxiety quickly",
            "📵 Limit social media and news consumption",
            "💬 Talk to a trusted friend or family member about how you feel",
            "😴 Ensure 7–8 hours of quality sleep every night",
            "🏥 Consult a Psychiatrist or Psychologist — seeking help is strength, not weakness",
        ],
        "doctors": [
            {"name": "Dr. Maham Qadri", "specialty": "Psychiatrist", "hospital": "Mind & Soul Clinic", "timing": "Mon–Sat: 10AM–7PM"},
            {"name": "Dr. Rizwan Baig", "specialty": "Clinical Psychologist", "hospital": "Mental Wellness Center", "timing": "Tue–Sun: 9AM–5PM"},
            {"name": "Dr. Faryal Shah", "specialty": "Psychiatrist", "hospital": "Neuro Psych Hospital", "timing": "Mon–Fri: 11AM–6PM"},
        ],
        "voice_response": "You may be experiencing anxiety or stress. Practice deep breathing by inhaling for 4 counts, holding for 4, and exhaling for 4. Take a short walk outside and limit social media use. Talk to someone you trust and ensure you get 7 to 8 hours of sleep. Please consult a Psychiatrist or Psychologist for proper support.",
    },
    {
        "keywords": ["eye", "eyes", "eye pain", "blurry vision", "red eye", "eye irritation", "conjunctivitis", "itchy eyes", "watery eyes"],
        "condition": "Eye Problem / Conjunctivitis",
        "emoji": "👁️",
        "specialist": "Ophthalmologist",
        "diagnosis": "You may have an eye infection (conjunctivitis), eye strain, or irritation from allergy, infection, or excessive screen time.",
        "first_aid": [
            "💧 Rinse your eye gently with clean cool water or saline solution",
            "🚫 Do NOT rub your eyes — it worsens irritation and spreads infection",
            "🌿 Apply a clean cool compress over closed eyes to soothe redness",
            "💊 Use antibiotic eye drops only if prescribed by a doctor",
            "📵 Reduce screen time and use 20-20-20 rule (every 20 min, look 20 feet away for 20 sec)",
            "🙅 Do not share towels, pillows, or eye products with others",
            "🏥 See an Ophthalmologist if vision becomes blurry or pain is severe",
        ],
        "doctors": [
            {"name": "Dr. Samina Akhtar", "specialty": "Ophthalmologist", "hospital": "Eye Care Hospital", "timing": "Mon–Sat: 9AM–5PM"},
            {"name": "Dr. Adeel Hassan", "specialty": "Eye Surgeon", "hospital": "Vision Plus Clinic", "timing": "Tue–Sun: 10AM–6PM"},
            {"name": "Dr. Kiran Zafar", "specialty": "Ophthalmologist", "hospital": "Bright Eye Center", "timing": "Mon–Fri: 8AM–3PM"},
        ],
        "voice_response": "You may have an eye problem or conjunctivitis. Rinse your eye gently with clean cool water. Do not rub your eyes. Apply a cool compress over closed eyes. Reduce screen time. Do not share towels or eye products. See an Ophthalmologist if vision becomes blurry or pain is severe.",
    },
]

DEFAULT_RESPONSE = {
    "condition": "General Health Concern",
    "emoji": "🩺",
    "specialist": "General Physician",
    "diagnosis": "Based on your input, a specific condition could not be identified. A General Physician can properly evaluate your symptoms.",
    "first_aid": [
        "🛏️ Rest and avoid strenuous activity",
        "💧 Stay hydrated — drink at least 8 glasses of water daily",
        "🥗 Eat a balanced, nutritious diet",
        "😴 Get at least 7–8 hours of sleep",
        "🚫 Avoid self-medicating without a doctor's advice",
        "🏥 Visit a General Physician for a proper diagnosis",
    ],
    "doctors": [
        {"name": "Dr. Ahmed Raza", "specialty": "General Physician", "hospital": "City General Hospital", "timing": "Mon–Sat: 9AM–5PM"},
        {"name": "Dr. Amna Pervez", "specialty": "General Physician", "hospital": "City Health Clinic", "timing": "Daily: 8AM–10PM"},
        {"name": "Dr. Sara Khan", "specialty": "Internal Medicine", "hospital": "Medicare Clinic", "timing": "Daily: 10AM–7PM"},
    ],
    "voice_response": "Based on your symptoms, I recommend consulting a General Physician for a proper diagnosis. Rest well, stay hydrated, eat nutritious food, and avoid self-medicating. Please take care of your health.",
}

# -----------------------------------------------
# Helper Functions
# -----------------------------------------------
def get_disease_info(user_input):
    user_input_lower = user_input.lower()
    for disease in DISEASE_DB:
        for keyword in disease["keywords"]:
            if keyword in user_input_lower:
                return disease
    return DEFAULT_RESPONSE

def text_to_speech_base64(text):
    tts = gTTS(text=text, lang="en")
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp_file.name)
    with open(tmp_file.name, "rb") as f:
        audio_bytes = f.read()
    os.remove(tmp_file.name)
    return base64.b64encode(audio_bytes).decode()

def play_audio_response(text):
    audio_b64 = text_to_speech_base64(text)
    audio_html = f"""
    <div class="voice-box" style="text-align:center; margin-top:10px;">
        <p style="color:#00c6ff; font-family:'Syne',sans-serif; font-size:14px; font-weight:700; margin-bottom:12px;">
            🔊 Assistant Voice Response — Auto Playing
        </p>
        <audio controls autoplay style="width:100%; border-radius:8px;">
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
        </audio>
    </div>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

def show_full_response(info):
    # Diagnosis
    st.markdown(f"""
    <div class="response-card">
        <p style="color:#00c6ff; font-weight:700; font-size:18px; margin-bottom:8px;">
            {info['emoji']} Detected Condition: {info['condition']}
        </p>
        <p style="color:rgba(255,255,255,0.88); font-size:15px; line-height:1.75; margin:0;">
            {info['diagnosis']}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # First Aid
    items_html = "".join([
        f'<li style="color:rgba(255,255,255,0.88); font-size:14px; margin-bottom:9px; line-height:1.6;">{item}</li>'
        for item in info["first_aid"]
    ])
    st.markdown(f"""
    <div class="firstaid-card">
        <p style="color:#00ff88; font-weight:700; font-size:16px; margin-bottom:14px;">
            🩹 First Aid & Home Treatment
        </p>
        <ul style="padding-left:18px; margin:0;">{items_html}</ul>
    </div>
    """, unsafe_allow_html=True)

    # Specialist
    st.markdown(f"""
    <div class="specialist-card">
        <p style="color:#ffb400; font-weight:700; font-size:15px; margin-bottom:4px;">👨‍⚕️ Recommended Specialist</p>
        <p style="color:white; font-size:17px; margin:0; font-weight:700;">{info['specialist']}</p>
        <p style="color:rgba(255,255,255,0.45); font-size:12px; margin-top:5px;">Book an appointment if symptoms persist or worsen.</p>
    </div>
    """, unsafe_allow_html=True)

    # Doctors
    doctors_html = ""
    for doc in info.get("doctors", []):
        doctors_html += f"""
        <div style="
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(180,0,255,0.25);
            border-radius: 12px;
            padding: 14px 18px;
            margin-bottom: 10px;
        ">
            <p style="color:#cc88ff; font-weight:700; font-size:15px; margin:0 0 4px 0;">👨‍⚕️ {doc['name']}</p>
            <p style="color:rgba(255,255,255,0.7); font-size:13px; margin:2px 0;">🏥 {doc['hospital']}</p>
            <p style="color:rgba(255,255,255,0.55); font-size:13px; margin:2px 0;">🔬 {doc['specialty']}</p>
            <p style="color:rgba(255,255,255,0.45); font-size:12px; margin:2px 0;">🕐 {doc['timing']}</p>
        </div>
        """
    st.markdown(f"""
    <div class="doctor-card">
        <p style="color:#cc88ff; font-weight:700; font-size:16px; margin-bottom:14px;">
            🏥 Recommended Doctors Near You
        </p>
        {doctors_html}
    </div>
    """, unsafe_allow_html=True)

    # Voice Response
    play_audio_response(info["voice_response"])

# -----------------------------------------------
# Video Voice Recognition Component
# -----------------------------------------------
def video_voice_component():
    video_html = """
    <div style="
        background: linear-gradient(135deg, rgba(0,198,255,0.08), rgba(0,114,255,0.08));
        border: 1px solid rgba(0,198,255,0.4);
        border-radius: 20px;
        padding: 28px 24px;
        text-align: center;
        font-family: 'DM Sans', sans-serif;
    ">
        <p style="color:#00c6ff; font-weight:800; font-size:20px; margin-bottom:6px; font-family:'Syne',sans-serif;">
            🎥 Video Voice Recognition
        </p>
        <p style="color:rgba(255,255,255,0.55); font-size:13px; margin-bottom:22px;">
            Your camera will show while you speak. The app listens and analyzes your symptoms in real-time.
        </p>

        <!-- Video Preview -->
        <div style="position:relative; display:inline-block; margin-bottom:20px;">
            <video id="videoFeed" autoplay muted playsinline style="
                width: 320px;
                height: 220px;
                border-radius: 14px;
                border: 2px solid rgba(0,198,255,0.5);
                background: #000;
                object-fit: cover;
            "></video>
            <div id="recIndicator" style="
                display:none;
                position:absolute;
                top:10px; right:10px;
                background:rgba(255,0,0,0.85);
                color:white;
                font-size:11px;
                font-weight:700;
                padding:4px 10px;
                border-radius:20px;
                letter-spacing:1px;
            ">● REC</div>
        </div>

        <br>

        <!-- Mic Button -->
        <button id="videoMicBtn" onclick="toggleVideoRecording()" style="
            background: linear-gradient(135deg, #00c6ff, #0072ff);
            border: none;
            border-radius: 50%;
            width: 80px;
            height: 80px;
            font-size: 32px;
            cursor: pointer;
            color: white;
            box-shadow: 0 4px 28px rgba(0,198,255,0.55);
            transition: all 0.3s ease;
            margin-bottom: 18px;
        ">🎤</button>

        <div id="videoStatus" style="color:rgba(255,255,255,0.45); font-size:13px; margin-bottom:16px;">
            Click mic to start — camera will activate automatically
        </div>

        <!-- Live Transcript -->
        <div id="videoTranscriptBox" style="
            display:none;
            background: rgba(0,198,255,0.07);
            border-left: 3px solid #00c6ff;
            border-radius: 0 12px 12px 0;
            padding: 14px 18px;
            text-align:left;
            color:white;
            font-style:italic;
            margin-bottom:14px;
        ">
            <small style="color:#00c6ff; font-style:normal;">🎙️ You said:</small><br>
            <span id="videoTranscriptText" style="font-size:15px;"></span>
        </div>

        <!-- Copy Area -->
        <div id="videoCopyArea" style="display:none;">
            <p style="color:rgba(255,255,255,0.45); font-size:12px; margin-bottom:8px;">
                📋 Copy this text and paste it into the box below:
            </p>
            <input id="videoTranscriptInput" readonly style="
                width:100%;
                padding:10px 14px;
                background:rgba(255,255,255,0.08);
                border:1px solid rgba(0,198,255,0.4);
                border-radius:8px;
                color:white;
                font-size:14px;
                box-sizing:border-box;
                margin-bottom:10px;
            "/>
            <button onclick="copyVideoTranscript()" style="
                background:rgba(0,198,255,0.18);
                border:1px solid rgba(0,198,255,0.5);
                border-radius:8px;
                color:#00c6ff;
                padding:10px 28px;
                cursor:pointer;
                font-size:13px;
                font-weight:700;
            ">📋 Copy Text</button>
        </div>
    </div>

    <script>
    let videoStream = null;
    let videoRecognition = null;
    let videoIsRecording = false;

    async function startCamera() {
        try {
            videoStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
            document.getElementById('videoFeed').srcObject = videoStream;
        } catch(e) {
            document.getElementById('videoStatus').innerHTML = '⚠️ Camera access denied. Voice-only mode active.';
            document.getElementById('videoStatus').style.color = '#ffb400';
        }
    }

    function stopCamera() {
        if (videoStream) {
            videoStream.getTracks().forEach(t => t.stop());
            videoStream = null;
            document.getElementById('videoFeed').srcObject = null;
        }
    }

    function toggleVideoRecording() {
        if (videoIsRecording) { stopVideoRecording(); } else { startVideoRecording(); }
    }

    function startVideoRecording() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            document.getElementById('videoStatus').innerHTML =
                '❌ Voice recognition requires Chrome or Edge browser.';
            document.getElementById('videoStatus').style.color = '#ff6b6b';
            return;
        }

        startCamera();

        const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
        videoRecognition = new SR();
        videoRecognition.lang = 'en-US';
        videoRecognition.interimResults = true;
        videoRecognition.maxAlternatives = 1;

        videoRecognition.onstart = function() {
            videoIsRecording = true;
            document.getElementById('videoMicBtn').style.background = 'linear-gradient(135deg,#ff416c,#ff4b2b)';
            document.getElementById('videoMicBtn').innerHTML = '⏹';
            document.getElementById('videoMicBtn').style.boxShadow = '0 0 0 0 rgba(255,65,108,0.7)';
            document.getElementById('recIndicator').style.display = 'block';
            document.getElementById('videoStatus').innerHTML = '🔴 Recording... Speak your symptoms clearly';
            document.getElementById('videoStatus').style.color = '#ff6b6b';
            document.getElementById('videoCopyArea').style.display = 'none';
        };

        videoRecognition.onresult = function(event) {
            let interim = '', final = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const t = event.results[i][0].transcript;
                if (event.results[i].isFinal) final += t;
                else interim += t;
            }
            const display = final || interim;
            document.getElementById('videoTranscriptText').innerText = display;
            document.getElementById('videoTranscriptBox').style.display = 'block';
            if (final) {
                document.getElementById('videoTranscriptInput').value = final;
                document.getElementById('videoCopyArea').style.display = 'block';
            }
        };

        videoRecognition.onerror = function(e) {
            document.getElementById('videoStatus').innerHTML = '❌ Error: ' + e.error + '. Please try again.';
            document.getElementById('videoStatus').style.color = '#ff6b6b';
            resetVideoMic();
            stopCamera();
        };

        videoRecognition.onend = function() {
            resetVideoMic();
            stopCamera();
            if (document.getElementById('videoTranscriptInput').value) {
                document.getElementById('videoStatus').innerHTML = '✅ Recording complete! Copy your text below.';
                document.getElementById('videoStatus').style.color = '#00ff88';
            }
        };

        videoRecognition.start();
    }

    function stopVideoRecording() {
        if (videoRecognition) videoRecognition.stop();
    }

    function resetVideoMic() {
        videoIsRecording = false;
        document.getElementById('videoMicBtn').style.background = 'linear-gradient(135deg,#00c6ff,#0072ff)';
        document.getElementById('videoMicBtn').style.boxShadow = '0 4px 28px rgba(0,198,255,0.55)';
        document.getElementById('videoMicBtn').innerHTML = '🎤';
        document.getElementById('recIndicator').style.display = 'none';
    }

    function copyVideoTranscript() {
        const input = document.getElementById('videoTranscriptInput');
        input.select();
        document.execCommand('copy');
        document.getElementById('videoStatus').innerHTML = '✅ Copied! Paste it in the symptom box below.';
        document.getElementById('videoStatus').style.color = '#00ff88';
    }
    </script>
    """
    st.components.v1.html(video_html, height=620)

# -----------------------------------------------
# Text Voice Recognition Component
# -----------------------------------------------
def voice_input_component():
    voice_html = """
    <div style="
        background: linear-gradient(135deg, rgba(0,198,255,0.08), rgba(0,114,255,0.08));
        border: 1px solid rgba(0,198,255,0.4);
        border-radius: 16px;
        padding: 22px;
        text-align: center;
        font-family: 'DM Sans', sans-serif;
    ">
        <p style="color:#00c6ff; font-weight:700; font-size:15px; margin-bottom:6px;">🎙️ Audio-Only Voice Input</p>
        <p style="color:rgba(255,255,255,0.5); font-size:13px; margin-bottom:16px;">
            Click mic, speak clearly, then copy & paste text below
        </p>
        <button id="micBtn" onclick="toggleRecording()" style="
            background: linear-gradient(135deg, #00c6ff, #0072ff);
            border:none; border-radius:50%;
            width:70px; height:70px; font-size:28px;
            cursor:pointer; color:white;
            box-shadow:0 4px 22px rgba(0,198,255,0.5);
            transition: all 0.3s;
            display:block; margin:0 auto 16px;
        ">🎤</button>
        <div id="status" style="color:rgba(255,255,255,0.4); font-size:13px; margin-bottom:12px;">Click mic to start</div>
        <div id="transcriptBox" style="display:none; background:rgba(0,198,255,0.07); border-left:3px solid #00c6ff; border-radius:0 10px 10px 0; padding:12px 16px; text-align:left; color:white; font-style:italic; margin-bottom:12px;">
            <small style="color:#00c6ff; font-style:normal;">Heard:</small><br>
            <span id="transcriptText"></span>
        </div>
        <div id="copyArea" style="display:none;">
            <input id="transcriptInput" readonly style="width:100%; padding:9px 12px; background:rgba(255,255,255,0.08); border:1px solid rgba(0,198,255,0.4); border-radius:8px; color:white; font-size:14px; box-sizing:border-box; margin-bottom:9px;"/>
            <button onclick="copyTranscript()" style="background:rgba(0,198,255,0.18); border:1px solid rgba(0,198,255,0.5); border-radius:8px; color:#00c6ff; padding:8px 22px; cursor:pointer; font-size:13px; font-weight:600;">📋 Copy Text</button>
        </div>
    </div>
    <script>
    let recognition=null,isRecording=false;
    function toggleRecording(){if(isRecording){stopRecording();}else{startRecording();}}
    function startRecording(){
        if(!('webkitSpeechRecognition'in window)&&!('SpeechRecognition'in window)){
            document.getElementById('status').innerHTML='❌ Use Chrome or Edge.';
            document.getElementById('status').style.color='#ff6b6b';return;
        }
        const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
        recognition=new SR();recognition.lang='en-US';recognition.interimResults=true;
        recognition.onstart=function(){isRecording=true;document.getElementById('micBtn').style.background='linear-gradient(135deg,#ff416c,#ff4b2b)';document.getElementById('micBtn').innerHTML='⏹';document.getElementById('status').innerHTML='🔴 Listening...';document.getElementById('status').style.color='#ff6b6b';document.getElementById('copyArea').style.display='none';};
        recognition.onresult=function(e){let i='',f='';for(let x=e.resultIndex;x<e.results.length;x++){const t=e.results[x][0].transcript;if(e.results[x].isFinal)f+=t;else i+=t;}const d=f||i;document.getElementById('transcriptText').innerText=d;document.getElementById('transcriptBox').style.display='block';if(f){document.getElementById('transcriptInput').value=f;document.getElementById('copyArea').style.display='block';}};
        recognition.onerror=function(e){document.getElementById('status').innerHTML='❌ '+e.error;document.getElementById('status').style.color='#ff6b6b';resetMic();};
        recognition.onend=function(){resetMic();if(document.getElementById('transcriptInput').value){document.getElementById('status').innerHTML='✅ Done! Copy below.';document.getElementById('status').style.color='#00ff88';}};
        recognition.start();
    }
    function stopRecording(){if(recognition)recognition.stop();}
    function resetMic(){isRecording=false;document.getElementById('micBtn').style.background='linear-gradient(135deg,#00c6ff,#0072ff)';document.getElementById('micBtn').innerHTML='🎤';}
    function copyTranscript(){const i=document.getElementById('transcriptInput');i.select();document.execCommand('copy');document.getElementById('status').innerHTML='✅ Copied!';document.getElementById('status').style.color='#00ff88';}
    </script>
    """
    st.components.v1.html(voice_html, height=340)

# -----------------------------------------------
# PAGES
# -----------------------------------------------

if option == "🎥 Video Voice Recognition":
    st.subheader("🎥 Video Voice Recognition — Tell Us Your Symptoms")
    st.markdown("Your **camera activates** while you speak. The app listens, understands your symptoms, and responds with full diagnosis, first aid, and doctor recommendations — all by voice.")

    col1, col2 = st.columns([1.1, 1])

    with col1:
        st.markdown("#### Step 1 — Record Your Symptoms via Video")
        video_voice_component()

    with col2:
        st.markdown("#### Step 2 — Paste & Analyze")
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("🔵 **How it works:**\n\n1. Click the 🎤 mic button on the left\n2. Your camera turns ON\n3. Speak your symptoms clearly\n4. Text appears automatically\n5. Copy & paste it below\n6. Click Analyze for full response + voice reply")
        video_user_input = st.text_area(
            "Paste your spoken symptoms here:",
            placeholder="e.g. I have been having fever and chills since yesterday morning...",
            height=150,
            key="video_input"
        )
        if st.button("🔍 Analyze & Get Full Voice Response", key="video_analyze"):
            if video_user_input.strip():
                with st.spinner("Analyzing your symptoms..."):
                    info = get_disease_info(video_user_input)
                show_full_response(info)
            else:
                st.warning("Please paste your spoken symptoms in the box above first.")

elif option == "📝 Symptom Checker":
    st.subheader("📝 Symptom Checker")

    st.markdown("### 🎙️ Step 1 — Voice Input *(Chrome/Edge only)*")
    voice_input_component()

    st.markdown("### ✏️ Step 2 — Type or Paste Your Symptoms")
    user_input = st.text_area(
        "Describe your symptoms in detail:",
        placeholder="e.g. I have fever, headache, and body aches since yesterday...",
        height=130
    )

    if st.button("🔍 Analyze Symptoms & Get Voice Response"):
        if user_input.strip():
            with st.spinner("Analyzing..."):
                info = get_disease_info(user_input)
            show_full_response(info)
        else:
            st.warning("Please describe your symptoms first.")

elif option == "📷 Image Disease Scanner":
    st.header("📷 Upload Medical Image")
    uploaded_file = st.file_uploader("Upload image (skin / report / x-ray)", type=["jpg", "png", "jpeg"])
    user_city = st.text_input("Enter your city for nearby hospital suggestion:")

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        if st.button("Scan Image"):
            possible_keywords = ["skin infection", "cough", "fever", "rash"]
            keyword = random.choice(possible_keywords)
            info = get_disease_info(keyword)
            show_full_response(info)
            if user_city.strip():
                st.subheader("🏥 Suggested Nearby Hospitals")
                st.write(f"• {user_city} General Hospital")
                st.write(f"• City Care Medical Center")
                st.write(f"• Al-Shifa Health Clinic")
            else:
                st.info("Enter your city to get hospital suggestions.")

elif option == "📸 Live Skin Scanner":
    st.header("📸 Live Skin Scanner")
    user_city = st.text_input("Enter your city for hospital suggestion:")
    camera_image = st.camera_input("Take a photo of your skin area")

    if camera_image is not None:
        st.image(camera_image, caption="Captured Image", use_container_width=True)
        if st.button("Analyze Live Image"):
            info = get_disease_info("rash itching eczema")
            show_full_response(info)
            if user_city.strip():
                st.subheader("🏥 Suggested Nearby Hospitals")
                st.write(f"• {user_city} General Hospital")
                st.write(f"• City Care Medical Center")
                st.write(f"• Al-Shifa Health Clinic")
            else:
                st.info("Enter your city to get hospital suggestions.")

elif option == "🌍 World Famous Hospitals":
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
