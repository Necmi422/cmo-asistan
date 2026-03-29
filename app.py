import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA VE TEMA AYARLARI ---
st.set_page_config(
    page_title="CMO Sempozyumu 2026",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS: Sol menüdeki beyaz yazıları ve butonları görünür yapar
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #1a237e !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    div.stButton > button {
        background-color: #283593;
        color: white !important;
        border: 1px solid #3949ab;
        width: 100%;
        border-radius: 8px;
        margin-bottom: 5px;
    }
    /* Örnek sorular için stil */
    .stButton > button {
        border-radius: 20px;
        border: 1px solid #4285F4;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. API VE MODEL YAPILANDIRMASI ---
# API Key'i doğrudan buraya yazıyoruz
API_KEY = "AIzaSyChx3p9huHTg6IMVEI-Not5i94g099578o"
genai.configure(api_key=API_KEY)

# 404 hatasını önlemek için model ismini EN GÜNCEL haliyle tanımlıyoruz
# Bazı kütüphane versiyonlarında başına 'models/' eklemek zorunludur.
MODEL_NAME = "models/gemini-1.5-flash"

system_instruction = """
Sen CMO Future Business Symposium 2026'nın resmi asistanısın. 
Antalya Belek'te 16-19 Nisan 2026'da gerçekleşecek etkinlik hakkında uzmansın.
Tema: 'Mutasyon' ve 'WTF?!'.
"""

# Model kurulumu
model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    system_instruction=system_instruction
)

# --- 3. SOL MENÜ (Sidebar) ---
with st.sidebar:
    st.markdown("### ✨ CMO Sempozyumu")
    st.markdown("---")
    
    # Menü butonları
    if st.button("💬 Asistan (Ana Sayfa)"):
        st.session_state.messages = [] # Sohbeti temizle
        st.rerun()
    
    st.button("📅 Program")
    st.button("👥 Konuşmacılar")
    st.button("🏆 CMO Awards")
    
    st.markdown("---")
    st.markdown(f"👤 **Necmi Yıldız**\n\n*Organizatör*")
    st.caption("Google Istanbul")

# --- 4. ANA EKRAN VE SOHBET MANTIĞI ---
st.markdown("## Build with Gemini")
st.caption("Sempozyum dijital asistanı aktif.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# ÖRNEK SORULAR (Başlangıçta görünür)
if not st.session_state.messages:
    st.write("👋 **Sıkça Sorulan Sorular:**")
    
    # Örnek soruları listesi
    suggestions = [
        "Sempozyumun bu yılki teması nedir?",
        "Etkinlik nerede ve ne zaman yapılacak?",
        "CMO Awards töreni hakkında bilgi verir misin?",
        "Programda hangi başlıklar var?"
    ]
    
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        if cols[i % 2].button(suggestion):
            # Tıklanan soruyu sohbete ekle ve yanıt üret
            st.session_state.messages.append({"role": "user", "content": suggestion})
            with st.spinner("Düşünüyorum..."):
                try:
                    response = model.generate_content(suggestion)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    st.rerun()
                except Exception as e:
                    st.error(f"Hata: {str(e)}")

# Sohbet Geçmişini Yazdır
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Yeni Soru Girişi
if prompt := st.chat_input("Bir şey sorun..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Teknik Hata: {str(e)}")
            st.info("Eğer 'Models not found' hatası devam ediyorsa API Key'iniz Google Cloud konsolunda henüz aktifleşmemiş olabilir.")
