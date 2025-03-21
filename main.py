# main.py
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
import os
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
load_dotenv()

# Google API anahtarını ortam değişkeninden al
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY ortam değişkeni bulunamadı. Lütfen .env dosyasına ekleyin.")
    st.stop()

# Sistem promptunu tanımla
SYSTEM_PROMPT = """Sen eğlenceli, pozitif ve bilgili bir sohbet asistanısın. Her zaman:
- Samimi ve arkadaş canlısı bir ton kullan
- Mizah ve kelime oyunlarını uygun şekilde kullan
- Karmaşık konuları basit ve eğlenceli örneklerle açıkla
- Pozitif ve yapıcı ol
- Yanıtlarını emojilerle zenginleştir 
- Türkçe yanıt ver ve Türk kültürüne uygun örnekler kullan
- Konuyla ilgili eğlenceli gerçekleri ve hikayeleri paylaş
"""

# LLM modelini başlat
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.7
)

# Streamlit uygulamasını yapılandır
st.title("Gemini Chat Uygulaması")
st.write("Google Gemini-2.0-Flash ile sohbet edin!")

# Sohbet geçmişini session state'te sakla
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sohbet geçmişini göster
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# Kullanıcı girişi
prompt = st.chat_input("Mesajınızı yazın...")

if prompt:
    # Sistem promptu ve kullanıcı mesajını birleştir
    system_message = HumanMessage(content=SYSTEM_PROMPT)
    user_message = HumanMessage(content=prompt)
    st.session_state.messages.append(user_message)
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # LLM'den cevap al
    with st.chat_message("assistant"):
        with st.spinner("Yanıt bekleniyor..."):
            response = llm.invoke([system_message, user_message])
            st.markdown(response.content)
    
    # AI mesajını ekle
    ai_message = AIMessage(content=response.content)
    st.session_state.messages.append(ai_message)

# Temizleme butonu
if st.button("Sohbeti Temizle"):
    st.session_state.messages = []
    st.rerun()

# Yan panelde bilgi
with st.sidebar:
    st.header("Bilgi")
    st.write("Bu uygulama Google Gemini-2.0-Flash modelini kullanır.")
    st.write("LangChain ile entegre edilmiştir.")
    st.write("Streamlit ile oluşturulmuştur.")