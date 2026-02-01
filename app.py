import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="Zenith Studio Pro V2", page_icon="🌌", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    .main-title { font-size: 3.5rem; font-weight: 800; text-align: center; background: -webkit-linear-gradient(#00c6ff, #0072ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0; }
    .stChatMessage { background: rgba(255, 255, 255, 0.05); border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 10px; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00c6ff, #0072ff); border: none; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR (CONTROL PANEL) ---
with st.sidebar:
    st.markdown('<h1 style="color: #00c6ff;">🌌 ZENITH PANEL</h1>', unsafe_allow_html=True)
    user_key = st.text_input("🔑 Masukkan API Key Anda:", type="password", help="Gunakan kuota Anda sendiri dari Google AI Studio.")
    
    st.divider()
    st.subheader("🛠️ Pengaturan Model")
    selected_model = st.selectbox("Pilih Otak:", ["gemini-1.5-flash", "gemini-2.0-flash-exp", "gemini-1.5-pro"])
    temp = st.slider("Kreativitas (Temperature):", 0.0, 2.0, 1.0)
    
    st.divider()
    st.subheader("📁 Lampiran (Multi-Modal)")
    uploaded_file = st.file_uploader("Upload Foto/Dokumen", type=["png", "jpg", "jpeg", "webp"])
    if uploaded_file:
        st.image(uploaded_file, caption="Preview File", use_container_width=True)
    
    if st.button("🗑️ Hapus Riwayat Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 3. LOGIKA UTAMA ---
st.markdown('<h1 class="main-title">ZENITH STUDIO PRO</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #b0b0b0;">AI Intelligence System v2.5 Full Suite</p>', unsafe_allow_html=True)

ZENITH_INSTRUCTION = "Kamu adalah Zenith Studio Pro V2. Asisten AI premium yang solutif, cerdas, dan mampu menganalisis gambar dengan detail. Gunakan gaya bahasa yang pro namun bersahabat."

if not user_key:
    st.warning("⚠️ SISTEM TERKUNCI: Masukkan API Key di sidebar untuk mengakses fitur Multi-Modal Zenith.")
    st.info("💡 Tip: Zenith sekarang bisa 'melihat' foto jika Anda menguploadnya di sidebar.")
else:
    try:
        genai.configure(api_key=user_key)
        model = genai.GenerativeModel(
            model_name=selected_model,
            system_instruction=ZENITH_INSTRUCTION
        )

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Tampilkan Pesan
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Input Chat
        if prompt := st.chat_input("Tanya Zenith apa saja..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Zenith sedang berpikir..."):
                    # Logika Multi-Modal (Teks + Gambar)
                    if uploaded_file:
                        img = Image.open(uploaded_file)
                        response = model.generate_content(
                            [prompt, img],
                            generation_config={"temperature": temp}
                        )
                    else:
                        response = model.generate_content(
                            prompt,
                            generation_config={"temperature": temp}
                        )
                    
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"❌ Terjadi Kesalahan: {e}")

st.divider()
st.caption("© 2026 Zenith Studio Pro V2 | Built for High Performance")
