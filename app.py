import streamlit as st
import google.generativeai as genai
import os

# 1. Konfigurasi Halaman
st.set_page_config(page_title="AI App Saya", page_icon="🤖")
st.title("Aplikasi AI Saya 🚀")

# 2. Ambil API Key dari Secrets (Akan kita setting nanti di web Streamlit)
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# 3. Inisialisasi Model (Ganti 'gemini-1.5-flash' jika pakai model lain)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Tampilan Input User
user_input = st.text_input("Tanya sesuatu ke AI:", placeholder="Ketik di sini...")

if st.button("Kirim"):
    if user_input:
        with st.spinner("Sedang berpikir..."):
            try:
                # 5. Proses generate konten
                response = model.generate_content(user_input)
                st.subheader("Jawaban AI:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
    else:
        st.warning("Masukkan teks terlebih dahulu!")