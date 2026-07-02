import streamlit as st
import pandas as pd
import requests
import io
import random
import cv2
import numpy as np
from PIL import Image, ImageOps

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Vinted Power Seller Suite", page_icon="🛍️", layout="wide")

st.title("🛍️ Vinted Power Seller Suite")

# Funzione GrabCut (Sostituisce l'AI che sbagliava)
def extract_tshirt_grabcut(pil_img):
    # Convertiamo PIL a OpenCV (BGR)
    img = np.array(pil_img.convert("RGB"))
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # Creiamo una maschera basata sulla dimensione dell'immagine
    # GrabCut parte dall'idea che il capo sia al centro
    mask = np.zeros(img_bgr.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    
    # Rettangolo che definisce l'area (margine di 50px dai bordi)
    h, w = img_bgr.shape[:2]
    rect = (50, 50, w - 100, h - 100)
    
    # Algoritmo GrabCut
    cv2.grabCut(img_bgr, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    
    # Creiamo una maschera binaria (0 per sfondo, 1 per oggetto)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    img_final = img_bgr * mask2[:, :, np.newaxis]
    
    # Convertiamo di nuovo in PIL RGBA
    img_rgba = cv2.cvtColor(img_final, cv2.COLOR_BGR2RGBA)
    # Impostiamo il trasparente dove la maschera è 0
    img_rgba[mask2 == 0] = [0, 0, 0, 0]
    
    return Image.fromarray(img_rgba)

# ==========================================
# NAVIGAZIONE
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs(["📸 Manichino AI", "📝 Annunci", "💰 Prezzi", "📊 Trend"])

with tab1:
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("Caricamento")
        foto_originale = st.file_uploader("Carica foto:", type=["jpg", "jpeg", "png"])
        proporzione = st.slider("Dimensione:", 50, 90, 70)
        
    with col2:
        if foto_originale:
            if st.button("✨ Genera Foto (Metodo GrabCut)"):
                with st.spinner("Calcolo contorni in corso..."):
                    try:
                        img_input = Image.open(foto_originale)
                        
                        # Usiamo GrabCut invece di rembg
                        maglietta_isolata = extract_tshirt_grabcut(img_input)
                        
                        # Composizione
                        risultato = Image.new("RGBA", (1440, 1440), (255, 255, 255, 255))
                        dim = int(1440 * (proporzione / 100))
                        maglietta_isolata.thumbnail((dim, dim))
                        pos = ((1440 - maglietta_isolata.width)//2, (1440 - maglietta_isolata.height)//2)
                        risultato.paste(maglietta_isolata, pos, maglietta_isolata)
                        
                        st.image(risultato.convert("RGB"), width=500)
                    except Exception as e:
                        st.error(f"Errore tecnico: {e}")

# TAB 2: DESCRIZIONI
with tab2:
    st.header("📝 Generatore Descrizioni")
    brand = st.text_input("Brand")
    tipo = st.text_input("Tipo")
    if st.button("Genera Testo"):
        st.text_area("Copia questo:", f"Vendo {tipo} originale {brand}. In ottime condizioni, lavato e igienizzato.")

# TAB 3: CALCOLATORE PREZZI
with tab3:
    st.header("💰 Calcolatore Margini")
    costo = st.number_input("Costo (€)", value=15.0)
    vendita = st.number_input("Vendita (€)", value=45.0)
    
    st.metric("Guadagno", f"{vendita - costo:.2f} €")
    
    df_prezzi = pd.DataFrame({
        "Voce": ["Costo", "Vendita", "Profitto"], 
        "Valore": [f"{costo}€", f"{vendita}€", f"{vendita-costo}€"]
    })
    st.table(df_prezzi)

# TAB 4: TREND
with tab4:
    st.header("📊 Trend di Mercato")
    df_trend = pd.DataFrame({
        "Categoria": ["Streetwear", "Vintage", "Denim"],
        "Trend": ["⬆️ Alta", "➡️ Stabile", "⬆️ Crescita"]
    })
    st.dataframe(df_trend)
    
    st.table(pd.DataFrame({
        "Nicchia": ["Band Tees", "Football Jerseys"],
        "Potenziale": ["Eccellente", "Molto Alto"]
    }))
