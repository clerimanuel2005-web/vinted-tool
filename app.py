import streamlit as st
import pandas as pd
import requests
import io
import random
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from rembg import remove, new_session

# CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Vinted Power Seller Suite", page_icon="🛍️", layout="wide")

# CACHE RESOURCE: Carica AI una sola volta
@st.cache_resource
def get_session():
    return new_session(model_name="u2net_clothing")

session_clothing = get_session()

st.title("🛍️ Vinted Power Seller Suite")
st.write("L'hub definitivo per gestire il tuo business su Vinted.")

tab1, tab2, tab3, tab4 = st.tabs(["📸 Manichino AI", "📝 Annunci", "💰 Prezzi", "📊 Trend"])

# TAB 1: MANICHINO AI (Con correzione logo)
with tab1:
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("Configurazione")
        foto_originale = st.file_uploader("Carica foto:", type=["jpg", "jpeg", "png"])
        proporzione = st.slider("Dimensione:", 50, 90, 70)
        scenario = st.selectbox("Scenario:", ["Sfondo bianco", "Showroom", "Muro"])
    
    with col2:
        if foto_originale:
            if st.button("✨ Genera Foto"):
                with st.spinner("Elaborazione maglietta..."):
                    try:
                        img_input = Image.open(foto_originale).convert("RGBA")
                        # TRUCCO: Maschera sfocata per ignorare il logo
                        img_blur = img_input.filter(ImageFilter.GaussianBlur(30))
                        maschera = remove(img_blur, session=session_clothing).convert("L")
                        maschera = maschera.filter(ImageFilter.MaxFilter(7))
                        
                        maglietta_isolata = img_input.copy()
                        maglietta_isolata.putalpha(maschera)
                        
                        risultato = Image.new("RGBA", (1440, 1440), (255, 255, 255, 255))
                        dim = int(1440 * (proporzione / 100))
                        maglietta_isolata.thumbnail((dim, dim))
                        pos = ((1440 - maglietta_isolata.width)//2, (1440 - maglietta_isolata.height)//2)
                        risultato.paste(maglietta_isolata, pos, maglietta_isolata)
                        
                        st.image(risultato.convert("RGB"), width=500)
                    except Exception as e:
                        st.error(f"Errore: {e}")

# TAB 2: DESCRIZIONI DETTAGLIATE
with tab2:
    st.header("📝 Generatore Descrizioni")
    c1, c2 = st.columns(2)
    with c1:
        brand = st.text_input("Brand", "Off-White")
        tipo = st.text_input("Tipo", "T-Shirt")
        taglia = st.selectbox("Taglia", ["S", "M", "L", "XL"])
        cond = st.selectbox("Condizioni", ["Nuovo", "Ottimo", "Buono"])
    with c2:
        st.subheader("Testo Generato")
        testo = f"Vendo {tipo} originale {brand}. Taglia {taglia}. Condizioni: {cond}. Ottima qualità."
        st.text_area("Copia/Incolla", testo, height=200)

# TAB 3: CALCOLATORE PREZZI COMPLETO
with tab3:
    st.header("💰 Calcolatore Margini Avanzato")
    costo = st.number_input("Costo Acquisto (€)", value=15.0)
    vendita = st.number_input("Prezzo Vendita (€)", value=45.0)
    sconto = st.slider("Sconto Lotto (%)", 0, 50, 10)
    
    # Tabelle dettagliate
    profitto_singolo = vendita - costo
    profitto_lotto = (vendita * (1 - sconto/100)) - costo
    
    st.metric("Profitto Vendita Singola", f"{profitto_singolo:.2f} €")
    
    st.subheader("Analisi Dettagliata")
    df_prezzi = pd.DataFrame({
        "Tipo": ["Singolo", "Lotto"],
        "Prezzo": [f"{vendita}€", f"{vendita * (1 - sconto/100):.2f}€"],
        "Profitto": [f"{profitto_singolo:.2f}€", f"{profitto_lotto:.2f}€"]
    })
    st.table(df_prezzi)

# TAB 4: TREND DI MERCATO
with tab4:
    st.header("📊 Analisi Trend di Mercato")
    st.subheader("Categorie Hot")
    df_trend = pd.DataFrame({
        "Categoria": ["Streetwear", "Vintage", "Denim", "Accessori"],
        "Volume": ["Alto", "Medio", "Alto", "Basso"],
        "Trend": ["⬆️", "➡️", "⬆️", "⬇️"]
    })
    # Tabella standard senza parametri deprecati
    st.dataframe(df_trend)
    
    st.subheader("Nicchie ad alto margine")
    df_nicchie = pd.DataFrame({
        "Nicchia": ["Band Tees", "Football Jerseys", "Workwear"],
        "Potenziale": ["Eccellente", "Molto Alto", "Alto"]
    })
    st.table(df_nicchie)
