import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA YAPILANDIRMASI VE AI STUDIO TEMASI ---
st.set_page_config(
    page_title="CMO Sempozyumu 2026 - Dijital Asistan",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# AI Studio'nun koyu lacivert menü ve yazı tiplerini taklit eden CSS
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #1a237e;
        color: white;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 10px;
    }
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. API VE MODEL AYARLARI ---
API_KEY = "AIzaSyChx3p9huHTg6IMVEI-Not5i94g099578o"
genai.configure(api_key=API_KEY)

# Sisteme verdiğin bilgileri buraya "Beyin" olarak yüklüyoruz
system_instruction = """
Sen CMO Future Business Symposium 2026'nın RESMİ dijital asistanısın. 
Ekran görüntüsündeki ve linkteki TÜM bilgilere hakimsin.

BİLGİ BANKASI:
- ANA TEMA: "Mutasyon - Pazarlamanın Konfor Alanını Terk Etmesi" (WTF?! temasıyla da anılır).
- KONUM: Antalya, Belek.
- TARİH: 16 – 19 Nisan 2026.
- ÖNEMLİ BÖLÜMLER: 
  1. Program (Pazarlamanın geleceği, mutasyon tartışmaları).
  2. Konuşmacılar (Sektör liderleri ve CMO'lar).
  3. Networking Match (Katılımcı eşleşmeleri).
  4. CMO Awards (Ödül töreni Antalya'da yapılacak).

KURALLAR:
- Cevapların profesyonel ama samimi olsun (AI Studio'daki gibi).
- Kullanıcıya "CMO Sempozyumu 2026'ya hoş geldiniz!" diyerek yardımcı ol.
- Eğer bir bilgiyi bilmiyorsan "Kayıt masasına danışabilirsiniz" de.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# --- 3. SOL MENÜ (AI Studio Görünümü) ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=80)
    st.markdown("### CMO Sempozyumu 2026\n**Dijital Asistan**")
    st.markdown("---")
    
    # Menü İkonları (AI Studio'daki gibi)
    st.button("💬 Asistan", use_container_width=True)
    st.button("📅 Program", use_container_width=True)
    st.button("👥 Konuşmacılar", use_container_width=True)
    st.button("🤝 Networking Match", use_container_width=True)
    st.button("🏆 CMO Awards", use_container_width=True)
    
    st.markdown("---")
    st.write(f"👤 **Necmi Yıldız**\n*Katılımcı*")

# --- 4. ANA EKRAN ---
st.markdown("## Asistan <span style='color:#4caf50; font-size:small;'>● SİSTEM AKTİF</span>", unsafe_allow_html=True)
st.caption("CMO Future Business Symposium 2026 Resmi Dijital Asistanı")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "CMO Sempozyumu 2026'ya hoş geldiniz! Bu yıl 'WTF?!' temasıyla Antalya'da buluşuyoruz. Program detayları, konuşmacılarımız veya katılım koşulları hakkında size nasıl yardımcı olabilirim?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Mesajınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Bir hata oluştu. API anahtarınızı kontrol edin.")
