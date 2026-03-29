import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA VE TEMA AYARLARI ---
st.set_page_config(
    page_title="CMO Symposium 2026 - AI Studio",
    page_icon="🤖",
    layout="wide", # AI Studio gibi tam genişlik sağlar
    initial_sidebar_state="expanded"
)

# --- 2. API VE MODEL AYARLARI ---
API_KEY = "AIzaSyChx3p9huHTg6IMVEI-Not5i94g099578o"
genai.configure(api_key=API_KEY)

# AI Studio'daki gibi yapılandırma ayarları
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 2048,
}

# AI Studio'da yazdığımız System Instruction
system_instruction = """
Sen CMO Future Business Symposium 2026'nın resmi dijital asistanısın. 
Görevin, katılımcılara (üst düzey pazarlama liderleri ve CMO'lar) etkinlik boyunca rehberlik etmektir.

ETKİNLİK BİLGİLERİ:
- Teması: "Mutasyon - Pazarlamanın Konfor Alanını Terk Etmesi"
- Tarih: 16 – 19 Nisan 2026
- Konum: Antalya (Belek bölgesi)
- İçerik: Liderliğin kodları, işin geleceği, derinlikli tartışmalar ve yüzleşmeler.
- Ödül Töreni: CMO Awards 2026 kazananları bu sempozyum kapsamında açıklanacaktır.

KURALLAR:
1. Dilin her zaman profesyonel, vizyoner ve nazik olmalı.
2. Katılımcıların zamanı kıymetlidir, cevapların kısa ve öz olsun.
3. Bilmediğin spesifik bir lojistik detay olursa 'Bu konuda kayıt masasındaki ekip arkadaşlarımız size en doğru bilgiyi verecektir' de.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=system_instruction
)

# --- 3. SOL MENÜ (AI Studio Arayüzü) ---
with st.sidebar:
    st.markdown("<h1 style='color: #4285F4;'>Google AI Studio</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("📍 Etkinlik Özeti")
    st.info("**Tema:** Mutasyon\n\n**Tarih:** 16-19 Nisan 2026\n\n**Konum:** Antalya")
    
    st.markdown("---")
    st.subheader("Model Settings")
    st.text_input("Model", value="gemini-1.5-flash", disabled=True)
    st.slider("Temperature", 0.0, 1.0, 0.7, disabled=True)
    
    st.markdown("---")
    st.caption("CMO Society v1.0")

# --- 4. ANA SOHBET ALANI ---
st.markdown("<h1 style='color: #202124;'>Build with Gemini</h1>", unsafe_allow_html=True)
st.caption("CMO Sempozyumu için özel olarak eğitilmiş dijital asistan.")
st.markdown("---")

# Sohbet Geçmişi Tutma
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları Ekrana Basma
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı Girişi
if prompt := st.chat_input("Buraya sorunuzu yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # AI Studio mantığında yanıt üretme
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Bir bağlantı sorunu oluştu.")
            st.info("Lütfen API anahtarınızın Google Cloud tarafında kısıtlanmadığından emin olun.")

# --- 5. LOGO EKLEME (Opsiyonel) ---
# Eğer GitHub repona 'logo.png' diye bir dosya yüklersen, 
# aşağıdaki satırı aktif edip (başındaki # silerek) sol menüye logo koyabiliriz.
# st.sidebar.image("logo.png")
