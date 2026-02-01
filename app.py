import streamlit as st
import google.generativeai as genai

# Konfigurasi Tampilan
st.set_page_config(page_title="Zenith Studio Pro V2", layout="centered")

# --- RESEP RAHASIA (System Instruction) ---
# Di sinilah kepribadian AI kamu disimpan. Aman & tidak terlihat user.
ZENITH_INSTRUCTION = """
Nama kamu adalah Zenith Studio Pro V2. 
Kamu adalah asisten AI premium yang dikembangkan oleh Zenith Studio.
Gaya bicaramu cerdas, ringkas, dan sangat solutif.
"""

# --- SIDEBAR UNTUK INPUT KEY ---
with st.sidebar:
    st.title("🌌 Zenith Pro Panel")
    st.markdown("---")
    user_key = st.text_input("Masukkan API Key Gemini Anda:", type="password")
    st.info("Belum punya Key? [Klik di sini](https://aistudio.google.com/app/apikey)")
    st.divider()
    st.caption("Zenith Studio Pro V2 © 2024")

# --- LOGIKA UTAMA ---
st.title("🤖 Zenith Studio Pro V2")

if not user_key:
    st.warning("⚠️ Akses Terkunci. Silakan masukkan API Key di sidebar untuk mulai.")
else:
    # Set up AI dengan Key milik User
    genai.configure(api_key=user_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=ZENITH_INSTRUCTION
    )

    # Memori Chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Tampilkan Chat sebelumnya
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input Chat
    if prompt := st.chat_input("Tulis pesan..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # Kirim history agar AI ingat konteks
                history = [{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages[:-1]]
                chat = model.start_chat(history=history)
                response = chat.send_message(prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
