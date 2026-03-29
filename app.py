import streamlit as st
import google.generativeai as genai

# Sayfa Yapılandırması
st.set_page_config(page_title="CMO Sempozyum Asistanı", page_icon="🎤")
st.title("🤖 CMO Sempozyum 2026")
st.markdown("Dijital asistanınıza hoş geldiniz. Etkinlik hakkında her şeyi sorabilirsiniz.")

# API ve Model Ayarları
genai.configure(api_key="AIzaSyChx3p9huHTg6IMVEI-Not5i94g099578o")

# BURAYA DİKKAT: Üç tırnak ( """ ) kullandık ki metin alt satıra geçebilsin
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""
Sen CMO Future Business Symposium 2026'nın resmi dijital asistanısın. 
Görevin, katılımcılara (üst düzey pazarlama liderleri ve CMO'lar) etkinlik boyunca rehberlik etmektir.

ETKİNLİK BİLGİLERİ:
- Teması: Mutasyon - Pazarlamanın Konfor Alanını Terk Etmesi
- Tarih: 16 – 19 Nisan 2026
- Konum: Antalya (Belek bölgesi)
- İçerik: Liderliğin kodları, işin geleceği, derinlikli tartışmalar ve yüzleşmeler.
- Ödül Töreni: CMO Awards 2026 kazananları bu sempozyum kapsamında açıklanacaktır.

KURALLAR:
1. Dilin her zaman profesyonel, vizyoner ve nazik olmalı.
2. Katılımcıların zamanı kıymetlidir, cevapların kısa ve öz olsun.
3. Bilmediğin spesifik bir lojistik detay olursa 'Bu konuda kayıt masasındaki ekip arkadaşlarımız size en doğru bilgiyi verecektir' de.
4. Tekfen Tower (Google Ofisi) ile ilgili sorularda, asistanın hazırlık sürecinin orada yapıldığını ama asıl etkinliğin Antalya'da olduğunu nazikçe belirt.
"""
)

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı Girişi
if prompt := st.chat_input("Nasıl yardımcı olabilirim?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Düşünüyorum..."):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
