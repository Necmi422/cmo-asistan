import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA YAPILANDIRMASI VE AI STUDIO TEMASI ---
st.set_page_config(
    page_title="CMO Sempozyumu 2026 - Dijital Asistan",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gelişmiş CSS: Sol menüdeki görünürlük sorununu ve AI Studio şıklığını sağlar
st.markdown("""
    <style>
    /* Sol menü (Sidebar) arka planı ve yazı renkleri */
    [data-testid="stSidebar"] {
        background-color: #1a237e !important;
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p, [data-testid="stSidebar"] h3 {
        color: white !important;
    }
    /* Sol menüdeki butonlar */
    div.stButton > button {
        background-color: #283593;
        color: white !important;
        border: 1px solid #3949ab;
        width: 100%;
        border-radius: 8px;
    }
    /* Örnek soru butonları */
    .stButton > button {
        border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. API VE MODEL AYARLARI ---
API_KEY = "AIzaSyChx3p9huHTg6IMVEI-Not5i94g099578o"
genai.configure(api_key=API_KEY)

# 404 hatasını çözmek için model ismini doğrudan tanımlıyoruz
MODEL_ID = "models/gemini-1.5-flash"

system_instruction = """
Sen CMO Future Business Symposium 2026'nın RESMİ dijital asistanısın. 
Görevin, katılımcılara etkinlik boyunca rehberlik etmektir.

BİLGİ BANKASI:
- ANA TEMA: "Mutasyon - Pazarlamanın Konfor Alanını Terk Etmesi" (WTF?!).
- KONUM: Antalya, Belek.
- TARİH: 16 – 19 Nisan 2026.
- ÖDÜL TÖRENİ: CMO Awards 2026 Antalya'da yapılacaktır.
"""

# Model nesnesini oluştururken model_id'yi netleştiriyoruz
model = genai.GenerativeModel(
    model_name=MODEL_ID,
    system_instruction=system_instruction
)

# --- 3. SOL MENÜ (Sidebar) ---
with st.sidebar:
    st.markdown("### ✨ CMO Sempozyumu 2026")
    st.caption("Dijital Asistan v1.3")
    st.markdown("---")
    
    st.button("💬 Asistan (Aktif)", key="m1")
    st.button("📅 Program", key="m2")
    st.button("👥 Konuşmacılar", key="m3")
    st.button("🤝 Networking", key="m4")
    st.button("🏆 CMO Awards", key="m5")
    
    st.markdown("---")
    st.markdown("👤 **Necmi Yıldız**\n\n*Katılımcı / Organizatör*")
    st.info("📍 Tekfen Tower, İstanbul")

# --- 4. ANA EKRAN VE ÖRNEK SORULAR ---
st.markdown("## Build with Gemini")
st.caption("CMO Future Business Symposium 2026 Resmi Dijital Asistanı")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Örnek Sorular (Ekranda buton olarak görünür)
if not st.session_state.messages:
    st.write("👋 **Hoş geldiniz! İşte sorabileceğiniz bazı örnekler:**")
    
    suggestions = [
        "Sempozyumun bu yılki teması nedir?",
        "Antalya'daki etkinlik programı belli mi?",
        "CMO Awards töreni ne zaman yapılacak?",
        "Networking Match özelliği nasıl çalışıyor?"
    ]
    
    cols = st.columns(2)
    for i, quest in enumerate(suggestions):
        if cols[i % 2].button(quest):
            st.session_state.temp_prompt = quest

# Mesaj Geçmişi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Giriş ve Yanıt
prompt = st.chat_input("Mesajınızı yazın...")
user_input = prompt or st.session_state.get("temp_prompt")

if user_input:
    if "temp_prompt" in st.session_state: del st.session_state["temp_prompt"]
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            # Yanıt üretme
            response = model.generate_content(user_input)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Teknik bir sorun oluştu: {str(e)}")
