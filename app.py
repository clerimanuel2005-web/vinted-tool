import streamlit as st
import pandas as pd
import requests
import io
import random
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageEnhance

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Vinted Power Seller Suite", page_icon="🛍️", layout="wide")

# Funzione GrabCut: Segmentazione basata sulla geometria, non sull'AI
def extract_tshirt_grabcut(pil_img):
    img = np.array(pil_img.convert("RGB"))
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    mask = np.zeros(img_bgr.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    h, w = img_bgr.shape[:2]
    # GrabCut: isola l'oggetto centrale
    rect = (20, 20, w - 40, h - 40)
    cv2.grabCut(img_bgr, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    img_final = img_bgr * mask2[:, :, np.newaxis]
    img_rgba = cv2.cvtColor(img_final, cv2.COLOR_BGR2RGBA)
    img_rgba[mask2 == 0] = [0, 0, 0, 0]
    return Image.fromarray(img_rgba)

st.title("🛍️ Vinted Power Seller Suite")
st.write("L'hub completo per gestire il tuo business su Vinted.")

tab1, tab2, tab3, tab4 = st.tabs(["📸 Manichino AI", "📝 Annunci", "💰 Prezzi", "📊 Trend"])

# TAB 1: MANICHINO AI (GrabCut + Composizione HD)
with tab1:
    col_foto1, col_foto2 = st.columns([1.2, 1.8], gap="large")
    with col_foto1:
        st.markdown("### 1️⃣ Carica la tua Foto")
        foto_originale = st.file_uploader("Trascina la foto:", type=["jpg", "jpeg", "png"])
        scenario = st.selectbox("Scenario:", ["Gruccia (Cemento)", "Showroom Lusso", "Bianco E-commerce"])
        proporzione = st.slider("Dimensione capo (%):", 50, 90, 70)
        
    with col_foto2:
        if foto_originale:
            if st.button("✨ Genera Foto Catalogo (Metodo GrabCut)"):
                with st.spinner("Calcolo maschera geometrica in corso..."):
                    try:
                        img_input = Image.open(foto_originale)
                        # Isola senza AI
                        maglietta = extract_tshirt_grabcut(img_input)
                        
                        # Composizione
                        risultato = Image.new("RGBA", (1440, 1440), (255, 255, 255, 255))
                        dim = int(1440 * (proporzione / 100))
                        maglietta.thumbnail((dim, dim))
                        pos = ((1440 - maglietta.width)//2, (1440 - maglietta.height)//2)
                        risultato.paste(maglietta, pos, maglietta)
                        
                        st.image(risultato.convert("RGB"), width=580)
                    except Exception as e: st.error(f"Errore: {e}")

# TAB 2: DESCRIZIONI
with tab2:
    st.header("📝 Scrittura Automatica Annunci")
    c_a, c_b = st.columns(2)
    with c_a:
        brand = st.text_input("Brand", placeholder="Es. Off-White")
        tipo = st.text_input("Tipo", placeholder="Es. T-shirt")
        taglia = st.selectbox("Taglia", ["XS", "S", "M", "L", "XL"])
        condizioni = st.selectbox("Condizioni", ["Nuovo", "Ottimo", "Buono"])
    with c_b:
        st.subheader("📋 Testo Pronto")
        desc = f"Vendo {tipo} {brand}. Taglia {taglia}. Condizioni: {condizioni}. Spedizione rapida."
        st.text_area("Copia questo:", desc, height=200)

# TAB 3: CALCOLATORE PREZZI
with tab3:
    st.header("💰 Calcolatore Margini")
    costo = st.number_input("Costo acquisto (€)", value=15.0)
    vendita = st.number_input("Prezzo vendita (€)", value=45.0)
    sconto = st.slider("Sconto lotto (%)", 0, 50, 15)
    
    st.metric("Guadagno Netto", f"{(vendita - costo):.2f} €")
    
    df_prezzi = pd.DataFrame({
        "Voce": ["Costo", "Vendita", "Profitto", "Prezzo Lotto"],
        "Valore": [f"{costo}€", f"{vendita}€", f"{vendita-costo}€", f"{vendita*(1-sconto/100):.2f}€"]
    })
    st.table(df_prezzi)

# TAB 4: TREND DI MERCATO
with tab4:
    st.header("📊 Trend di Mercato")
    st.markdown("### 🔥 Categorie più cercate")
    df_trend = pd.DataFrame({
        "Categoria": ["Streetwear", "Vintage", "Denim", "Accessori"],
        "Trend": ["⬆️ Alta", "➡️ Stabile", "⬆️ Crescita", "⬇️ Basso"]
    })
    st.dataframe(df_trend)
    
    st.markdown("### 📈 Nicchie ad alto margine")
    df_nicchie = pd.DataFrame({
        "Nicchia": ["Band Tees", "Football Jerseys", "Workwear"],
        "Potenziale": ["Eccellente", "Molto Alto", "Alto"]
    })
    st.table(df_nicchie)
