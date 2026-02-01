import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Zenith Studio Pro V2", page_icon="🌌", layout="centered")

# --- 2. CSS CUSTOM (BIAR GAK CUMA CHAT DOANG) ---
st.markdown("""
    <style>
    /* Mengubah background utama */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    
    /* Styling Header */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        background: -webkit-linear-gradient(#00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1rem;
        color: #b0b0b0;
        margin-bottom: 2rem;
    }

    /* Efek Glassmorphism untuk Chat */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 10px;
        margin-bottom: 10px;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. UI HEADER ---
st.markdown('<h1 class="main-title">ZENITH STUDIO PRO</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Next-Generation AI Intelligence v2.5</p>', unsafe_allow_html=True)

# --- 4. SIDEBAR (LOGIC USER QUOTA) ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/galaxy.png", width=80)
    st.title("Zenith Panel")
    st.markdown("---")
    st.write("🔑 **Akses Pengguna**")
    user_key = st.text_input("API Key Gemini:", type="password", placeholder="Paste Key anda disini...")
    st.info("Aplikasi ini menggunakan kuota user. Ambil key di [Google AI Studio](https://aistudio.google.com/app/apikey)")
    st.divider()
    st.caption("Zenith Studio © 2026")

# --- 5. LOGIKA AI ---
ZENITH_INSTRUCTION = "Nama kamu Zenith Studio Pro V2. Kamu asisten AI yang sangat cerdas, visualis, dan solutif."

if not user_key:
    st.warning("⚠️ SISTEM TERKUNCI: Silakan masukkan API Key di sidebar untuk mengaktifkan Zenith.")
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueGZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZAm8=giphy.gif", use_column_width=True)
else:
    try:
        genai.configure(api_key=user_key)
        # Gunakan model terbaru yang tadi kita bahas
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash", # Sesuaikan dengan yang tadi berhasil
            system_instruction=ZENITH_INSTRUCTION
        )

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Tulis pesan untuk Zenith..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                history = [{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages[:-1]]
                chat = model.start_chat(history=history)
                response = chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Terjadi gangguan sinyal: {e}")
