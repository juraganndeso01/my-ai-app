import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Zenith Studio Pro V2", page_icon="🌌", layout="centered")

# --- 2. RESEP RAHASIA (System Instruction) ---
# Paste instruksi dari Google AI Studio di antara tanda kutip di bawah ini
ZENITH_INSTRUCTION = """
Nama kamu adalah Zenith Studio Pro V2. 
Kamu adalah asisten AI premium yang dikembangkan oleh Zenith Studio.
Gaya bicaramu cerdas, ringkas, dan sangat solutif.
"""

# --- 3. SIDEBAR UNTUK INPUT KEY ---
with st.sidebar:
    st.title("🌌 Zenith Pro Panel")
    st.markdown("---")
    user_key = st.text_input("Masukkan API Key Gemini Anda:", type="password")
    st.info("Dapatkan Key di: [Google AI Studio](https://aistudio.google.com/app/apikey)")
    st.divider()
    st.caption("Zenith Studio Pro V2 © 2026")

# --- 4. LOGIKA UTAMA ---
st.title("🤖 Zenith Studio Pro V2")

if not user_key:
    st.warning("⚠️ Akses Terkunci. Silakan masukkan API Key di sidebar untuk mulai.")
else:
    try:
        # Konfigurasi AI
        genai.configure(api_key=user_key)
        
        # Inisialisasi Model dengan path lengkap 'models/' untuk menghindari error 404
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash", 
            system_instruction=ZENITH_INSTRUCTION
        )

        # Memori Chat (Session State)
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Tampilkan History Chat
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Input User
        if prompt := st.chat_input("Apa yang bisa Zenith bantu?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # Menyiapkan riwayat pesan untuk dikirim kembali (konteks)
                history = [{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages[:-1]]
                chat = model.start_chat(history=history)
                response = chat.send_message(prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Terjadi kesalahan teknis: {e}")
        st.info("Tips: Pastikan API Key Anda valid dan sudah mengaktifkan 'Gemini API' di Google AI Studio.")
