import streamlit as st
import pandas as pd
import uuid
from datetime import datetime
import base64

# Sayfa Yapılandırması
st.set_page_config(page_title="İnciroğlu Otomotiv | Müşteri Takip", layout="wide")

# Logoları Base64 olarak gömme fonksiyonu
def get_image_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# NOT: Dosyalarınız aynı klasörde olduğu sürece bu kod çalışır.
# Eğer hala dosya hatası alırsanız, bu iki satırı kullanın:
col_logo1, col_logo2 = st.columns([1, 1])
with col_logo1:
    try:
        st.image("BMW.png", width=150)
    except:
        st.error("BMW.png dosyası bulunamadı, dosya adını kontrol edin.")
with col_logo2:
    try:
        st.image("mini.png", width=150)
    except:
        st.error("mini.png dosyası bulunamadı, dosya adını kontrol edin.")

# Beyaz Başlık
st.markdown("""
    <div style='background-color: #1a1a1a; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <h1 style='text-align: center; color: #FFFFFF; font-family: Arial, sans-serif;'>
        İnciroğlu Otomotiv Müşteri Takip Sistemi
        </h1>
    </div>
    """, unsafe_allow_html=True)

# --- (Form ve Diğer Kodlarınız Aşağıda) ---
if 'musteriler' not in st.session_state:
    st.session_state.musteriler = pd.DataFrame(columns=[
        "ID", "Tarih", "İsim", "Telefon", "Model", "Danışman", "Durum", "Test Sürüşü", "Özet"
    ])

with st.form("yeni_kayit", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    isim = col1.text_input("Müşteri Adı Soyadı")
    telefon = col2.text_input("Telefon Numarası")
    model = col3.selectbox("Model", ["BMW 3 Serisi", "MINI 3 KAPI", "Diğer"])
    
    if st.form_submit_button("➕ Müşteriyi Kaydet"):
        yeni_id = str(uuid.uuid4())[:8].upper()
        tarih = datetime.now().strftime("%Y-%m-%d")
        yeni_kayit = pd.DataFrame([[yeni_id, tarih, isim, telefon, model, "Danışman", "Beklemede", "Yapılmadı", "Özet"]], 
                                   columns=st.session_state.musteriler.columns)
        st.session_state.musteriler = pd.concat([st.session_state.musteriler, yeni_kayit], ignore_index=True)
        st.success("Kayıt Başarılı!")

st.subheader("Müşteri Listesi")
st.dataframe(st.session_state.musteriler)