import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA VE AI STUDIO GÖRSEL AYARLARI ---
st.set_page_config(
    page_title="CMO Symposium 2026 - AI Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS: Sol menüyü koyu lacivert, yazıları beyaz yapar. AI Studio şıklığı sağlar.
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    div.stButton > button {
        background-color: #1e293b;
        color: white !important;
        border: 1px solid #334155;
        border-radius: 8px;
        width: 100%;
        margin-bottom: 8px;
    }
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    /* Örnek Soru Butonları */
    div.stButton > button[kind="secondary"] {
        border-radius: 20px;
        border: 1px solid #4285F4;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. API VE MODEL YAPILANDIRMASI (HATA GİDERİCİ) ---
API_KEY = "AIzaSyChx3p9huHTg6IMVEI-Not5i94g099578o"
genai.configure(api_key=API_KEY)

# 404 Hatasını engellemek için "latest" takısını ekledik
MODEL_ID = "gemini-1.5-flash-latest"

system_instruction = """
Sen CMO Future Business Symposium 2026'nın resmi asistanısın. 
Antalya Belek'te 16-19 Nisan 2026'da gerçekleşecek etkinlik hakkında uzmansın.
Tema: 'Mutasyon - Pazarlamanın Konfor Alanını Terk Etmesi' (WTF?!).
Daima profesyonel, vizyoner ve kısa cevaplar ver.
"""

# Modeli oluşturma
model = genai.GenerativeModel(
    model_name=MODEL_ID,
    system_instruction=system_instruction
)

# --- 3. SOL MENÜ (Sidebar) ---
with st.sidebar:
    st.markdown("### ✨ CMO Symposium 2026")
    st.caption("Resmi Dijital Asistan")
    st.markdown("---")
    
    # Menü Öğeleri
    st.button("💬 Asistan")
    st.button("📅 Program")
    st.button("👥 Konuşmacılar")
    st.button("🤝 Networking")
    st.button("🏆 CMO Awards")
    
    st.markdown("---")
    st.markdown("👤 **Necmi Yıldız**\n\n*Organizatör / PMM*")
    st.info("📍 Google Istanbul - Tekfen Tower")

# --- 4. ANA EKRAN VE SOHBET AKIŞI ---
st.title("Build with Gemini")
st.caption("Antalya'daki büyük buluşma için size rehberlik ediyorum.")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# ÖRNEK SORULAR (Başlangıçta ekrana gelir)
if not st.session_state.messages:
    st.write("💡 **Hızlı Başlangıç:**")
    cols = st.columns(2)
    
    starters = [
        "Sempozyumun teması nedir?",
        "Antalya'daki program detayları neler?",
        "CMO Awards ne zaman açıklanacak?",
        "Etkinlik konumu ve tarihi nedir?"
    ]
    
    for i, s_prompt in enumerate(starters):
        if cols[i % 2].button(s_prompt):
            st.session_state.messages.append({"role": "user", "content": s_prompt})
            try:
                # Butona basıldığında hemen yanıt al
                response = model.generate_content(s_prompt)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.rerun()
            except Exception as e:
                st.error(f"Teknik Hata: {str(e)}")

# Mesaj Geçmişini Yazdır
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Yeni Mesaj Girişi
if user_query := st.chat_input("Mesajınızı buraya yazın..."):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(user_query)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Yanıt üretilemedi: {str(e)}")
