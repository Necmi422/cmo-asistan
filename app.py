import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA YAPILANDIRMASI VE AI STUDIO TEMASI ---
st.set_page_config(
    page_title="CMO Sempozyumu 2026 - Dijital Asistan",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# AI Studio'nun o meşhur lacivert sol menüsünü ve profesyonel arayüzünü taklit eden CSS
st.markdown("""
    <style>
    /* Sol menü (Sidebar) tasarımı */
    [data-testid="stSidebar"] {
        background-color: #1a237e;
        color: white;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    /* Sohbet balonlarını yuvarlatma */
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 10px;
    }
    /* Giriş kutusunu düzenleme */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    /* Başlık rengi */
    .stMarkdown h1, .stMarkdown h2 {
        color: #202124;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. API VE MODEL AYARLARI ---
# API Key burada gömülü:
API_KEY = "AIzaSyChx3p9huHTg6IMVEI-Not5i94g099578o"
genai.configure(api_key=API_KEY)

# Sisteme verdiğimiz kurumsal bilgiler
system_instruction = """
Sen CMO Future Business Symposium 2026'nın RESMİ dijital asistanısın. 
Görevin, katılımcılara (üst düzey pazarlama liderleri ve CMO'lar) etkinlik boyunca rehberlik etmektir.

BİLGİ BANKASI:
- ANA TEMA: "Mutasyon - Pazarlamanın Konfor Alanını Terk Etmesi" (Etkinlikte 'WTF?!' temasıyla da anılmaktadır).
- KONUM: Antalya, Belek bölgesi.
- TARİH: 16 – 19 Nisan 2026.
- İÇERİK: Liderliğin kodları, işin geleceği, derinlikli tartışmalar ve yüzleşmeler.
- ÖDÜL TÖRENİ: CMO Awards 2026 kazananları bu sempozyum kapsamında açıklanacaktır.

KURALLAR:
1. Dilin her zaman profesyonel, vizyoner ve nazik olmalı.
2. Katılımcıların zamanı kıymetlidir, cevapların kısa ve öz olsun.
3. Kullanıcıyı her zaman "CMO Sempozyumu 2026'ya hoş geldiniz!" diyerek veya samimi bir asistan tonuyla karşıla.
"""

# Model Yapılandırması
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 2048,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=system_instruction
)

# --- 3. SOL MENÜ (AI STUDIO GÖRÜNÜMÜ) ---
with st.sidebar:
    # İkon ve Başlık
    st.markdown("### ✨ CMO Sempozyumu 2026\n**Dijital Asistan**")
    st.markdown("---")
    
    # AI Studio gibi butonlar
    st.button("💬 Asistan", use_container_width=True)
    st.button("📅 Program", use_container_width=True)
    st.button("👥 Konuşmacılar", use_container_width=True)
    st.button("🤝 Networking Match", use_container_width=True)
    st.button("🏆 CMO Awards", use_container_width=True)
    
    st.markdown("---")
    # Kullanıcı Profili (Senin için)
    st.markdown("👤 **Necmi Yıldız**\n*Katılımcı / Organizatör*")
    st.caption("Google Istanbul - Tekfen Tower")

# --- 4. ANA SOHBET EKRANI ---
st.markdown("## Asistan <span style='color:#4caf50; font-size:small;'>● SİSTEM AKTİF</span>", unsafe_allow_html=True)
st.caption("CMO Future Business Symposium 2026 Resmi Dijital Asistanı")
st.markdown("---")

# Sohbet Geçmişi Yönetimi
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "CMO Sempozyumu 2026'ya hoş geldiniz! Bu yıl 'WTF?!' temasıyla Antalya'da buluşuyoruz. Program detayları, konuşmacılarımız veya katılım koşulları hakkında size nasıl yardımcı olabilirim?"}
    ]

# Mesajları Ekranda Göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı Girişi
if prompt := st.chat_input("Mesajınızı buraya yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Yapay zekadan yanıt alma
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # HATA ANALİZİ: Sorun neyse ekrana detaylı basar
            st.error(f"Hata Oluştu: {str(e)}")
            st.info("İpucu: Eğer 'User location not supported' diyorsa, Streamlit'in bulut sunucuları Türkiye dışındaki bir bölgeden Google'a erişmeye çalışıyor olabilir.")
